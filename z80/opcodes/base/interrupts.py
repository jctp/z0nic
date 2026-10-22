OPCODES = [
    {"opcode": "0xF3", "mnemonic": "DI", "description": "Disable maskable interrupts"},
    {"opcode": "0xFB", "mnemonic": "EI", "description": "Enable maskable interrupts after the next instruction"},
]


def _matches_opcode(opcode, entry):
    value = entry["opcode"]
    if "-" in value:
        start, end = value.split("-", 1)
        return int(start, 16) <= opcode <= int(end, 16)
    return opcode == int(value, 16)


# Opcode: 0xF3
# Mnemonic: DI
# Description: Disable maskable interrupts

def _di(self):
    self.IFF1 = False
    self.IFF2 = False
    self.EI_delay = 0
    return 4

# Opcode: 0xFB
# Mnemonic: EI
# Description: Enable maskable interrupts after the next instruction

def _ei(self):
    self.EI_delay = 2
    return 4


def execute(self, opcode):
    for entry in OPCODES:
        if _matches_opcode(opcode, entry):
            if opcode == 0xF3:
                return _di(self)
            if opcode == 0xFB:
                return _ei(self)

            raise NotImplementedError(
                f"{__name__}: {entry['opcode']} {entry['mnemonic']} ({entry['description']}) is not implemented"
            )

    raise NotImplementedError(f"{__name__}: opcode 0x{opcode:02X} is not defined in the interrupt table")
