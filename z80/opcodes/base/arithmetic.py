OPCODES = [
    {"opcode": "0x03", "mnemonic": "INC BC", "description": "Increment BC"},
    {"opcode": "0x04-0x07", "mnemonic": "INC r", "description": "Increment register r"},
    {"opcode": "0x09", "mnemonic": "ADD HL,BC", "description": "Add BC to HL"},
    {"opcode": "0x0B", "mnemonic": "DEC BC", "description": "Decrement BC"},
    {
        "opcode": "0x0C-0x0F",
        "mnemonic": "INC/DEC r",
        "description": "Increment or decrement the selected register",
    },
    {"opcode": "0x13", "mnemonic": "INC DE", "description": "Increment DE"},
    {"opcode": "0x14-0x17", "mnemonic": "INC r", "description": "Increment register r"},
    {"opcode": "0x19", "mnemonic": "ADD HL,DE", "description": "Add DE to HL"},
    {"opcode": "0x1B", "mnemonic": "DEC DE", "description": "Decrement DE"},
    {
        "opcode": "0x1C-0x1F",
        "mnemonic": "INC/DEC r",
        "description": "Increment or decrement the selected register",
    },
    {"opcode": "0x23", "mnemonic": "INC HL", "description": "Increment HL"},
    {"opcode": "0x24-0x27", "mnemonic": "INC r", "description": "Increment register r"},
    {"opcode": "0x29", "mnemonic": "ADD HL,HL", "description": "Add HL to HL"},
    {"opcode": "0x2B", "mnemonic": "DEC HL", "description": "Decrement HL"},
    {
        "opcode": "0x2C-0x2F",
        "mnemonic": "INC/DEC r",
        "description": "Increment or decrement the selected register",
    },
    {"opcode": "0x33", "mnemonic": "INC SP", "description": "Increment SP"},
    {
        "opcode": "0x34",
        "mnemonic": "INC (HL)",
        "description": "Increment the byte at address HL",
    },
    {
        "opcode": "0x35",
        "mnemonic": "DEC (HL)",
        "description": "Decrement the byte at address HL",
    },
    {"opcode": "0x39", "mnemonic": "ADD HL,SP", "description": "Add SP to HL"},
    {"opcode": "0x3B", "mnemonic": "DEC SP", "description": "Decrement SP"},
    {
        "opcode": "0x3C-0x3F",
        "mnemonic": "INC/DEC r",
        "description": "Increment or decrement the selected register",
    },
    {
        "opcode": "0x80-0x87",
        "mnemonic": "ADD A,r",
        "description": "Add the selected register to A",
    },
    {
        "opcode": "0x88-0x8F",
        "mnemonic": "ADC A,r",
        "description": "Add the selected register and carry to A",
    },
    {
        "opcode": "0x90-0x97",
        "mnemonic": "SUB r",
        "description": "Subtract the selected register from A",
    },
    {
        "opcode": "0x98-0x9F",
        "mnemonic": "SBC A,r",
        "description": "Subtract the selected register and carry from A",
    },
    {"opcode": "0xC6", "mnemonic": "ADD A,n", "description": "Add immediate byte to A"},
    {
        "opcode": "0xCE",
        "mnemonic": "ADC A,n",
        "description": "Add immediate byte and carry to A",
    },
    {
        "opcode": "0xD6",
        "mnemonic": "SUB n",
        "description": "Subtract immediate byte from A",
    },
    {
        "opcode": "0xDE",
        "mnemonic": "SBC A,n",
        "description": "Subtract immediate byte and carry from A",
    },
]


def _matches_opcode(opcode, entry):
    value = entry["opcode"]
    if "-" in value:
        start, end = value.split("-", 1)
        return int(start, 16) <= opcode <= int(end, 16)
    return opcode == int(value, 16)


# Opcode: 0x03
# Mnemonic: INC BC
# Description: Increment BC


def _inc_bc(self):
    self.BC.inc()
    return 4


# Opcode: 0x04-0x07
# Mnemonic: INC r
# Description: Increment register r


def _inc_r(self):
    return None


# Opcode: 0x09
# Mnemonic: ADD HL,BC
# Description: Add BC to HL


def _add_hl_bc(self):
    return None


# Opcode: 0x0B
# Mnemonic: DEC BC
# Description: Decrement BC


def _dec_bc(self):
    self.BC.dec()
    return 4


# Opcode: 0x0C-0x0F
# Mnemonic: INC/DEC r
# Description: Increment or decrement the selected register


def _inc_dec_r(self):
    return None


# Opcode: 0x13
# Mnemonic: INC DE
# Description: Increment DE


def _inc_de(self):
    self.DE.inc(1)
    return 4


# Opcode: 0x14-0x17
# Mnemonic: INC r
# Description: Increment register r


def _inc_r_alt(self):
    return None


# Opcode: 0x19
# Mnemonic: ADD HL,DE
# Description: Add DE to HL


def _add_hl_de(self):
    return None


# Opcode: 0x1B
# Mnemonic: DEC DE
# Description: Decrement DE


def _dec_de(self):
    self.DE.dec()
    return 4


# Opcode: 0x1C-0x1F
# Mnemonic: INC/DEC r
# Description: Increment or decrement the selected register


def _inc_dec_r_alt(self):
    return None


# Opcode: 0x23
# Mnemonic: INC HL
# Description: Increment HL


def _inc_hl(self):
    self.HL.inc(1)
    return 4


# Opcode: 0x24-0x27
# Mnemonic: INC r
# Description: Increment register r


def _inc_r_alt_2(self):
    return None


# Opcode: 0x29
# Mnemonic: ADD HL,HL
# Description: Add HL to HL


def _add_hl_hl(self):
    return None


# Opcode: 0x2B
# Mnemonic: DEC HL
# Description: Decrement HL


def _dec_hl(self):
    self.HL.dec(1)
    return 4


# Opcode: 0x2C-0x2F
# Mnemonic: INC/DEC r
# Description: Increment or decrement the selected register


def _inc_dec_r_alt_2(self):
    return None


# Opcode: 0x33
# Mnemonic: INC SP
# Description: Increment SP


def _inc_sp(self):
    self.SP.inc()
    return 4


# Opcode: 0x34
# Mnemonic: INC (HL)
# Description: Increment the byte at address HL


def _inc_hl_mem(self):
    return None


# Opcode: 0x35
# Mnemonic: DEC (HL)
# Description: Decrement the byte at address HL


def _dec_hl_mem(self):
    return None


# Opcode: 0x39
# Mnemonic: ADD HL,SP
# Description: Add SP to HL


def _add_hl_sp(self):
    return None


# Opcode: 0x3B
# Mnemonic: DEC SP
# Description: Decrement SP


def _dec_sp(self):
    self.SP.dec(1)
    return 4


# Opcode: 0x3C-0x3F
# Mnemonic: INC/DEC r
# Description: Increment or decrement the selected register


def _inc_dec_r_alt_3(self):
    return None


# Opcode: 0x80-0x87
# Mnemonic: ADD A,r
# Description: Add the selected register to A


def _add_a_r(self):
    return None


# Opcode: 0x88-0x8F
# Mnemonic: ADC A,r
# Description: Add the selected register and carry to A


def _adc_a_r(self):
    return None


# Opcode: 0x90-0x97
# Mnemonic: SUB r
# Description: Subtract the selected register from A


def _sub_r(self, opcode):
    lhs = self.A.get()
    rhs = self.read_from_opcode_r(opcode)
    result = self.alu_sub(lhs, rhs)

    self.A.set(result)
    return 4


# Opcode: 0x98-0x9F
# Mnemonic: SBC A,r
# Description: Subtract the selected register and carry from A


def _sbc_a_r(self):
    return None


# Opcode: 0xC6
# Mnemonic: ADD A,n
# Description: Add immediate byte to A


def _add_a_n(self):
    return None


# Opcode: 0xCE
# Mnemonic: ADC A,n
# Description: Add immediate byte and carry to A


def _adc_a_n(self):
    return None


# Opcode: 0xD6
# Mnemonic: SUB n
# Description: Subtract immediate byte from A


def _sub_n(self):
    return None


# Opcode: 0xDE
# Mnemonic: SBC A,n
# Description: Subtract immediate byte and carry from A


def _sbc_a_n(self):
    return None


def execute(self, opcode):
    for entry in OPCODES:
        if _matches_opcode(opcode, entry):
            if opcode == 0x03:
                return _inc_bc(self)
            if opcode == 0x13:
                return _inc_de(self)
            if opcode == 0x23:
                return _inc_hl(self)
            if opcode == 0x33:
                return _inc_sp(self)
            if opcode in (0x04, 0x0C, 0x14, 0x1C, 0x24, 0x2C, 0x34, 0x3C):
                return _inc_r(self)
            if opcode == 0x09:
                return _add_hl_bc(self)
            if opcode == 0x0B:
                return _dec_bc(self)
            if opcode == 0x1B:
                return _dec_de(self)
            if opcode == 0x2B:
                return _dec_hl(self)
            if opcode == 0x3B:
                return _dec_sp(self)
            if opcode == 0x19:
                return _add_hl_de(self)
            if opcode == 0x29:
                return _add_hl_hl(self)
            if opcode == 0x39:
                return _add_hl_sp(self)
            if opcode == 0x34:
                return _inc_hl_mem(self)
            if opcode == 0x35:
                return _dec_hl_mem(self)
            if opcode in range(0x80, 0x88):
                return _add_a_r(self)
            if opcode in range(0x88, 0x90):
                return _adc_a_r(self)
            if opcode in range(0x90, 0x98):
                return _sub_r(self, opcode)
            if opcode in range(0x98, 0xA0):
                return _sbc_a_r(self)
            if opcode == 0xC6:
                return _add_a_n(self)
            if opcode == 0xCE:
                return _adc_a_n(self)
            if opcode == 0xD6:
                return _sub_n(self)
            if opcode == 0xDE:
                return _sbc_a_n(self)

            raise NotImplementedError(
                f"{__name__}: {entry['opcode']} {entry['mnemonic']} ({entry['description']}) is not implemented"
            )

    raise NotImplementedError(
        f"{__name__}: opcode 0x{opcode:02X} is not defined in the arithmetic table"
    )
