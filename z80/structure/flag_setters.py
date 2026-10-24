class FlagSetters:
    def set_subtraction_flags(self, lhs, rhs, result):
        # lhs - rhs, masked to 8 bits: the result determines Z/S/C/H/PV, with N set
        # because subtraction instructions always set the add/subtract flag.
        self.F.sign = (result & 0x80) != 0
        self.F.zero = result == 0
        self.F.add_sub = True
        self.F.carry = lhs < rhs
        self.F.half_carry = ((lhs ^ rhs ^ result) & 0x10) != 0
        self.F.parity_overflow = ((lhs ^ rhs) & 0x80) != 0 and (
            (lhs ^ result) & 0x80
        ) != 0

    def set_addition_flags(self, lhs, rhs, result, carry_in=0):
        # Adds lhs + rhs + carry_in, keeps the low byte as the machine result and
        # derives C/H from the 9-bit total to model the Z80's carry/half-carry rules.
        total = lhs + rhs + carry_in
        final = total & 0xFF
        self.F.sign = (final & 0x80) != 0
        self.F.zero = final == 0
        self.F.add_sub = False
        self.F.carry = total > 0xFF
        self.F.half_carry = ((lhs ^ rhs ^ final) & 0x10) != 0
        self.F.parity_overflow = ((lhs ^ final) & (rhs ^ final) & 0x80) != 0

    def set_logic_flags(self, value):
        # For AND/OR/XOR-like instructions, the byte is simply transformed by a logic
        # operation; the flags reflect the new byte's sign, zero, and parity bit pattern.
        self.F.sign = (value & 0x80) != 0
        self.F.zero = value == 0
        self.F.add_sub = False
        self.F.half_carry = False
        self.F.parity_overflow = value.bit_count() % 2 == 0

    def set_input_flags(self, value):
        # IN A,(n) loads a byte from I/O; it updates S/Z/PV like a normal data byte and
        # clears N/H because no arithmetic is being performed on the accumulator.
        self.F.sign = (value & 0x80) != 0
        self.F.zero = value == 0
        self.F.add_sub = False
        self.F.half_carry = False
        self.F.parity_overflow = value.bit_count() % 2 == 0

    def set_inc_dec_flags(self, before, after, is_dec=False):
        # INC/DEC updates Z/S/PV based on the new value while N reflects the operation
        # type; H is affected by the low nibble carry/borrow and C is unchanged.
        self.F.sign = (after & 0x80) != 0
        self.F.zero = after == 0
        self.F.add_sub = is_dec

        if is_dec:
            self.F.half_carry = (before & 0x0F) == 0
        else:
            self.F.half_carry = (((before & 0x0F) + 1) & 0x10) != 0

        # PV is set if the value was 0x7F before INC or 0x80 before DEC.
        if is_dec:
            self.F.parity_overflow = before == 0x80
        else:
            self.F.parity_overflow = before == 0x7F

    def set_add16_flags(self, lhs, rhs):
        total = lhs + rhs
        self.F.add_sub = False
        self.F.half_carry = (((lhs & 0x0FFF) + (rhs & 0x0FFF)) & 0x1000) != 0
        self.F.carry = total > 0xFFFF

    def set_sub16_flags(self, lhs, rhs):
        self.F.add_sub = True
        self.F.half_carry = (lhs & 0x0FFF) < (rhs & 0x0FFF)
        self.F.carry = lhs < rhs

    def set_bit_test_flags(self, value, bit):
        # BIT b,r checks whether the selected bit is zero; Z becomes the inverse of that
        # bit, H is set, N is reset, and the other flags keep their test semantics.
        self.F.zero = ((value >> bit) & 0x01) == 0
        self.F.sign = bit == 7 and (value & 0x80) != 0
        self.F.add_sub = False
        self.F.half_carry = True
        self.F.parity_overflow = self.F.zero

