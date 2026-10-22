OPCODES = [
    {"opcode": "0xB8-0xBF", "mnemonic": "CP r", "description": "Compare A with the selected register"},
    {"opcode": "0xFE", "mnemonic": "CP n", "description": "Compare A with the immediate byte"},
]


def _matches_opcode(opcode, entry):
    value = entry["opcode"]
    if "-" in value:
        start, end = value.split("-", 1)
        return int(start, 16) <= opcode <= int(end, 16)
    return opcode == int(value, 16)


# Opcode: 0xB8-0xBF
# Mnemonic: CP r
# Description: Compare A with the selected register

def _cp_r(self):
    return None


# Opcode: 0xFE
# Mnemonic: CP n
# Description: Compare A with the immediate byte

def _cp_n(self):
    return None


def execute(self, opcode):
    for entry in OPCODES:
        if _matches_opcode(opcode, entry):
            if opcode in range(0xB8, 0xC0):
                return _cp_r(self)
            if opcode == 0xFE:
                return _cp_n(self)

            raise NotImplementedError(
                f"{__name__}: {entry['opcode']} {entry['mnemonic']} ({entry['description']}) is not implemented"
            )

    raise NotImplementedError(f"{__name__}: opcode 0x{opcode:02X} is not defined in the compare table")
