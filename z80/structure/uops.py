class UOps:
    # region Read uOps
    def read_byte(self):
        value = self.ingest_next_byte()
        self.byte_validity_check(value, "read_byte")
        return value

    def read_word(self):
        value = self.ingest_next_word()
        self.word_validity_check(value, "read_word")
        return value

    # endregion
    # region Jump uOps

    def jump_absolute(self, target):
        self.PC.set(target & 0xFFFF)

    def jump_relative(self, offset):
        offset = self.signed_byte(offset)
        self.PC.set((self.PC.get() + offset) & 0xFFFF)

    # endregion
    # region Push uOps

    def push_byte(self, value):
        self.byte_validity_check(value, "push_byte")
        self.SP.dec()
        self.memory.write8(self.SP.get(), value)

    def push_word(self, value):
        self.word_validity_check(value, "push_word")
        self.push_byte((value >> 8) & 0xFF)
        self.push_byte(value & 0xFF)

    # endregion
    # region Pop uOps

    def pop_byte(self):
        value = self.memory.read8(self.SP.get())
        self.byte_validity_check(value, "pop_byte")
        self.SP.inc()
        return value

    def pop_word(self):
        lo = self.pop_byte()
        hi = self.pop_byte()
        return ((hi << 8) | lo) & 0xFFFF

    # endregion
    # region Subroutine uOps

    def call(self, target):
        self.word_validity_check(target, "call")
        self.push_word(self.PC.get())
        self.PC.set(target & 0xFFFF)

    def ret(self):
        self.PC.set(self.pop_word())

    # endregion
    # region ALU Arithmetic uOps

    def alu_add(self, lhs, rhs, carry_in=0):
        total = lhs + rhs + carry_in
        result = total & 0xFF
        self.set_addition_flags(lhs, rhs, result, carry_in)
        return result

    def alu_adc(self, lhs, rhs, carry_in=None):
        if carry_in is None:
            carry_in = int(self.F.carry)
        total = lhs + rhs + carry_in
        result = total & 0xFF
        self.set_addition_flags(lhs, rhs, result, carry_in)
        return result

    def alu_sub(self, lhs, rhs):
        result = (lhs - rhs) & 0xFF
        self.set_subtraction_flags(lhs, rhs, result)
        return result

    def alu_sbc(self, lhs, rhs, carry_in=None):
        if carry_in is None:
            carry_in = int(self.F.carry)
        rhs_total = (rhs + carry_in) & 0xFF
        result = (lhs - rhs_total) & 0xFF
        self.set_subtraction_flags(lhs, rhs_total, result)
        return result

    def alu_cp(self, lhs, rhs):
        result = (lhs - rhs) & 0xFF
        self.set_subtraction_flags(lhs, rhs, result)
        return result

    # endregion
    # region ALU Logic uOps

    def alu_and(self, lhs, rhs):
        result = lhs & rhs
        self.set_logic_flags(result)
        return result & 0xFF

    def alu_or(self, lhs, rhs):
        result = lhs | rhs
        self.set_logic_flags(result)
        return result & 0xFF

    def alu_xor(self, lhs, rhs):
        result = lhs ^ rhs
        self.set_logic_flags(result)
        return result & 0xFF

    # endregion
    # region Bitwise uOps

    def bit(self, bit, value):
        self.byte_validity_check(value, "bit")
        if not 0 <= bit <= 7:
            raise ValueError(f"bit {bit} is not valid: bit operation")
        self.set_bit_test_flags(value, bit)

    def set_(self, bit, value):
        self.byte_validity_check(value, "set_")
        if not 0 <= bit <= 7:
            raise ValueError(f"bit {bit} is not valid: set_")
        value |= (1 << bit)
        return value & 0xFF

    def res(self, bit, value):
        self.byte_validity_check(value, "res")
        if not 0 <= bit <= 7:
            raise ValueError(f"bit {bit} is not valid: res")
        value &= ~(1 << bit)
        return value & 0xFF

    # endregion
    # region Shift/Rotate uOps

    def rlc(self, value):
        self.byte_validity_check(value, "rlc")
        carry = (value >> 7) & 1
        result = ((value << 1) | carry) & 0xFF
        self.F.carry = bool(carry)
        self.set_logic_flags(result)
        return result

    def rrc(self, value):
        self.byte_validity_check(value, "rrc")
        carry = value & 1
        result = ((value >> 1) | (carry << 7)) & 0xFF
        self.F.carry = bool(carry)
        self.set_logic_flags(result)
        return result

    def rl(self, value):
        self.byte_validity_check(value, "rl")
        carry_out = (value >> 7) & 1
        result = ((value << 1) | int(self.F.carry)) & 0xFF
        self.F.carry = bool(carry_out)
        self.set_logic_flags(result)
        return result

    def rr(self, value):
        self.byte_validity_check(value, "rr")
        carry_out = value & 1
        result = ((value >> 1) | (int(self.F.carry) << 7)) & 0xFF
        self.F.carry = bool(carry_out)
        self.set_logic_flags(result)
        return result

    def sla(self, value):
        self.byte_validity_check(value, "sla")
        carry = (value >> 7) & 1
        result = (value << 1) & 0xFF
        self.F.carry = bool(carry)
        self.set_logic_flags(result)
        return result

    def sra(self, value):
        self.byte_validity_check(value, "sra")
        carry = value & 1
        result = ((value >> 1) | (value & 0x80)) & 0xFF
        self.F.carry = bool(carry)
        self.set_logic_flags(result)
        return result

    def srl(self, value):
        self.byte_validity_check(value, "srl")
        carry = value & 1
        result = (value >> 1) & 0xFF
        self.F.carry = bool(carry)
        self.set_logic_flags(result)
        return result

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
