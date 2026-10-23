OPCODES = [
    {"opcode": "0x00", "mnemonic": "NOP", "description": "No operation"},
    {
        "opcode": "0x76",
        "mnemonic": "HALT",
        "description": "Stop the CPU until an interrupt occurs",
    },
]


def _matches_opcode(opcode, entry):
    value = entry["opcode"]
    if "-" in value:
        start, end = value.split("-", 1)
        return int(start, 16) <= opcode <= int(end, 16)
    return opcode == int(value, 16)


# Opcode: 0x00
# Mnemonic: NOP
# Description: No operation


def _nop(self):
    return 4


# Opcode: 0x76
# Mnemonic: HALT
# Description: Stop the CPU until an interrupt occurs


def _halt(self):
    return None


def execute(self, opcode):
    for entry in OPCODES:
        if _matches_opcode(opcode, entry):
            if opcode == 0x00:
                return _nop(self)
            if opcode == 0x76:
                return _halt(self)

            raise NotImplementedError(
                f"{__name__}: {entry['opcode']} {entry['mnemonic']} ({entry['description']}) is not implemented"
            )

    raise NotImplementedError(
        f"{__name__}: opcode 0x{opcode:02X} is not defined in the control table"
    )
