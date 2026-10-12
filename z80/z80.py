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

        # Alternate registers
        self.a_alt = 0
        self.f_alt = 0

        self.b_alt = 0
        self.c_alt = 0

        self.d_alt = 0
        self.e_alt = 0

        self.h_alt = 0
        self.l_alt = 0

        # Flag register bits
        self.flag_s = False  # Sign
        self.flag_z = False  # Zero
        self.flag_h = False  # Half Carry
        self.flag_pv = False  # Parity/Overflow
        self.flag_n = False  # Add/Subtract
        self.flag_c = False  # Carry

        # Alternate flag register bits
        self.flag_s_alt = False
        self.flag_z_alt = False
        self.flag_h_alt = False
        self.flag_pv_alt = False
        self.flag_n_alt = False
        self.flag_c_alt = False

        # Special registers
        self.pc = 0
        self.sp = 0
        self.ix = 0
        self.iy = 0

        # Interrupt enable flip-flops
        self.iff1 = False
        self.iff2 = False

        # Interrupt state
        self.interrupt_mode = 0
        self.interrupt_pending = False
        self.cycles_since_interrupt = 0

    def step(self):
        opcode = self.memory.read8(self.pc)
        self.pc += 1

        opcode_t_states = dispatcher.execute(self, opcode)

        # Ensure that opcode_t_states is always valid and avoids divide by zero
        if opcode_t_states in (None, 0):
            opcode_t_states = 1

        # Simple interrupt test
        self.cycles_since_interrupt += opcode_t_states

        if self.cycles_since_interrupt >= 50000:
            self.interrupt_pending = True
            self.cycles_since_interrupt = 0

        if self.interrupt_pending:
            self.interrupt()
            self.interrupt_pending = False

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

    def get_register_pair(self, pair):
        match pair:
            case 0:     # BC
                return self.get_bc()
            case 1:     # DE
                return self.get_de()
            case 2:     # HL
                return self.get_hl()
            case 3:     # AF
                return self.get_af()

    def set_register_pair(self, pair, value):
        match pair:
            case 0:     # BC
                self.set_bc(value)
            case 1:     # DE
                self.set_de(value)
            case 2:     # HL
                self.set_hl(value)
            case 3:     # AF
                self.set_af(value)

    def push16(self, value):
        self.sp -= 1
        self.memory.write8(
            self.sp,
            (value >> 8) & 0xFF
        )
        self.sp -= 1
        self.memory.write8(
            self.sp,
            value & 0xFF
        )

    def pop16(self):
        low = self.memory.read8(self.sp)
        self.sp += 1
        high = self.memory.read8(self.sp)
        self.sp += 1
        return (high << 8) | low

    def exchange_af(self):

        logger.debug(
            f"BEFORE EX AF: A={self.a:02X} ALT={self.a_alt:02X}"
        )

        self.a, self.a_alt = (
            self.a_alt,
            self.a
        )

        self.flag_s, self.flag_s_alt = (
            self.flag_s_alt,
            self.flag_s
        )

        self.flag_z, self.flag_z_alt = (
            self.flag_z_alt,
            self.flag_z
        )

        self.flag_h, self.flag_h_alt = (
            self.flag_h_alt,
            self.flag_h
        )

        self.flag_pv, self.flag_pv_alt = (
            self.flag_pv_alt,
            self.flag_pv
        )

        self.flag_n, self.flag_n_alt = (
            self.flag_n_alt,
            self.flag_n
        )

        self.flag_c, self.flag_c_alt = (
            self.flag_c_alt,
            self.flag_c
        )

        logger.debug(
            f"AFTER EX AF: A={self.a:02X} ALT={self.a_alt:02X}"
        )
        
    def exchange_bcdEhl(self):
        self.b, self.b_alt = self.b_alt, self.b
        self.c, self.c_alt = self.c_alt, self.c
        self.d, self.d_alt = self.d_alt, self.d
        self.e, self.e_alt = self.e_alt, self.e
        self.h, self.h_alt = self.h_alt, self.h
        self.l, self.l_alt = self.l_alt, self.l

    # BC register pair
    # Combines B and C into a 16-bit value
    def get_bc(self):
        return (self.b << 8) | self.c

    # BC register pair
    # Splits a 16-bit value into B and C
    def set_bc(self, value):
        value &= 0xFFFF

        self.b = (value >> 8) & 0xFF
        self.c = value & 0xFF

    # DE register pair
    # Combines D and E into a 16-bit value
    def get_de(self):
        return (self.d << 8) | self.e

    # DE register pair
    # Splits a 16-bit value into D and E
    def set_de(self, value):
        value &= 0xFFFF
        self.d = (value >> 8) & 0xFF
        self.e = value & 0xFF

    # HL register pair
    # Combines H and L into a 16-bit value
    def get_hl(self):
        return (self.h << 8) | self.l

    # HL register pair
    # Splits a 16-bit value into H and L
    def set_hl(self, value):
        value &= 0xFFFF
        self.h = (value >> 8) & 0xFF
        self.l = value & 0xFF

    # AF register pair
    # Combines A and the individual CPU flags into a 16-bit value
    def get_af(self):
        flags = (
            (self.flag_s  << 7) |
            (self.flag_z  << 6) |
            (self.flag_h  << 4) |
            (self.flag_pv << 2) |
            (self.flag_n  << 1) |
            (self.flag_c)
        )
        return (self.a << 8) | flags

    # AF register pair
    # Loads A and the CPU flags from a 16-bit value
    def set_af(self, value):
        value &= 0xFFFF
        self.a = (value >> 8) & 0xFF
        f = value & 0xFF
        self.flag_s = bool(f & 0x80)
        self.flag_z = bool(f & 0x40)
        self.flag_h = bool(f & 0x10)
        self.flag_pv = bool(f & 0x04)
        self.flag_n = bool(f & 0x02)
        self.flag_c = bool(f & 0x01)

    def interrupt(self):

        if not self.iff1:
            return

        logger.debug(
            f"INTERRUPT IM{self.interrupt_mode}"
        )

        self.iff1 = False
        self.iff2 = False

        self.push16(self.pc)

        match self.interrupt_mode:

            case 0:
                logger.warning(
                    "IM0 interrupt"
                )

            case 1:
                self.pc = 0x0038

            case 2:
                logger.warning(
                    "IM2 interrupt"
                )

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
