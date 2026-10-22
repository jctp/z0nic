from logger import logger

class VDP:
    def __init__(self):

        # VRAM and CRAM setup
        self.vram = bytearray(0x4000)
        self.cram = bytearray(0x20)
        self.registers = [0] * 16

        # VBlank
        self.status = 0x80

        # Timing
        self.cycles = 0
        self.scanline = 0
        self.frame = 0

        # Interrupts
        self.frame_interrupt_pending = False
        self.line_interrupt_pending = False

    def _write_control(self, value):
        pass

    def _write_data(self, value):
        pass

    def _read_status(self):
        pass

    def _read_data(self):
        pass

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

    def _get_v_counter(self):
        return self.scanline & 0xFF

    def _get_h_counter(self):
        return 0 # TODO: Implement

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

            # VBlank interrupt
            if self.scanline == 192:
                self.frame_interrupt_pending = True
                self.status |= 0x80
