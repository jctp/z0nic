from bug_world import enter_bug_world

# region Initialisation


class VDP:
    def __init__(self, video_standard="PAL"):

        # Video mode - NTSC or PAL
        self.video_standard = video_standard

        # Video & Colour RAM
        self.vram = bytearray(0x4000)
        self.cram = bytearray(0x20)

        # Write-only registers R0-15
        self.wo_registers = [0] * 16

        # VRAM AND CRAM ACCESS
        # 14-bit pointer, top-two bits of second control byte decide VRAM or CRAM
        # 0b11 (code 3) sends the command to CRAM
        self.ram_address = 0
        self.vram_read_buffer = 0

        # CONTROL PORT
        # Latch is used to tell VDP when first or second byte of the command word is being sent
        # Set for the first byte, unset for the second
        self.control_port_latch = None
        self.control_port_code = 0b00

        # STATUS
        # Set to 0x80 for Vblank
        # Set to 0x40 for a sprite collision
        # Set to 0x20 for sprite overflow
        self.status = 0x80

        # TIMING
        self.cpu_tstates = 0
        self.scanline = 0
        self.frame_complete = False

        # VIDEO STANDARD SETUP
        self.visible_scanlines = 192  # Default, support for 224 and 240 will come later
        self.visible_columns = 256
        self.total_columns = 342

        if self.video_standard == "NTSC":
            self.tv_hz = 60
            self.total_scanlines = 262
        elif self.video_standard == "PAL":
            self.tv_hz = 50
            self.total_scanlines = 313
        else:
            enter_bug_world(f"Invalid video standard requested: {self.video_standard}")

        # INTERRUPTS
        self.line_counter = 0
        self.line_interrupt_pending = False

        # OUTPUT
        # The finished frame to be returned to the emulator
        self.frame = 0 # counter
        self.frame_lines = [None] * self.visible_scanlines
        self.drawn_frame = None

    # endregion

    # region Helpers

    def _inc_ram_address(self, by=1):
        self.ram_address = (self.ram_address + by) & 0x3FFF

    # region Read/Write

    # I/O read dispatch: 0xBE data, 0xBF status, others open bus (0xFF)
    def read(self, port):
        if port == 0xBE:
            return self._read_data()
        if port == 0xBF:
            return self._read_status()
        return 0xFF

    # I/O write dispatch: 0xBE data, 0xBF control
    def write(self, port, value):
        if port == 0xBE:
            self._write_data(value)
        elif port == 0xBF:
            self._write_control(value)

    def _read_data(self):
        # Reads return the byte prefetched by the
        # previous access!
        # This is caches in vram_read_buffer
        self.control_port_latch = None
        value = self.vram_read_buffer
        self.vram_read_buffer = self.vram[self.ram_address]
        self._inc_ram_address(1)
        return value

    def _read_status(self):
        status = self.status
        self.status = 0
        self.control_port_latch = None
        return status

    def _write_data(self, value):
        self.control_port_latch = None

        if self.control_port_code == 0b11:
            self._cram_write(value)
        else:
            self._vram_write(value)

        self._inc_ram_address(1)

    def _vram_write(self, value):
        self.vram[self.ram_address] = value

    def _cram_write(self, value):
        self.cram[self.ram_address & 0x1F] = value

    def _write_control(self, value):
        # First byte is latched; second byte selects either
        # a register write or an address set
        if self.control_port_latch is None:
            self.control_port_latch = value
            return

        first_write_byte = self.control_port_latch
        second_write_byte = value
        self.control_port_latch = None
        code = second_write_byte >> 6

        # Register write: only the register changes, the address and code are left alone
        if code == 0b10:
            self._register_write(first_write_byte, second_write_byte)
            return

        self.control_port_code = code
        self.ram_address = ((second_write_byte & 0x3F) << 8 | first_write_byte) & 0x3FFF

        match code:
            # VRAM read
            case 0b00:
                self._vram_read()

    def _vram_read(self):
        self.vram_read_buffer = self.vram[self.ram_address]
        self._inc_ram_address(1)

    def _register_write(self, value_byte, address_byte):
        self.wo_registers[address_byte & 0x0F] = value_byte

    # endregion

    # region Decoding

    # Reads one pixel of a 4bpp planar 8x8 tile (32 bytes, four bitplanes per row).
    def decode_tile_pixel(self, tile_index, x, y):
        row = tile_index * 32 + y * 4
        bit = 7 - x
        value = 0
        for plane in range(4):
            value |= ((self.vram[row + plane] >> bit) & 1) << plane
        return value

    # Converts a CRAM entry (2 bits per channel) to 0-255 RGB.
    def colour_rgb(self, palette, index):
        byte = self.cram[palette * 16 + index]
        return (
            (byte & 0x03) * 85,
            ((byte >> 2) & 0x03) * 85,
            ((byte >> 4) & 0x03) * 85,
        )

    # Name table address from R2 bits 1-3; each row is 32 entries of 2 bytes.
    def _name_entry_address(self, column, row):
        name_table = (self.wo_registers[2] & 0x0E) << 10
        return name_table + (row * 32 + column) * 2

    def _name_entry(self, column, row):
        address = self._name_entry_address(column % 32, row % 28)
        return self.vram[address] | (self.vram[address + 1] << 8)

    def _tile_row(self, y):
        return y // 8

    def _tile_index(self, entry):
        return entry & 0x1FF

    def _tile_flip_x(self, entry):
        return bool(entry & 0x0200)

    def _tile_flip_y(self, entry):
        return bool(entry & 0x0400)

    def _tile_palette(self, entry):
        return (entry >> 11) & 0x01

    def _tile_priority(self, entry):
        return bool(entry & 0x1000)

    # R0 bit 6 locks horizontal scroll on the top two rows; R0 bit 7 locks vertical scroll on columns 24-31.
    def _background_sample(self, x, y):
        if self.wo_registers[0] & 0x40 and y < 16:
            bg_x = x
        else:
            bg_x = (x - self.wo_registers[8]) % 256

        if self.wo_registers[0] & 0x80 and x >= 192:
            bg_y = y
        else:
            bg_y = (y + self.wo_registers[9]) % 224

        entry = self._name_entry(bg_x // 8, self._tile_row(bg_y))

        fine_x = bg_x % 8
        fine_y = bg_y % 8
        if self._tile_flip_x(entry):
            fine_x = 7 - fine_x
        if self._tile_flip_y(entry):
            fine_y = 7 - fine_y

        index = self.decode_tile_pixel(self._tile_index(entry), fine_x, fine_y)
        if index == 0:
            return self.colour_rgb(1, self.wo_registers[7] & 0x0F), False, False
        return (
            self.colour_rgb(self._tile_palette(entry), index),
            True,
            self._tile_priority(entry),
        )

    # endregion

    # region Sprites

    # Sprite attribute table base from R5 bits 1-6.
    def _sprite_table(self):
        return (self.wo_registers[5] & 0x7E) << 7

    def _sprite_height(self):
        return 16 if self.wo_registers[1] & 0x02 else 8

    # Up to 8 sprites covering line y; a Y byte of 0xD0 ends the list.
    def _sprites_on_line(self, y):
        table = self._sprite_table()
        height = self._sprite_height()
        found = []
        overflow = False
        for i in range(64):
            sprite_y = self.vram[table + i]
            if sprite_y == 0xD0:
                break
            top = (sprite_y + 1) & 0xFF
            row = (y - top) & 0xFF
            if row < height:
                if len(found) == 8:
                    overflow = True
                    break
                found.append((i, row))
        return found, overflow

    # Colour index 0 is transparent and earlier sprites win.
    def _sprite_line(self, y):
        table = self._sprite_table()
        height = self._sprite_height()
        found, overflow = self._sprites_on_line(y)
        pixels = [None] * 256
        occupied = [False] * 256
        collision = False
        for i, row in found:
            x = self.vram[table + 0x80 + i * 2]
            tile = self.vram[table + 0x81 + i * 2]
            if self.wo_registers[0] & 0x08:
                x -= 8
            if height == 16:
                tile &= 0xFE
                if row >= 8:
                    tile += 1
                    row -= 8
            if self.wo_registers[6] & 0x04:
                tile += 256
            for col in range(8):
                sx = x + col
                if not 0 <= sx < 256:
                    continue
                index = self.decode_tile_pixel(tile, col, row)
                if not index:
                    continue
                if occupied[sx]:
                    collision = True
                    continue
                occupied[sx] = True
                pixels[sx] = self.colour_rgb(1, index)
        return pixels, collision, overflow

    # endregion

    # region Interrupts

    # Interrupt output: frame IRQ (R1 bit 5) or line IRQ (R0 bit 4).
    def irq_line(self):
        frame_irq = bool(self.status & 0x80) and bool(self.wo_registers[1] & 0x20)
        line_irq = self.line_interrupt_pending and bool(self.wo_registers[0] & 0x10)
        return frame_irq or line_irq

    # Clears the pending line interrupt once the CPU has taken it.
    def acknowledge_line_interrupt(self):
        self.line_interrupt_pending = False

    # endregion

    # region Assembly

    def render_line(self, y):
        backdrop = self.colour_rgb(1, self.wo_registers[7] & 0x0F)
        if not self.wo_registers[1] & 0x40:
            return [backdrop] * 256

        background = [self._background_sample(x, y) for x in range(256)]
        sprites, collision, overflow = self._sprite_line(y)
        if collision:
            self.status |= 0x20
        if overflow:
            self.status |= 0x40

        line = []
        for x in range(256):
            colour, opaque, priority = background[x]
            if sprites[x] is not None and not (priority and opaque):
                colour = sprites[x]
            if self.wo_registers[0] & 0x20 and x < 8:
                colour = backdrop
            line.append(colour)
        return line

    def render_frame(self):
        return self.drawn_frame

    # endregion

    # region Graphics Tick

    # H counter: 171 values per line, with 0x94-0xE8 skipped (the SMS counter jumps there).
    def _get_h_counter(self):
        count = (self.cpu_tstates * 3) // 4
        return count if count <= 0x93 else count + 0x55

    # V counter: low 8 bits of the current scanline.
    def _get_v_counter(self):
        return self.scanline & 0xFF

    def tick(self, cpu_tstates):
        self.cpu_tstates += cpu_tstates

        # Columns
        while self.cpu_tstates >= 228:
            self.cpu_tstates -= 228

            # Scanlines
            self.scanline += 1

            # Frame is complete and handed back to the emulator
            if self.scanline >= self.total_scanlines:
                self.scanline = 0
                self.frame += 1
                self.drawn_frame = self.frame_lines
                self.frame_lines = [None] * self.visible_scanlines
                self.frame_complete = True

            if self.scanline == 0:
                self.line_counter = self.wo_registers[10]
            elif self.scanline <= self.visible_scanlines:
                if self.line_counter == 0:
                    self.line_counter = self.wo_registers[10]
                    self.line_interrupt_pending = True
                else:
                    self.line_counter -= 1

            if self.scanline < self.visible_scanlines:
                self.frame_lines[self.scanline] = self.render_line(self.scanline)

            # VBlank Interrupt
            if self.scanline == self.visible_scanlines:
                self.status |= 0x80

    # endregion
