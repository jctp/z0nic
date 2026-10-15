from logger import logger
import datetime
import time

from z80.opcodes import dispatcher

# endregion
# region Z80 CPU


class Z80:
    def __init__(
        self,
        memory,
        io,
        clock_hz,
        exception_on_non_implemented,
        register_check,
        heartbeat_seconds=False,
        opcode_trace=None,
    ):
        self.setup()
        self.memory = memory
        self.io = io
        self.clock_hz = clock_hz
        self.exception_on_non_implemented = exception_on_non_implemented
        self.register_check = register_check
        self.heartbeat_seconds = heartbeat_seconds
        self.opcode_trace = opcode_trace

    # endregion
    # region Z80 Setup

    def setup(self):
        # Diagnostic variables
        self.heartbeat_counter = 0  # Counts cycles to log status message every X cycles instead of full DEBUG level

        # Main registers
        self.a = 0  # Accumulator
        self.f = 0  # Flag

        self.b = 0  # Accumulator
        self.c = 0  # Flag

        self.d = 0  # Accumulator
        self.e = 0  # Flag

        self.h = 0  # Accumulator
        self.l = 0  # Flag

        self.i = 0
        self.r = 0

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

    # endregion
    # region PC Control

    # Increment PC with wraparound
    def inc_pc(self, increment=1):
        self.pc = (self.pc + increment) & 0xFFFF

    # Set PC directly with wraparound
    def set_pc(self, value):
        self.pc = value & 0xFFFF

    # endregion
    # region Opcode Helpers

    # Helper for BIT b,(IX+d)
    def bit_ix_displacement(self, displacement, bit):
        if displacement & 0x80:
            displacement -= 0x100

        address = (self.ix + displacement) & 0xFFFF

        value = self.memory.read8(address)

        result = value & (1 << bit)

        self.flag_z = result == 0
        self.flag_pv = result == 0
        self.flag_h = True
        self.flag_n = False

        if bit == 7:
            self.flag_s = bool(result)

        return value

    # Helper for LD r,(IX+d)
    def load_register_from_ix_displacement(self, displacement, register):
        if displacement & 0x80:
            displacement -= 0x100

        address = (self.ix + displacement) & 0xFFFF

        value = self.memory.read8(address)

        self.set_register(register, value)

        return value

    # Helper for LD (IX+d),r
    def store_register_to_ix_displacement(self, displacement, register):
        if displacement & 0x80:
            displacement -= 0x100

        address = (self.ix + displacement) & 0xFFFF

        value = self.get_register(register)

        self.memory.write8(address, value)

        return value

    # Helper for LD (nn),rr
    def store_register_pair(self, value):
        address = self.read16_immediate()
        self.memory.write8(address, value & 0xFF)
        self.memory.write8((address + 1) & 0xFFFF, (value >> 8) & 0xFF)
        return address

    # Helper for LD rr,(nn)
    def load_register_pair(self, setter):
        address = self.read16_immediate()
        value = self.read16(address)
        setter(value)
        return value, address

    # Duplicated opcodes like ADD A,r use this to locate the
    # register embodied in the right three bits of the opcode
    def get_register(self, register):
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
            case 0:  # BC
                return self.get_bc()
            case 1:  # DE
                return self.get_de()
            case 2:  # HL
                return self.get_hl()
            case 3:  # AF
                return self.get_af()

    def set_register_pair(self, pair, value):
        match pair:
            case 0:  # BC
                self.set_bc(value)
            case 1:  # DE
                self.set_de(value)
            case 2:  # HL
                self.set_hl(value)
            case 3:  # AF
                self.set_af(value)

    # Helper for LDI, LDIR, LDD, LDDR
    def block_transfer_helper(self, increment, repeat):
        match increment, repeat:
            # LDI
            case 1, 0:
                t_states = 15
                value = self.memory.read8(self.get_hl())
                self.memory.write8(self.get_de(), value)
                self.set_hl((self.get_hl() + 1) & 0xFFFF)
                self.set_de((self.get_de() + 1) & 0xFFFF)
                self.set_bc((self.get_bc() - 1) & 0xFFFF)
                self.flag_h = 0
                self.flag_pv = int(self.get_bc() != 0)
                self.flag_n = 0
                return t_states

            # LDIR
            case 1, 1:
                value = self.memory.read8(self.get_hl())
                self.memory.write8(self.get_de(), value)

                self.set_hl((self.get_hl() + 1) & 0xFFFF)
                self.set_de((self.get_de() + 1) & 0xFFFF)
                self.set_bc((self.get_bc() - 1) & 0xFFFF)

                if self.get_bc() != 0:
                    t_states = 21
                    self.pc = (self.pc - 2) & 0xFFFF
                else:
                    t_states = 16

                if self.get_bc() == 0:
                    logger.debug("LDIR COMPLETE")

                self.flag_h = 0
                self.flag_pv = int(self.get_bc() != 0)
                self.flag_n = 0

                return t_states

            # LDD
            case 0, 0:
                t_states = 16
                value = self.memory.read8(self.get_hl())
                self.memory.write8(self.get_de(), value)
                self.set_hl((self.get_hl() - 1) & 0xFFFF)
                self.set_de((self.get_de() - 1) & 0xFFFF)
                self.set_bc((self.get_bc() - 1) & 0xFFFF)
                self.flag_h = 0
                self.flag_pv = int(self.get_bc() != 0)
                self.flag_n = 0
                return t_states

            # LDDR
            case 0, 1:
                value = self.memory.read8(self.get_hl())
                self.memory.write8(self.get_de(), value)
                self.set_hl((self.get_hl() - 1) & 0xFFFF)
                self.set_de((self.get_de() - 1) & 0xFFFF)
                self.set_bc((self.get_bc() - 1) & 0xFFFF)

                if self.get_bc() != 0:
                    t_states = 21
                    self.pc = (self.pc - 2) & 0xFFFF
                else:
                    t_states = 16

                self.flag_h = 0
                self.flag_pv = int(self.get_bc() != 0)
                self.flag_n = 0

                return t_states

    # endregion
    # region Push/Pop Helpers

    def push16(self, value):
        self.sp = (self.sp - 1) & 0xFFFF
        self.memory.write8(self.sp, (value >> 8) & 0xFF)
        self.sp = (self.sp - 1) & 0xFFFF
        self.memory.write8(self.sp, value & 0xFF)

    def pop16(self):
        low = self.memory.read8(self.sp)
        self.sp = (self.sp + 1) & 0xFFFF
        high = self.memory.read8(self.sp)
        self.sp = (self.sp + 1) & 0xFFFF
        return (high << 8) | low

    # Helper for PUSH rr
    def push_register_pair(self, value):
        self.push16(value)
        return value

    # Helper for POP rr instructions
    def pop_register_pair(self, setter):
        value = self.pop16()
        setter(value)
        return value

    # Helper for INC rr instructions
    def increment_register_pair(self, getter, setter):
        value = (getter() + 1) & 0xFFFF
        setter(value)
        return value

    # Helper for INI, IND, INIR, and INDR
    def block_in(self, increment, repeat):
        # Read the value from port BC
        value = self.io.read(self.get_bc())

        # Write the value to memory at HL
        self.memory.write8(self.get_hl(), value)

        # Decrement B
        self.b = (self.b - 1) & 0xFF

        # Advance or retreat HL
        self.set_hl((self.get_hl() + increment) & 0xFFFF)

        # TODO: Accurate flag behaviour

        # INIR and INDR repeat until B becomes zero
        if repeat and self.b != 0:
            self.set_pc(self.pc - 2)
            return 21

        return 16

    # endregion

    # region Read/Writes

    # Read two bytes from an address as a 16-bit value
    def read16(self, address):
        low = self.memory.read8(address)
        high = self.memory.read8((address + 1) & 0xFFFF)
        return (high << 8) | low

    # Read two bytes from an address immediately, incrementing PC accordingly
    def read16_immediate(self):
        value = self.read16(self.pc)
        self.pc = (self.pc + 2) & 0xFFFF
        return value

    # Helper for LD rr,nn instructions
    # Read a 16-bit immediate value and load it into a register pair
    def load16_register(self, setter):
        value = self.read16_immediate()
        setter(value)
        return value

    # endregion
    # region Register Exchange

    def exchange_af(self):
        logger.debug(f"BEFORE EX AF: A={self.a:02X} ALT={self.a_alt:02X}")

        self.a, self.a_alt = (self.a_alt, self.a)

        self.flag_s, self.flag_s_alt = (self.flag_s_alt, self.flag_s)

        self.flag_z, self.flag_z_alt = (self.flag_z_alt, self.flag_z)

        self.flag_h, self.flag_h_alt = (self.flag_h_alt, self.flag_h)

        self.flag_pv, self.flag_pv_alt = (self.flag_pv_alt, self.flag_pv)

        self.flag_n, self.flag_n_alt = (self.flag_n_alt, self.flag_n)

        self.flag_c, self.flag_c_alt = (self.flag_c_alt, self.flag_c)

        logger.debug(f"AFTER EX AF: A={self.a:02X} ALT={self.a_alt:02X}")

    def exchange_bcdEhl(self):
        self.b, self.b_alt = self.b_alt, self.b
        self.c, self.c_alt = self.c_alt, self.c
        self.d, self.d_alt = self.d_alt, self.d
        self.e, self.e_alt = self.e_alt, self.e
        self.h, self.h_alt = self.h_alt, self.h
        self.l, self.l_alt = self.l_alt, self.l

    # endregion
    # region Gets/Sets

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
            (self.flag_s << 7)
            | (self.flag_z << 6)
            | (self.flag_h << 4)
            | (self.flag_pv << 2)
            | (self.flag_n << 1)
            | (self.flag_c)
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

    def set_ix(self, value):
        self.ix = value & 0xFFFF

    def set_iy(self, value):
        self.iy = value & 0xFFFF

    # endregion
    # region Interrupt Handling

    def interrupt(self):
        if not self.iff1:
            return

        logger.debug(f"INTERRUPT IM{self.interrupt_mode}")

        self.iff1 = False
        self.iff2 = False

        self.push16(self.pc)

        match self.interrupt_mode:
            case 0:
                logger.debug("IM0 interrupt")

            case 1:
                self.set_pc(0x0038)

            case 2:
                logger.debug("IM2 interrupt")

    # region IO

    def io_read_bc(self):
        return self.io.read(port=self.get_bc())

    def io_write_bc(self, value):
        self.io.write(port=self.get_bc(), value=value)

    # Helper for OUTI, OUTD, OTIR, and OTDR
    def block_out(self, increment, repeat):
        # Take the value from HL
        value = self.memory.read8(self.get_hl())

        # Write the byte pointed to by HL to BC
        self.io.write(port=self.get_bc(), value=value)

        # Decrement B
        self.b = (self.b - 1) & 0xFF

        # Advance or retreat HL by the increment
        self.set_hl((self.get_hl() + increment) & 0xFFFF)

        # TODO: Accurate flag behaviour

        # OTIR and OTDR repeat until B becomes zero
        if repeat and self.b != 0:
            self.set_pc(self.pc - 2)
            return 21

        return 16

    # endregion

    # endregion
    # region Stepping

    def step(self):
        opcode = self.memory.read8(self.pc)
        self.inc_pc(increment=1)

        opcode_t_states = dispatcher.execute(self, opcode)

        # Ensure that opcode_t_states is always valid and avoids divide by zero
        if opcode_t_states in (None, 0):
            opcode_t_states = 1

        # Process delayed EI behaviour
        if self.ei_pending:
            self.ei_pending = False

        elif self.interrupt_pending:
            # TODO: Restore interrupt behaviour after the VDP is implemented
            self.interrupt()
            self.interrupt_pending = False

        # Validate registers are within range
        if self.register_check:
            self.register_in_range_check(opcode)

        if self.opcode_trace != None:
            if self.pc == self.opcode_trace:
                print(
                    f"Entering {self.opcode_trace:02X}: "
                    f"BC={self.get_bc():04X} "
                    f"DE={self.get_de():04X} "
                    f"HL={self.get_hl():04X}"
                )

        # ----------
        # DEBUGGING

        # ----------

        # Heartbeat every N seconds to show CPU is alive
        self.heartbeat_counter += opcode_t_states

        if self.heartbeat_seconds != None and self.heartbeat_counter >= (
            self.clock_hz * self.heartbeat_seconds
        ):
            logger.info(
                f"\n"
                f"---------- CPU HEARTBEAT @ {datetime.datetime.now().strftime('%I:%M:%S %p')}\n"
                f"PC={self.pc:04X}\n"
                f"AF={self.get_af():02X} BC={self.get_bc():02X} DE={self.get_de():02X} HL={self.get_hl():02X}\n"
                f"OP={self.memory.read8(self.pc):02X}"
            )

            self.heartbeat_counter = 0

        time.sleep((1 / self.clock_hz) * opcode_t_states)

    # endregion
    # region Error Handling

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

    # endregion
    # region Register Assertion

    # Assert that all 8-bit CPU registers are within 8-bit range and raise if not
    def register_in_range_check(self, opcode):
        assert 0x00 <= self.a <= 0xFF, (
            f"Register A out of range (value is {self.a:#04X}), last opcode ended: {opcode:02X}"
        )
        assert 0x00 <= self.b <= 0xFF, (
            f"Register B out of range (value is {self.b:#04X}), last opcode ended: {opcode:02X}"
        )
        assert 0x00 <= self.c <= 0xFF, (
            f"Register C out of range (value is {self.c:#04X}), last opcode ended: {opcode:02X}"
        )
        assert 0x00 <= self.d <= 0xFF, (
            f"Register D out of range (value is {self.d:#04X}), last opcode ended: {opcode:02X}"
        )
        assert 0x00 <= self.e <= 0xFF, (
            f"Register E out of range (value is {self.e:#04X}), last opcode ended: {opcode:02X}"
        )
        assert 0x00 <= self.h <= 0xFF, (
            f"Register H out of range (value is {self.h:#04X}), last opcode ended: {opcode:02X}"
        )
        assert 0x00 <= self.l <= 0xFF, (
            f"Register L out of range (value is {self.l:#04X}), last opcode ended: {opcode:02X}"
        )

        assert 0x00 <= self.a_alt <= 0xFF, (
            f"Register A' out of range (value is {self.a_alt:#04X}), last opcode ended: {opcode:02X}"
        )
        assert 0x00 <= self.b_alt <= 0xFF, (
            f"Register B' out of range (value is {self.b_alt:#04X}), last opcode ended: {opcode:02X}"
        )
        assert 0x00 <= self.c_alt <= 0xFF, (
            f"Register C' out of range (value is {self.c_alt:#04X}), last opcode ended: {opcode:02X}"
        )
        assert 0x00 <= self.d_alt <= 0xFF, (
            f"Register D' out of range (value is {self.d_alt:#04X}), last opcode ended: {opcode:02X}"
        )
        assert 0x00 <= self.e_alt <= 0xFF, (
            f"Register E' out of range (value is {self.e_alt:#04X}), last opcode ended: {opcode:02X}"
        )
        assert 0x00 <= self.h_alt <= 0xFF, (
            f"Register H' out of range (value is {self.h_alt:#04X}), last opcode ended: {opcode:02X}"
        )
        assert 0x00 <= self.l_alt <= 0xFF, (
            f"Register L' out of range (value is {self.l_alt:#04X}), last opcode ended: {opcode:02X}"
        )

        assert 0x00 <= self.i <= 0xFF, (
            f"Register I out of range (value is {self.i:#04X}), last opcode ended: {opcode:02X}"
        )
        assert 0x00 <= self.r <= 0xFF, (
            f"Register R out of range (value is {self.r:#04X}), last opcode ended: {opcode:02X}"
        )

        assert 0x0000 <= self.pc <= 0xFFFF, (
            f"PC out of range ({self.pc:04X}), last opcode ended: {opcode:02X}"
        )

        assert 0x0000 <= self.sp <= 0xFFFF, (
            f"SP out of range ({self.sp:04X}), last opcode ended: {opcode:02X}"
        )

        assert 0x0000 <= self.ix <= 0xFFFF, (
            f"IX out of range ({self.ix:04X}), last opcode ended: {opcode:02X}"
        )

        assert 0x0000 <= self.iy <= 0xFFFF, (
            f"IY out of range ({self.iy:04X}), last opcode ended: {opcode:02X}"
        )

        return None

    # endregion
