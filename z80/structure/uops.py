class UOps:
    # region Read uOps
    # Fetch the next opcode byte from ROM and validate that it is a valid 8-bit value.
    def read_byte(self):
        value = self.ingest_next_byte()
        self.byte_validity_check(value, "read_byte")
        return value

    # Fetch the next 16-bit immediate operand from ROM and validate it as a word.
    def read_word(self):
        value = self.ingest_next_word()
        self.word_validity_check(value, "read_word")
        return value

    # endregion
    # region Jump uOps

    # Set the program counter directly to a given absolute address.
    def jump_absolute(self, target):
        self.PC.set(target & 0xFFFF)

    # Add a signed relative displacement to the current PC to implement JR and DJNZ-style jumps.
    def jump_relative(self, offset):
        offset = self.signed_byte(offset)
        self.PC.set((self.PC.get() + offset) & 0xFFFF)

    # endregion
    # region Push uOps

    # Push one byte onto the stack and move the stack pointer downward.
    def push_byte(self, value):
        self.byte_validity_check(value, "push_byte")
        self.SP.dec()
        self.memory.write8(self.SP.get(), value)

    # Push a 16-bit value onto the stack in the standard Z80 order: high byte first.
    def push_word(self, value):
        self.word_validity_check(value, "push_word")
        self.push_byte((value >> 8) & 0xFF)
        self.push_byte(value & 0xFF)

    # endregion
    # region Pop uOps

    # Pop one byte from the stack and advance the stack pointer upward.
    def pop_byte(self):
        value = self.memory.read8(self.SP.get())
        self.byte_validity_check(value, "pop_byte")
        self.SP.inc()
        return value

    # Pop a 16-bit word from the stack using the same endian order used by PUSH.
    def pop_word(self):
        lo = self.pop_byte()
        hi = self.pop_byte()
        return ((hi << 8) | lo) & 0xFFFF

    # endregion
    # region Subroutine uOps

    # Save the return address and jump to a subroutine target.
    def call(self, target):
        self.word_validity_check(target, "call")
        self.push_word(self.PC.get())
        self.PC.set(target & 0xFFFF)

    # Return from a subroutine by restoring the saved PC from the stack.
    def ret(self):
        self.PC.set(self.pop_word())

    # endregion
    # region ALU Arithmetic uOps

    # Add two bytes and update the Z80 flags using the chosen carry input.
    def alu_add(self, lhs, rhs, carry_in=0):
        total = lhs + rhs + carry_in
        result = total & 0xFF
        self.set_addition_flags(lhs, rhs, result, carry_in)
        return result

    # Add two bytes with carry, matching the ADC instruction semantics.
    def alu_adc(self, lhs, rhs, carry_in=None):
        if carry_in is None:
            carry_in = int(self.F.carry)
        total = lhs + rhs + carry_in
        result = total & 0xFF
        self.set_addition_flags(lhs, rhs, result, carry_in)
        return result

    # Subtract one byte from another and set subtraction flags without changing operands.
    def alu_sub(self, lhs, rhs):
        result = (lhs - rhs) & 0xFF
        self.set_subtraction_flags(lhs, rhs, result)
        return result

    # Subtract with borrow, mirroring the Z80 SBC instruction behavior.
    def alu_sbc(self, lhs, rhs, carry_in=None):
        if carry_in is None:
            carry_in = int(self.F.carry)
        total = lhs - rhs - carry_in
        result = total & 0xFF
        self.F.sign = (result & 0x80) != 0
        self.F.zero = result == 0
        self.F.add_sub = True
        self.F.carry = total < 0
        self.F.half_carry = ((lhs & 0x0F) - (rhs & 0x0F) - carry_in) < 0
        self.F.parity_overflow = ((lhs ^ rhs) & (lhs ^ result) & 0x80) != 0
        return result

    # Compare one byte against another without storing the result in the accumulator.
    def alu_cp(self, lhs, rhs):
        result = (lhs - rhs) & 0xFF
        self.set_subtraction_flags(lhs, rhs, result)
        return result

    # Increment a byte value and update the INC flag state.
    def alu_inc(self, value):
        self.byte_validity_check(value, "alu_inc")
        before = value & 0xFF
        after = (before + 1) & 0xFF
        self.set_inc_dec_flags(before, after, is_dec=False)
        return after

    # Decrement a byte value and update the DEC flag state.
    def alu_dec(self, value):
        self.byte_validity_check(value, "alu_dec")
        before = value & 0xFF
        after = (before - 1) & 0xFF
        self.set_inc_dec_flags(before, after, is_dec=True)
        return after

    # endregion
    # region 16-bit Arithmetic

    # Add two 16-bit values and update the carry/half-carry flags for register-pair operations.
    def add16(self, a, b):
        result = (a + b) & 0xFFFF
        self.set_add16_flags(a, b)
        return result

    # Subtract two 16-bit values and update the subtraction-related flags.
    def sub16(self, a, b):
        result = (a - b) & 0xFFFF
        self.set_sub16_flags(a, b)
        return result

    # endregion
    # region ALU Logic uOps

    # Perform a bitwise AND and set the logic flags based on the result.
    def alu_and(self, lhs, rhs):
        result = lhs & rhs
        self.set_logic_flags(result)
        self.F.half_carry = True
        return result & 0xFF

    # Perform a bitwise OR and set the logic flags based on the result.
    def alu_or(self, lhs, rhs):
        result = lhs | rhs
        self.set_logic_flags(result)
        return result & 0xFF

    # Perform a bitwise XOR and set the logic flags based on the result.
    def alu_xor(self, lhs, rhs):
        result = lhs ^ rhs
        self.set_logic_flags(result)
        return result & 0xFF

    # endregion
    # region Bitwise uOps

    # Test a specific bit in a byte without modifying the source value.
    def bit(self, bit, value):
        self.byte_validity_check(value, "bit")
        if not 0 <= bit <= 7:
            raise ValueError(f"bit {bit} is not valid: bit operation")
        self.set_bit_test_flags(value, bit)

    # Set a single bit within a byte and return the modified value.
    def set_(self, bit, value):
        self.byte_validity_check(value, "set_")
        if not 0 <= bit <= 7:
            raise ValueError(f"bit {bit} is not valid: set_")
        value |= 1 << bit
        return value & 0xFF

    # Clear a single bit within a byte and return the modified value.
    def res(self, bit, value):
        self.byte_validity_check(value, "res")
        if not 0 <= bit <= 7:
            raise ValueError(f"bit {bit} is not valid: res")
        value &= ~(1 << bit)
        return value & 0xFF

    # endregion
    # region Shift/Rotate uOps

    # Rotate left through carry, moving the MSB back into the LSB and the old carry into the LSB.
    def rlc(self, value):
        self.byte_validity_check(value, "rlc")
        carry = (value >> 7) & 1
        result = ((value << 1) | carry) & 0xFF
        self.F.carry = bool(carry)
        self.set_logic_flags(result)
        return result

    # Rotate right through carry, moving the LSB back into the MSB and the old carry into the MSB.
    def rrc(self, value):
        self.byte_validity_check(value, "rrc")
        carry = value & 1
        result = ((value >> 1) | (carry << 7)) & 0xFF
        self.F.carry = bool(carry)
        self.set_logic_flags(result)
        return result

    # Rotate left through carry using the current carry flag as the new bit 0 value.
    def rl(self, value):
        self.byte_validity_check(value, "rl")
        carry_out = (value >> 7) & 1
        result = ((value << 1) | int(self.F.carry)) & 0xFF
        self.F.carry = bool(carry_out)
        self.set_logic_flags(result)
        return result

    # Rotate right through carry using the current carry flag as the new bit 7 value.
    def rr(self, value):
        self.byte_validity_check(value, "rr")
        carry_out = value & 1
        result = ((value >> 1) | (int(self.F.carry) << 7)) & 0xFF
        self.F.carry = bool(carry_out)
        self.set_logic_flags(result)
        return result

    # Arithmetic left shift, shifting bits left and placing the previous MSB into carry.
    def sla(self, value):
        self.byte_validity_check(value, "sla")
        carry = (value >> 7) & 1
        result = (value << 1) & 0xFF
        self.F.carry = bool(carry)
        self.set_logic_flags(result)
        return result

    # Arithmetic right shift preserves the sign bit while moving data right.
    def sra(self, value):
        self.byte_validity_check(value, "sra")
        carry = value & 1
        result = ((value >> 1) | (value & 0x80)) & 0xFF
        self.F.carry = bool(carry)
        self.set_logic_flags(result)
        return result

    # Logical right shift clears the top bit while moving bits toward the low end.
    def srl(self, value):
        self.byte_validity_check(value, "srl")
        carry = value & 1
        result = (value >> 1) & 0xFF
        self.F.carry = bool(carry)
        self.set_logic_flags(result)
        return result

    # endregion
    # region Repeat uOps

    # Advance the memory pointers for an incrementing block transfer and continue while BC remains non-zero.
    def inc_repeat(self):
        self.HL.inc()
        self.DE.inc()
        self.BC.dec()
        return self.BC.get() != 0

    # Advance the memory pointers for a decrementing block transfer and continue while BC remains non-zero.
    def dec_repeat(self):
        self.HL.dec()
        self.DE.dec()
        self.BC.dec()
        return self.BC.get() != 0

    # endregion
    # region Extended ED-family uOps

    # Add the selected register pair to HL with carry, mirroring the ED-prefixed ADC HL,ss instruction.
    def adc_hl_ss(self, ss_value):
        self.word_validity_check(ss_value, "adc_hl_ss")
        hl = self.HL.get()
        carry_in = int(self.F.carry)
        total = hl + ss_value + carry_in
        result = total & 0xFFFF
        self.F.carry = total > 0xFFFF
        self.F.half_carry = ((hl & 0x0FFF) + (ss_value & 0x0FFF) + carry_in) > 0x0FFF
        self.F.add_sub = False
        self.F.zero = result == 0
        self.F.sign = (result & 0x8000) != 0
        self.F.parity_overflow = ((hl ^ result) & (ss_value ^ result) & 0x8000) != 0
        self.HL.set(result)
        return result

    # Subtract the selected register pair from HL with borrow, mirroring the ED-prefixed SBC HL,ss instruction.
    def sbc_hl_ss(self, ss_value):
        self.word_validity_check(ss_value, "sbc_hl_ss")
        hl = self.HL.get()
        carry_in = int(self.F.carry)
        total = hl - ss_value - carry_in
        result = total & 0xFFFF
        self.F.carry = total < 0
        self.F.half_carry = ((hl & 0x0FFF) - (ss_value & 0x0FFF) - carry_in) < 0
        self.F.add_sub = True
        self.F.zero = result == 0
        self.F.sign = (result & 0x8000) != 0
        self.F.parity_overflow = ((hl ^ ss_value) & (hl ^ result) & 0x8000) != 0
        self.HL.set(result)
        return result

    # Negate the accumulator value using two's-complement arithmetic and update the arithmetic flags.
    def neg_acc(self):
        value = self.A.get()
        result = (-value) & 0xFF
        self.set_subtraction_flags(0, value, result)
        self.A.set(result)
        return result

    # Set the interrupt mode register to the selected Z80 operating mode.
    def im_mode(self, mode):
        if mode not in (0, 1, 2):
            raise ValueError(f"unsupported interrupt mode: {mode}")
        self.IM = mode
        return mode

    # Load the I or R register from the accumulator.
    def load_reg_from_a(self, reg_name):
        if reg_name not in ("I", "R"):
            raise ValueError(f"unsupported register for LD {reg_name},A: {reg_name}")
        getattr(self, reg_name).set(self.A.get())
        return self.A.get()

    # Load the accumulator from the I or R register and update the affected flags.
    def load_a_from_reg(self, reg_name):
        if reg_name not in ("I", "R"):
            raise ValueError(f"unsupported register for LD A,{reg_name}: {reg_name}")
        value = getattr(self, reg_name).get()
        self.A.set(value)
        self.set_input_flags(value)
        return value

    # Read a byte from the selected I/O port and return its value.
    def port_in(self, port):
        self.word_validity_check(port, "port_in")
        value = self.io.read(port & 0xFF)
        self.byte_validity_check(value, "port_in")
        return value

    # Write a byte value to the selected I/O port.
    def port_out(self, port, value):
        self.word_validity_check(port, "port_out")
        self.byte_validity_check(value, "port_out")
        self.io.write(port & 0xFF, value)
        return value

    # Perform the RRD instruction: rotate the lower nibble of memory and the accumulator across a byte boundary.
    def rrd(self):
        a = self.A.get()
        value = self.memory.read8(self.HL.get())
        result_mem = ((value >> 4) | ((a & 0x0F) << 4)) & 0xFF
        result_a = ((a & 0xF0) | (value & 0x0F)) & 0xFF
        self.memory.write8(self.HL.get(), result_mem)
        self.A.set(result_a)
        self.set_input_flags(result_a)
        self.F.add_sub = False
        self.F.half_carry = False
        return result_a

    # Perform the RLD instruction: rotate the upper nibble of memory and the accumulator across a byte boundary.
    def rld(self):
        a = self.A.get()
        value = self.memory.read8(self.HL.get())
        result_mem = ((value << 4) | (a & 0x0F)) & 0xFF
        result_a = ((a & 0xF0) | (value >> 4)) & 0xFF
        self.memory.write8(self.HL.get(), result_mem)
        self.A.set(result_a)
        self.set_input_flags(result_a)
        self.F.add_sub = False
        self.F.half_carry = False
        return result_a

    # Transfer a byte from memory to DE, advancing both pointers and continuing while BC is non-zero.
    def block_load(self, direction=1):
        value = self.memory.read8(self.HL.get())
        self.memory.write8(self.DE.get(), value)
        self.HL.set((self.HL.get() + direction) & 0xFFFF)
        self.DE.set((self.DE.get() + direction) & 0xFFFF)
        self.BC.dec()
        return self.BC.get() != 0

    # Compare memory against the accumulator while advancing the HL pointer and decrementing BC.
    def block_compare(self, direction=1):
        value = self.memory.read8(self.HL.get())
        self.alu_cp(self.A.get(), value)
        self.HL.set((self.HL.get() + direction) & 0xFFFF)
        self.BC.dec()
        return self.BC.get() != 0

    # Input a byte from the port in BC into memory at HL and continue while the remaining block count persists.
    def block_input(self, direction=1):
        port = self.BC.get() & 0xFFFF
        value = self.port_in(port)
        self.memory.write8(self.HL.get(), value)
        self.HL.set((self.HL.get() + direction) & 0xFFFF)
        self.B.set((self.B.get() - 1) & 0xFF)
        return self.B.get() != 0

    # Output a byte from memory at HL to the port in BC and continue while the block count remains non-zero.
    def block_output(self, direction=1):
        value = self.memory.read8(self.HL.get())
        self.port_out(self.BC.get() & 0xFFFF, value)
        self.HL.set((self.HL.get() + direction) & 0xFFFF)
        self.B.set((self.B.get() - 1) & 0xFF)
        return self.B.get() != 0

    # endregion
    # region Byte Handling

    def byte_validity_check(self, byte, error_message):
        if 0 <= byte <= 255:
            return
        else:
            raise ValueError(f"{byte:02X} is not a valid byte (octet): {error_message}")

    def word_validity_check(self, word, error_message):
        if 0 <= word <= 65535:
            return
        else:
            raise ValueError(f"{word:04X} is not a valid word: {error_message}")

    def signed_byte(self, value):
        if value & 0x80:
            return value - 0x100
        return value

    def ingest_next_byte(self):
        next_byte = self.memory.read8(self.PC.get())
        self.PC.inc()
        return next_byte

    def construct_word(self, lo_byte, hi_byte):
        self.byte_validity_check(lo_byte, "Word constructor lo byte")
        self.byte_validity_check(hi_byte, "Word constructor hi byte")
        word = ((hi_byte << 8) | lo_byte) & 0xFFFF
        return word

    def split_word(self, word):
        hi_byte = (word >> 8) & 0xFF
        lo_byte = word & 0xFF
        self.byte_validity_check(hi_byte, "Word splitter hi byte")
        self.byte_validity_check(lo_byte, "Word splitter lo byte")
        return hi_byte, lo_byte

    def ingest_next_word(self):
        lo_byte = self.ingest_next_byte()
        hi_byte = self.ingest_next_byte()
        return self.construct_word(lo_byte, hi_byte)

    # endregion
