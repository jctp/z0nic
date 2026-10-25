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
        self.vram_cram_address = 0
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
        self.frame = 0
        self.frame_complete = True

        # VIDEO STANDARD SETUP
        self.visible_scanlines = 192 # Default, support for 224 and 240 will come later
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
        self.frame_lines = [None] * self.visible_scanlines
        self.complete_frame = None

# endregion
# region Read/Write

    def _write_control(self, value):
        # First byte is latched; second byte selects either
        # a register write or an address set
        if self.control_port_latch is None:
            self.control_port_latch = value
            return

        self.first_write_byte = self.control_port_latch
        self.second_write_byte = value
        self.control_port_latch = None
        command_code = self.second_write_byte >> 6
        self.write_word = (self.first_write_byte << 8 | self.second_write_byte) & 0xFFFF

        # command_code can be one of four values:
        # 00 is a VRAM read
        # 01 is a VRAM write
        # 10 is a register write
        # 11 is a CRAM write

        match command_code:

            # VRAM read
            case 0b00:
                self._vram_read()

            # VRAM write
            case 0b01:
                self._vram_write()

            # Register write
            case 0b10:
                self._register_write()

            # CRAM write
            case 0b11:
                self._cram_write()

            case _:
                enter_bug_world("Invalid VDP command code ({command_code})")

    def _vram_read(self):
        pass

    def _vram_write(self):
        pass

    def _register_write(self):
        pass

    def _cram_write(self):
        pass

    def tick(self, t_states):
        pass
            





# endregion

# region Decoding
# endregion

# region Scanlines
# endregion

# region Sprites
# endregion

# region Graphics Tick
# endregion
