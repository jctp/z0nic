OPCODES = [
    {"opcode": "0xA0", "mnemonic": "AND B", "description": "Logical AND A with B"},
    {"opcode": "0xA1", "mnemonic": "AND C", "description": "Logical AND A with C"},
    {"opcode": "0xA2", "mnemonic": "AND D", "description": "Logical AND A with D"},
    {"opcode": "0xA3", "mnemonic": "AND E", "description": "Logical AND A with E"},
    {"opcode": "0xA4", "mnemonic": "AND H", "description": "Logical AND A with H"},
    {"opcode": "0xA5", "mnemonic": "AND L", "description": "Logical AND A with L"},
    {"opcode": "0xA6", "mnemonic": "AND (HL)", "description": "Logical AND A with memory at HL"},
    {"opcode": "0xA7", "mnemonic": "AND A", "description": "Logical AND A with A"},
    {"opcode": "0xA8", "mnemonic": "XOR B", "description": "Logical XOR A with B"},
    {"opcode": "0xA9", "mnemonic": "XOR C", "description": "Logical XOR A with C"},
    {"opcode": "0xAA", "mnemonic": "XOR D", "description": "Logical XOR A with D"},
    {"opcode": "0xAB", "mnemonic": "XOR E", "description": "Logical XOR A with E"},
    {"opcode": "0xAC", "mnemonic": "XOR H", "description": "Logical XOR A with H"},
    {"opcode": "0xAD", "mnemonic": "XOR L", "description": "Logical XOR A with L"},
    {"opcode": "0xAE", "mnemonic": "XOR (HL)", "description": "Logical XOR A with memory at HL"},
    {"opcode": "0xAF", "mnemonic": "XOR A", "description": "Logical XOR A with itself"},
    {"opcode": "0xB0", "mnemonic": "OR B", "description": "Logical OR A with B"},
    {"opcode": "0xB1", "mnemonic": "OR C", "description": "Logical OR A with C"},
    {"opcode": "0xB2", "mnemonic": "OR D", "description": "Logical OR A with D"},
    {"opcode": "0xB3", "mnemonic": "OR E", "description": "Logical OR A with E"},
    {"opcode": "0xB4", "mnemonic": "OR H", "description": "Logical OR A with H"},
    {"opcode": "0xB5", "mnemonic": "OR L", "description": "Logical OR A with L"},
    {"opcode": "0xB6", "mnemonic": "OR (HL)", "description": "Logical OR A with memory at HL"},
    {"opcode": "0xB7", "mnemonic": "OR A", "description": "Logical OR A with A"},
    {"opcode": "0xE6", "mnemonic": "AND n", "description": "Logical AND A with the immediate byte"},
    {"opcode": "0xEE", "mnemonic": "XOR n", "description": "Logical XOR A with the immediate byte"},
    {"opcode": "0xF6", "mnemonic": "OR n", "description": "Logical OR A with the immediate byte"},
]


def _matches_opcode(opcode, entry):
    value = entry["opcode"]
    if "-" in value:
        start, end = value.split("-", 1)
        return int(start, 16) <= opcode <= int(end, 16)
    return opcode == int(value, 16)


# Opcode: 0xA0
# Mnemonic: AND B
# Description: Logical AND A with B

def _and_b(self):
    return None


# Opcode: 0xA1
# Mnemonic: AND C
# Description: Logical AND A with C

def _and_c(self):
    return None


# Opcode: 0xA2
# Mnemonic: AND D
# Description: Logical AND A with D

def _and_d(self):
    return None


# Opcode: 0xA3
# Mnemonic: AND E
# Description: Logical AND A with E

def _and_e(self):
    return None


# Opcode: 0xA4
# Mnemonic: AND H
# Description: Logical AND A with H

def _and_h(self):
    return None


# Opcode: 0xA5
# Mnemonic: AND L
# Description: Logical AND A with L

def _and_l(self):
    return None


# Opcode: 0xA6
# Mnemonic: AND (HL)
# Description: Logical AND A with memory at HL

def _and_hl(self):
    return None


# Opcode: 0xA7
# Mnemonic: AND A
# Description: Logical AND A with A

def _and_a(self):
    return None


# Opcode: 0xA8
# Mnemonic: XOR B
# Description: Logical XOR A with B

def _xor_b(self):
    return None


# Opcode: 0xA9
# Mnemonic: XOR C
# Description: Logical XOR A with C

def _xor_c(self):
    return None


# Opcode: 0xAA
# Mnemonic: XOR D
# Description: Logical XOR A with D

def _xor_d(self):
    return None


# Opcode: 0xAB
# Mnemonic: XOR E
# Description: Logical XOR A with E

def _xor_e(self):
    return None


# Opcode: 0xAC
# Mnemonic: XOR H
# Description: Logical XOR A with H

def _xor_h(self):
    return None


# Opcode: 0xAD
# Mnemonic: XOR L
# Description: Logical XOR A with L

def _xor_l(self):
    return None


# Opcode: 0xAE
# Mnemonic: XOR (HL)
# Description: Logical XOR A with memory at HL

def _xor_hl(self):
    return None


# Opcode: 0xAF
# Mnemonic: XOR A
# Description: Logical XOR A with itself

def _xor_a(self):
    return None


# Opcode: 0xB0
# Mnemonic: OR B
# Description: Logical OR A with B

def _or_b(self):
    return None


# Opcode: 0xB1
# Mnemonic: OR C
# Description: Logical OR A with C

def _or_c(self):
    return None


# Opcode: 0xB2
# Mnemonic: OR D
# Description: Logical OR A with D

def _or_d(self):
    return None


# Opcode: 0xB3
# Mnemonic: OR E
# Description: Logical OR A with E

def _or_e(self):
    return None


# Opcode: 0xB4
# Mnemonic: OR H
# Description: Logical OR A with H

def _or_h(self):
    return None


# Opcode: 0xB5
# Mnemonic: OR L
# Description: Logical OR A with L

def _or_l(self):
    return None


# Opcode: 0xB6
# Mnemonic: OR (HL)
# Description: Logical OR A with memory at HL

def _or_hl(self):
    return None


# Opcode: 0xB7
# Mnemonic: OR A
# Description: Logical OR A with A

def _or_a(self):
    return None


# Opcode: 0xE6
# Mnemonic: AND n
# Description: Logical AND A with the immediate byte

def _and_n(self):
    return None


# Opcode: 0xEE
# Mnemonic: XOR n
# Description: Logical XOR A with the immediate byte

def _xor_n(self):
    return None


# Opcode: 0xF6
# Mnemonic: OR n
# Description: Logical OR A with the immediate byte

def _or_n(self):
    return None


def execute(self, opcode):
    for entry in OPCODES:
        if _matches_opcode(opcode, entry):
            if opcode == 0xA0:
                return _and_b(self)
            if opcode == 0xA1:
                return _and_c(self)
            if opcode == 0xA2:
                return _and_d(self)
            if opcode == 0xA3:
                return _and_e(self)
            if opcode == 0xA4:
                return _and_h(self)
            if opcode == 0xA5:
                return _and_l(self)
            if opcode == 0xA6:
                return _and_hl(self)
            if opcode == 0xA7:
                return _and_a(self)
            if opcode == 0xA8:
                return _xor_b(self)
            if opcode == 0xA9:
                return _xor_c(self)
            if opcode == 0xAA:
                return _xor_d(self)
            if opcode == 0xAB:
                return _xor_e(self)
            if opcode == 0xAC:
                return _xor_h(self)
            if opcode == 0xAD:
                return _xor_l(self)
            if opcode == 0xAE:
                return _xor_hl(self)
            if opcode == 0xAF:
                return _xor_a(self)
            if opcode == 0xB0:
                return _or_b(self)
            if opcode == 0xB1:
                return _or_c(self)
            if opcode == 0xB2:
                return _or_d(self)
            if opcode == 0xB3:
                return _or_e(self)
            if opcode == 0xB4:
                return _or_h(self)
            if opcode == 0xB5:
                return _or_l(self)
            if opcode == 0xB6:
                return _or_hl(self)
            if opcode == 0xB7:
                return _or_a(self)
            if opcode == 0xE6:
                return _and_n(self)
            if opcode == 0xEE:
                return _xor_n(self)
            if opcode == 0xF6:
                return _or_n(self)

            raise NotImplementedError(
                f"{__name__}: {entry['opcode']} {entry['mnemonic']} ({entry['description']}) is not implemented"
            )

    raise NotImplementedError(f"{__name__}: opcode 0x{opcode:02X} is not defined in the logic table")
