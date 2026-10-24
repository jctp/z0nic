# Note: this file was **mostly LLM-coded** and has not been verified against hardware.
# This project was to learn the Z80 - this is a bonus in order to actually do something fun with it.
# Sega Master System VDP (TMS9918-derived): VRAM, CRAM, registers, timing, and renderer.
#
# Data path, Z80 to screen:
# 1. The Z80 runs OUT (0xBE/0xBF) or IN; the I/O layer calls write() or read() here.
# 2. Port 0xBF (control) takes two bytes: a register write, or an address set that
#    picks VRAM or CRAM. Port 0xBE (data) moves bytes to or from that address.
# 3. VRAM holds the name table (which tile goes where), tile pixels, and the sprite
#    attribute table. CRAM holds 32 colours: palette 0 for background, 1 for sprites.
# 4. tick() advances the scanline counter with CPU cycles. At line 192 it sets VBlank,
#    and irq_line() reports the interrupt for the Z80 to take.
# 5. tick() draws each line into the frame as its scanline starts, combining background
#    and sprites into RGB; render_frame() returns the last completed frame.
# 6. system.py passes finished frames to the PNG writer in frame_dump.py. This emulator
#    has no live window; the PNG files are the screen.

from logger import logger


class VDP:
    def __init__(self):

        # VRAM and CRAM setup
        self.vram = bytearray(0x4000)
        self.cram = bytearray(0x20)
        # Write-only registers R0-R15.
        self.registers = [0] * 16

        # VRAM access: the data port reads through a one-byte read-ahead buffer
        self.address = 0
        self.read_buffer = 0

        # Control port: first byte of a two-byte command, and the command code
        self.control_latch = None
        self.code = 0b00

        # VBlank
        self.status = 0x80

        # Timing
        self.cycles = 0
        self.scanline = 0
        self.frame = 0
        self.frame_complete = False

        # Interrupts
        self.line_counter = 0
        self.line_interrupt_pending = False

        # Lines are drawn as the scanline reaches them, so mid-frame register changes apply from that line
        self.frame_lines = [None] * 192
        self.completed_frame = None

    # Control port: first byte is latched, second byte selects a register write or address set.
    def _write_control(self, value):
        if self.control_latch is None:
            self.control_latch = value
            return

        first = self.control_latch
        self.control_latch = None
        code = value >> 6

        # Second byte code: 00 VRAM read, 01 VRAM write, 10 register write, 11 CRAM write.
        # Register write: 10rrrr with the data in the first byte
        if code == 0b10:
            self.registers[value & 0x0F] = first
            return

        # Address set: the second byte supplies address bits 13-8
        self.address = ((value & 0x3F) << 8 | first) & 0x3FFF
        self.code = code

        if code == 0b00:
            self.read_buffer = self.vram[self.address]
            self.address = (self.address + 1) & 0x3FFF

    # Data port write: goes to CRAM when code is 0b11, otherwise VRAM; auto-increments address.
    def _write_data(self, value):
        self.control_latch = None

        if self.code == 0b11:
            self.cram[self.address & 0x1F] = value
        else:
            self.vram[self.address] = value

        self.address = (self.address + 1) & 0x3FFF

    # Status read: returns flags, then clears VBlank and the control latch.
    def _read_status(self):
        value = self.status
        self.status &= 0x7F
        self.control_latch = None
        return value

    # Data port read: returns the buffered byte and prefetches the next VRAM byte.
    def _read_data(self):
        self.control_latch = None
        # Reads return the byte prefetched on the previous access, so they lag one byte behind.
        value = self.read_buffer
        self.read_buffer = self.vram[self.address]
        self.address = (self.address + 1) & 0x3FFF
        return value

    # I/O read dispatch: 0xBE data, 0xBF status, others open bus (0xFF).
    # Called by the I/O layer when the Z80 executes IN.
    def read(self, port):
        if port == 0xBF:
            return self._read_status()

        if port == 0xBE:
            return self._read_data()

        return 0xFF

    # I/O write dispatch: 0xBE data, 0xBF control.
    def write(self, port, value):

        if port == 0xBF:
            self._write_control(value)
            return

        if port == 0xBE:
            self._write_data(value)
            return

    # Interrupt output: frame IRQ (R1 bit 5) or line IRQ (R0 bit 4).
    def irq_line(self):
        frame_irq = bool(self.status & 0x80) and bool(self.registers[1] & 0x20)
        line_irq = self.line_interrupt_pending and bool(self.registers[0] & 0x10)
        return frame_irq or line_irq

    # Clears the pending line interrupt once the CPU has taken it.
    def acknowledge_line_interrupt(self):
        self.line_interrupt_pending = False

    # V counter: low 8 bits of the current scanline.
    def _get_v_counter(self):
        return self.scanline & 0xFF

    # H counter is not emulated; always returns 0.
    def _get_h_counter(self):
        return 0  # TODO: Implement

    # Reads one pixel of a 4bpp planar 8x8 tile (32 bytes, four bitplanes per row).
    def decode_tile_pixel(self, tile_index, x, y):
        row = tile_index * 32 + y * 4
        bit = 7 - x
        value = 0
        for plane in range(4):
            value |= ((self.vram[row + plane] >> bit) & 1) << plane
        return value

    # Converts a CRAM entry (2 bits per channel) to 0-255 RGB; palette 0 is BG, 1 is sprites.
    def colour_rgb(self, palette, index):
        byte = self.cram[palette * 16 + index]
        return (
            (byte & 0x03) * 85,
            ((byte >> 2) & 0x03) * 85,
            ((byte >> 4) & 0x03) * 85,
        )

    # Name table address from R2 bits 1-3; each row is 32 entries of 2 bytes.
    def _name_entry_address(self, column, row):
        name_table = (self.registers[2] & 0x0E) << 10
        return name_table + (row * 32 + column) * 2

    # Reads a name table entry; the 32x28 map wraps. Entry is little-endian.
    def _name_entry(self, column, row):
        address = self._name_entry_address(column % 32, row % 28)
        return self.vram[address] | (self.vram[address + 1] << 8)

    # Converts a pixel row to a tile row.
    def _tile_row(self, y):
        return y // 8

    # Name entry bits: 0-8 tile, 9 flip X, 10 flip Y, 11 palette, 12 priority.
    def _tile_index(self, entry):
        return entry & 0x1FF

    def _tile_flip_x(self, entry):
        return bool(entry & 0x0200)

    def _tile_flip_y(self, entry):
        return bool(entry & 0x0400)

    def _tile_palette(self, entry):
        return (entry >> 11) & 0x01

    # Priority bit: background tile covers sprites where its pixel is non-zero.
    def _tile_priority(self, entry):
        return bool(entry & 0x1000)

    # Returns (rgb, opaque, priority) for one background pixel after scrolling.
    def _background_sample(self, x, y):
        bg_x = (x - self.registers[8]) % 256
        bg_y = (y + self.registers[9]) % 224

        entry = self._name_entry(bg_x // 8, self._tile_row(bg_y))

        fine_x = bg_x % 8
        fine_y = bg_y % 8
        if self._tile_flip_x(entry):
            fine_x = 7 - fine_x
        if self._tile_flip_y(entry):
            fine_y = 7 - fine_y

        index = self.decode_tile_pixel(self._tile_index(entry), fine_x, fine_y)
        if index == 0:
            return self.colour_rgb(1, self.registers[7] & 0x0F), False, False
        return (
            self.colour_rgb(self._tile_palette(entry), index),
            True,
            self._tile_priority(entry),
        )

    # Sprite attribute table base from R5 bits 1-6; Y bytes first, then X/tile pairs.
    def _sprite_table(self):
        return (self.registers[5] & 0x7E) << 7

    # R1 bit 1 selects 8x16 sprites instead of 8x8.
    def _sprite_height(self):
        return 16 if self.registers[1] & 0x02 else 8

    # Up to 8 sprites covering line y; a Y byte of 0xD0 ends the list.
    def _sprites_on_line(self, y):
        table = self._sprite_table()
        height = self._sprite_height()
        found = []
        for i in range(64):
            sprite_y = self.vram[table + i]
            if sprite_y == 0xD0:
                break
            top = (sprite_y + 1) & 0xFF
            row = (y - top) & 0xFF
            if row < height:
                found.append((i, row))
                if len(found) == 8:
                    break
        return found

    # Renders sprite pixels for line y; colour index 0 is transparent, earlier sprites win.
    def _sprite_line(self, y):
        table = self._sprite_table()
        height = self._sprite_height()
        pixels = [None] * 256
        for i, row in self._sprites_on_line(y):
            x = self.vram[table + 0x80 + i * 2]
            tile = self.vram[table + 0x81 + i * 2]
            if self.registers[0] & 0x08:
                x -= 8
            if height == 16:
                tile &= 0xFE
                if row >= 8:
                    tile += 1
                    row -= 8
            if self.registers[6] & 0x04:
                tile += 256
            for col in range(8):
                sx = x + col
                if not 0 <= sx < 256 or pixels[sx] is not None:
                    continue
                index = self.decode_tile_pixel(tile, col, row)
                if index:
                    pixels[sx] = self.colour_rgb(1, index)
        return pixels

    # Composites background, sprites, and column-0 blanking for one line.
    def render_line(self, y):
        background = [self._background_sample(x, y) for x in range(256)]
        sprites = self._sprite_line(y)
        line = []
        for x in range(256):
            colour, opaque, priority = background[x]
            if sprites[x] is not None and not (priority and opaque):
                colour = sprites[x]
            if self.registers[0] & 0x20 and x < 8:
                colour = self.colour_rgb(1, self.registers[7] & 0x0F)
            line.append(colour)
        return line

    # Returns the last completed frame as 192 rows; system.py passes it to the PNG writer.
    def render_frame(self):
        return self.completed_frame

    # Advances timing by CPU cycles; raises VBlank at line 192 and frame_complete on wrap.
    # Called by system.py after each CPU step with the cycles that step consumed.
    def tick(self, cycles):
        self.cycles += cycles

        # Columns
        while self.cycles >= 228:
            self.cycles -= 228

            # Rows (Scanlines)
            self.scanline += 1
            if self.scanline >= 313:
                self.scanline = 0

                # Frames: keep the finished picture until the next frame completes
                self.frame += 1
                self.completed_frame = self.frame_lines
                self.frame_lines = [None] * 192
                self.frame_complete = True

            # Line counter: reloaded from R10 at the top of the frame, then
            # counts down each active line and raises the line interrupt on expiry
            if self.scanline == 0:
                self.line_counter = self.registers[10]
            elif self.scanline <= 192:
                if self.line_counter == 0:
                    self.line_counter = self.registers[10]
                    self.line_interrupt_pending = True
                else:
                    self.line_counter -= 1

            if self.scanline < 192:
                self.frame_lines[self.scanline] = self.render_line(self.scanline)

            # VBlank interrupt
            if self.scanline == 192:
                self.status |= 0x80
