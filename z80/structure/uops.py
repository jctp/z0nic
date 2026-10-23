class UOps:
    # region Read uOps
    def read_byte(self):
        pass

    def read_word(self):
        pass

    # endregion
    # region Jump uOps

    def jump_absolute(self, target):
        self.PC.set(target & 0xFFFF)

    def jump_relative(self, offset):
        offset = self.signed_byte(offset)
        self.PC.set((self.PC.get() + offset) & 0xFFFF)

    # endregion
    # region Push uOps

    def push_byte(self):
        pass

    def push_word(self):
        pass

    # endregion
    # region Pop uOps

    def pop_byte(self):
        pass

    def pop_word(self):
        pass

    # endregion
    # region Subroutine uOps

    def call(self):
        pass

    def ret(self):
        pass

    # endregion
    # region ALU Arithmetic uOps

    def alu_add(self):
        pass

    def alu_adc(self):
        pass

    def alu_sub(self):
        pass

    def alu_sbc(self):
        pass

    def alu_cp(self):
        pass

    # endregion
    # region ALU Logic uOps

    def alu_and(self):
        pass

    def alu_or(self):
        pass

    def alu_xor(self):
        pass

    # endregion
    # region Bitwise uOps

    def bit(self):
        pass

    def set_(self):
        pass

    def res(self):
        pass

    # endregion
    # region Shift/Rotate uOps

    def rlc(self):
        pass

    def rrc(self):
        pass

    def rl(self):
        pass

    def rr(self):
        pass

    def sla(self):
        pass

    def sra(self):
        pass

    def srl(self):
        pass

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
