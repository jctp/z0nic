OPCODES = [
    {"opcode": "0xC1", "mnemonic": "POP BC", "description": "Pop the top of the stack into BC"},
    {"opcode": "0xC5", "mnemonic": "PUSH BC", "description": "Push BC onto the stack"},
    {"opcode": "0xD1", "mnemonic": "POP DE", "description": "Pop the top of the stack into DE"},
    {"opcode": "0xD5", "mnemonic": "PUSH DE", "description": "Push DE onto the stack"},
    {"opcode": "0xE1", "mnemonic": "POP HL", "description": "Pop the top of the stack into HL"},
    {"opcode": "0xE5", "mnemonic": "PUSH HL", "description": "Push HL onto the stack"},
    {"opcode": "0xF1", "mnemonic": "POP AF", "description": "Pop the top of the stack into AF"},
    {"opcode": "0xF5", "mnemonic": "PUSH AF", "description": "Push AF onto the stack"},
]


def _matches_opcode(opcode, entry):
    value = entry["opcode"]
    if "-" in value:
        start, end = value.split("-", 1)
        return int(start, 16) <= opcode <= int(end, 16)
    return opcode == int(value, 16)


# Opcode: 0xC1
# Mnemonic: POP BC
# Description: Pop the top of the stack into BC

def _pop_bc(self):
    return None


# Opcode: 0xC5
# Mnemonic: PUSH BC
# Description: Push BC onto the stack

def _push_bc(self):
    return None


# Opcode: 0xD1
# Mnemonic: POP DE
# Description: Pop the top of the stack into DE

def _pop_de(self):
    return None


# Opcode: 0xD5
# Mnemonic: PUSH DE
# Description: Push DE onto the stack

def _push_de(self):
    return None


# Opcode: 0xE1
# Mnemonic: POP HL
# Description: Pop the top of the stack into HL

def _pop_hl(self):
    return None


# Opcode: 0xE5
# Mnemonic: PUSH HL
# Description: Push HL onto the stack

def _push_hl(self):
    return None


# Opcode: 0xF1
# Mnemonic: POP AF
# Description: Pop the top of the stack into AF

def _pop_af(self):
    return None


# Opcode: 0xF5
# Mnemonic: PUSH AF
# Description: Push AF onto the stack

def _push_af(self):
    return None


def execute(self, opcode):
    for entry in OPCODES:
        if _matches_opcode(opcode, entry):
            if opcode == 0xC1:
                return _pop_bc(self)
            if opcode == 0xC5:
                return _push_bc(self)
            if opcode == 0xD1:
                return _pop_de(self)
            if opcode == 0xD5:
                return _push_de(self)
            if opcode == 0xE1:
                return _pop_hl(self)
            if opcode == 0xE5:
                return _push_hl(self)
            if opcode == 0xF1:
                return _pop_af(self)
            if opcode == 0xF5:
                return _push_af(self)

            raise NotImplementedError(
                f"{__name__}: {entry['opcode']} {entry['mnemonic']} ({entry['description']}) is not implemented"
            )

    raise NotImplementedError(f"{__name__}: opcode 0x{opcode:02X} is not defined in the stack table")
