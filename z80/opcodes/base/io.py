OPCODES = [
    {"opcode": "0xD3", "mnemonic": "OUT (n),A", "description": "Write A to the I/O port at the immediate address"},
    {"opcode": "0xDB", "mnemonic": "IN A,(n)", "description": "Read the I/O port at the immediate address into A"},
]


def _matches_opcode(opcode, entry):
    value = entry["opcode"]
    if "-" in value:
        start, end = value.split("-", 1)
        return int(start, 16) <= opcode <= int(end, 16)
    return opcode == int(value, 16)


# Opcode: 0xD3
# Mnemonic: OUT (n),A
# Description: Write A to the I/O port at the immediate address

def _out_n_a(self):
    return None


# Opcode: 0xDB
# Mnemonic: IN A,(n)
# Description: Read a byte from I/O port n into A

def _in_a_n(self):

    port_lo = self.ingest_next_byte()
    port = self.construct_word(port_lo, self.A.get())
    value = self.io.read(port)
    self.A.set(value)

    return 11


def execute(self, opcode):
    for entry in OPCODES:
        if _matches_opcode(opcode, entry):
            if opcode == 0xD3:
                return _out_n_a(self)
            if opcode == 0xDB:
                return _in_a_n(self)

            raise NotImplementedError(
                f"{__name__}: {entry['opcode']} {entry['mnemonic']} ({entry['description']}) is not implemented"
            )

    raise NotImplementedError(f"{__name__}: opcode 0x{opcode:02X} is not defined in the I/O table")
