from logger import logger
import time

from z80.opcodes import dispatcher


class Z80:
    def __init__(self, memory, io, clock_hz, exception_on_non_implemented):
        self.setup()
        self.memory = memory
        self.io = io
        self.clock_hz = clock_hz
        self.exception_on_non_implemented = exception_on_non_implemented

    def setup(self):

        # Main registers
        self.a = 0  # Accumulator
        self.f = 0  # Flag
        self.b = 0  # Accumulator
        self.c = 0  # Flag
        self.d = 0  # Accumulator
        self.e = 0  # Flag
        self.h = 0  # Accumulator
        self.l = 0  # Flag

        # Flag register bits
        self.flag_s = False  # Sign
        self.flag_z = False  # Zero
        self.flag_h = False  # Half Carry
        self.flag_pv = False  # Parity/Overflow
        self.flag_n = False  # Add/Subtract
        self.flag_c = False  # Carry

        # Special registers
        self.pc = 0
        self.sp = 0
        self.ix = 0
        self.iy = 0

        # Interrupt enable flip-flops
        self.iff1 = False
        self.iff2 = False

    def step(self):
        opcode = self.memory.read8(self.pc)
        self.pc += 1

        opcode_t_states = dispatcher.execute(self, opcode)

        # Ensure that opcode_t_states is always valid and avoids divide by zero
        if opcode_t_states in (None, 0):
            opcode_t_states = 1

        time.sleep((1 / self.clock_hz) * opcode_t_states)

    def get_register(self, register):
        # Duplicated opcodes like ADD A,r use this to locate the
        # register embodied in the right three bits of the opcode
        match register:
            case 0:
                return self.b
            case 1:
                return self.c
            case 2:
                return self.d
            case 3:
                return self.e
            case 4:
                return self.h
            case 5:
                return self.l
            case 6:
                hl = (self.h << 8) | self.l
                return self.memory.read8(hl)
            case 7:
                return self.a

    def set_register(self, register, value):
        value &= 0xFF
        match register:
            case 0:
                self.b = value
            case 1:
                self.c = value
            case 2:
                self.d = value
            case 3:
                self.e = value
            case 4:
                self.h = value
            case 5:
                self.l = value
            case 7:
                self.a = value

    def set_register_pair(self, pair, value):
        match pair:
            case 0:  # BC
                self.b = (value >> 8) & 0xFF
                self.c = value & 0xFF
            case 1:  # DE
                self.d = (value >> 8) & 0xFF
                self.e = value & 0xFF
            case 2:  # HL
                self.h = (value >> 8) & 0xFF
                self.l = value & 0xFF
            case 3:  # SP
                self.sp = value & 0xFFFF

    def opcode_not_implemented(self, opcode=0, asm="Unknown"):
        if self.exception_on_non_implemented == True:
            # Most of the time the opcode is handed over raw, but prefixed opcodes use strings for error messages
            if isinstance(opcode, int):
                opcode_string = f"{opcode:02X}"
            else:
                opcode_string = str(opcode)

            with open("debug/crash_opcode.txt", "w") as f:
                f.write(f"PC: {str(self.pc)}\n Opcode: {opcode_string}")
            raise Exception(
                f"PC: {self.pc:04X} - Opcode not implemented: {opcode_string} ({asm})"
            )

        else:
            opcode_t_states = (
                1  # No opcode is executed but we pretend one cycle has passed
            )
            return opcode_t_states

    def log_opcode(
        self, opcode, asm, prefix, opcode_t_states, message, implemented=True
    ):
        logger.debug(
            f"{self.pc:04X}: "
            f"{prefix:<6}"
            f"{opcode:02X} "
            f"[{asm:<12}] "
            f"({opcode_t_states:>3}) "
            f"- {message}"
        )

        if implemented == False:
            self.opcode_not_implemented(opcode, asm)
