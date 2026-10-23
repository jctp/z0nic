OPCODES = [
    {
        "opcode": "0x10",
        "mnemonic": "DJNZ e",
        "description": "Decrement B and jump relative if B is not zero",
    },
    {
        "opcode": "0x18",
        "mnemonic": "JR e",
        "description": "Jump relative by signed displacement",
    },
    {
        "opcode": "0x20",
        "mnemonic": "JR NZ,e",
        "description": "Jump relative if Z is reset",
    },
    {
        "opcode": "0x28",
        "mnemonic": "JR Z,e",
        "description": "Jump relative if Z is set",
    },
    {
        "opcode": "0x30",
        "mnemonic": "JR NC,e",
        "description": "Jump relative if C is reset",
    },
    {
        "opcode": "0x38",
        "mnemonic": "JR C,e",
        "description": "Jump relative if C is set",
    },
    {
        "opcode": "0xC2",
        "mnemonic": "JP NZ,nn",
        "description": "Jump to nn if Z is reset",
    },
    {"opcode": "0xC3", "mnemonic": "JP nn", "description": "Jump directly to nn"},
    {"opcode": "0xCA", "mnemonic": "JP Z,nn", "description": "Jump to nn if Z is set"},
    {
        "opcode": "0xD2",
        "mnemonic": "JP NC,nn",
        "description": "Jump to nn if C is reset",
    },
    {"opcode": "0xDA", "mnemonic": "JP C,nn", "description": "Jump to nn if C is set"},
    {
        "opcode": "0xE2",
        "mnemonic": "JP PO,nn",
        "description": "Jump to nn if parity is odd",
    },
    {
        "opcode": "0xE9",
        "mnemonic": "JP (HL)",
        "description": "Jump to the address contained in HL",
    },
    {
        "opcode": "0xEA",
        "mnemonic": "JP PE,nn",
        "description": "Jump to nn if parity is even",
    },
    {
        "opcode": "0xF2",
        "mnemonic": "JP P,nn",
        "description": "Jump to nn if sign is positive",
    },
    {
        "opcode": "0xFA",
        "mnemonic": "JP M,nn",
        "description": "Jump to nn if sign is negative",
    },
]


def _matches_opcode(opcode, entry):
    value = entry["opcode"]
    if "-" in value:
        start, end = value.split("-", 1)
        return int(start, 16) <= opcode <= int(end, 16)
    return opcode == int(value, 16)


# Opcode: 0x10
# Mnemonic: DJNZ e
# Description: Decrement B and jump relative if B is not zero


def _djnz_e(self):
    displacement = self.ingest_next_byte()
    self.B.dec()
    if self.B.get() != 0:
        self.jump_relative(displacement)
        return 13
    return 8


# Opcode: 0x18
# Mnemonic: JR e
# Description: Jump relative by signed displacement


def _jr_e(self):
    displacement = self.ingest_next_byte()
    self.jump_relative(displacement)
    return 12


# Opcode: 0x20
# Mnemonic: JR NZ,e
# Description: Jump relative if Z is reset


def _jr_nz_e(self):
    displacement = self.ingest_next_byte()
    if not self.F.zero:
        self.jump_relative(displacement)
        return 12
    return 7


# Opcode: 0x28
# Mnemonic: JR Z,e
# Description: Jump relative if Z is set


def _jr_z_e(self):
    displacement = self.ingest_next_byte()
    if self.F.zero:
        self.jump_relative(displacement)
        return 12
    return 7


# Opcode: 0x30
# Mnemonic: JR NC,e
# Description: Jump relative if C is reset


def _jr_nc_e(self):
    displacement = self.ingest_next_byte()
    if not self.F.carry:
        self.jump_relative(displacement)
        return 12
    return 7


# Opcode: 0x38
# Mnemonic: JR C,e
# Description: Jump relative if C is set


def _jr_c_e(self):
    displacement = self.ingest_next_byte()
    if self.F.carry:
        self.jump_relative(displacement)
        return 12
    return 7


# Opcode: 0xC2
# Mnemonic: JP NZ,nn
# Description: Jump to nn if Z is reset


def _jp_nz_nn(self):
    address = self.ingest_next_word()
    if not self.F.zero:
        self.jump_absolute(address)
        return 16
    return 10


# Opcode: 0xC3
# Mnemonic: JP nn
# Description: Jump directly to nn


def _jp_nn(self):
    nn = self.ingest_next_word()
    self.jump_absolute(nn)
    return 10


# Opcode: 0xCA
# Mnemonic: JP Z,nn
# Description: Jump to nn if Z is set


def _jp_z_nn(self):
    address = self.ingest_next_word()
    if self.F.zero:
        self.jump_absolute(address)
        return 16
    return 10


# Opcode: 0xD2
# Mnemonic: JP NC,nn
# Description: Jump to nn if C is reset


def _jp_nc_nn(self):
    address = self.ingest_next_word()
    if not self.F.carry:
        self.jump_absolute(address)
        return 16
    return 10


# Opcode: 0xDA
# Mnemonic: JP C,nn
# Description: Jump to nn if C is set


def _jp_c_nn(self):
    address = self.ingest_next_word()
    if self.F.carry:
        self.jump_absolute(address)
        return 16
    return 10


# Opcode: 0xE2
# Mnemonic: JP PO,nn
# Description: Jump to nn if parity is odd


def _jp_po_nn(self):
    address = self.ingest_next_word()
    if not self.F.parity_overflow:
        self.jump_absolute(address)
        return 16
    return 10


# Opcode: 0xE9
# Mnemonic: JP (HL)
# Description: Jump to the address contained in HL


def _jp_hl(self):
    self.PC.set(self.HL.get())
    return 4


# Opcode: 0xEA
# Mnemonic: JP PE,nn
# Description: Jump to nn if parity is even


def _jp_pe_nn(self):
    address = self.ingest_next_word()
    if self.F.parity_overflow:
        self.jump_absolute(address)
        return 16
    return 10


# Opcode: 0xF2
# Mnemonic: JP P,nn
# Description: Jump to nn if sign is positive


def _jp_p_nn(self):
    address = self.ingest_next_word()
    if not self.F.sign:
        self.jump_absolute(address)
        return 16
    return 10


# Opcode: 0xFA
# Mnemonic: JP M,nn
# Description: Jump to nn if sign is negative


def _jp_m_nn(self):
    address = self.ingest_next_word()
    if self.F.sign:
        self.jump_absolute(address)
        return 16
    return 10


def execute(self, opcode):
    for entry in OPCODES:
        if _matches_opcode(opcode, entry):
            if opcode == 0x10:
                return _djnz_e(self)
            if opcode == 0x18:
                return _jr_e(self)
            if opcode == 0x20:
                return _jr_nz_e(self)
            if opcode == 0x28:
                return _jr_z_e(self)
            if opcode == 0x30:
                return _jr_nc_e(self)
            if opcode == 0x38:
                return _jr_c_e(self)
            if opcode == 0xC2:
                return _jp_nz_nn(self)
            if opcode == 0xC3:
                return _jp_nn(self)
            if opcode == 0xCA:
                return _jp_z_nn(self)
            if opcode == 0xD2:
                return _jp_nc_nn(self)
            if opcode == 0xDA:
                return _jp_c_nn(self)
            if opcode == 0xE2:
                return _jp_po_nn(self)
            if opcode == 0xE9:
                return _jp_hl(self)
            if opcode == 0xEA:
                return _jp_pe_nn(self)
            if opcode == 0xF2:
                return _jp_p_nn(self)
            if opcode == 0xFA:
                return _jp_m_nn(self)

            raise NotImplementedError(
                f"{__name__}: {entry['opcode']} {entry['mnemonic']} ({entry['description']}) is not implemented"
            )

    raise NotImplementedError(
        f"{__name__}: opcode 0x{opcode:02X} is not defined in the jump table"
    )
