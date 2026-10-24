from logger import logger


class VDP:
    def __init__(self):

        # VRAM and CRAM setup
        self.vram = bytearray(0x4000)
        self.cram = bytearray(0x20)
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

        # Interrupts
        self.line_counter = 0
        self.line_interrupt_pending = False

    def _write_control(self, value):
        if self.control_latch is None:
            self.control_latch = value
            return

        first = self.control_latch
        self.control_latch = None
        code = value >> 6

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

    def _write_data(self, value):
        self.control_latch = None

        if self.code == 0b11:
            self.cram[self.address & 0x1F] = value
        else:
            self.vram[self.address] = value

        self.address = (self.address + 1) & 0x3FFF

    def _read_status(self):
        value = self.status
        self.status &= 0x7F
        self.control_latch = None
        return value

    def _read_data(self):
        self.control_latch = None
        value = self.read_buffer
        self.read_buffer = self.vram[self.address]
        self.address = (self.address + 1) & 0x3FFF
        return value

    def read(self, port):
        if port == 0xBF:
            return self._read_status()

        if port == 0xBE:
            return self._read_data()

        return 0xFF

    def write(self, port, value):

        if port == 0xBF:
            self._write_control(value)
            return

        if port == 0xBE:
            self._write_data(value)
            return

    def irq_line(self):
        frame_irq = bool(self.status & 0x80) and bool(self.registers[1] & 0x20)
        line_irq = self.line_interrupt_pending and bool(self.registers[0] & 0x10)
        return frame_irq or line_irq

    def acknowledge_line_interrupt(self):
        self.line_interrupt_pending = False

    def _get_v_counter(self):
        return self.scanline & 0xFF

    def _get_h_counter(self):
        return 0  # TODO: Implement

    def decode_tile_pixel(self, tile_index, x, y):
        row = tile_index * 32 + y * 4
        bit = 7 - x
        value = 0
        for plane in range(4):
            value |= ((self.vram[row + plane] >> bit) & 1) << plane
        return value

    def colour_rgb(self, palette, index):
        byte = self.cram[palette * 16 + index]
        return (
            (byte & 0x03) * 85,
            ((byte >> 2) & 0x03) * 85,
            ((byte >> 4) & 0x03) * 85,
        )

    def render_background_line(self, y):
        name_table = (self.registers[2] & 0x0E) << 10
        tile_row = (y // 8) * 32
        fine_y = y % 8

        line = []
        for x in range(256):
            entry = name_table + (tile_row + x // 8) * 2
            tile_index = (self.vram[entry] | (self.vram[entry + 1] << 8)) & 0x1FF
            index = self.decode_tile_pixel(tile_index, x % 8, fine_y)
            line.append(self.colour_rgb(0, index))
        return line

    def render_background_frame(self):
        return [self.render_background_line(y) for y in range(192)]

    def tick(self, cycles):
        self.cycles += cycles

        # Columns
        while self.cycles >= 228:
            self.cycles -= 228

            # Rows (Scanlines)
            self.scanline += 1
            if self.scanline >= 262:
                self.scanline = 0

                # Frames
                self.frame += 1

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

            # VBlank interrupt
            if self.scanline == 192:
                self.status |= 0x80
