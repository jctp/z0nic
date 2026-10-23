OPCODES = [
    {
        "opcode": "0x01",
        "mnemonic": "LD BC,nn",
        "description": "Load immediate 16-bit value into BC",
    },
    {
        "opcode": "0x02",
        "mnemonic": "LD (BC),A",
        "description": "Store A into memory at BC",
    },
    {
        "opcode": "0x06",
        "mnemonic": "LD B,n",
        "description": "Load immediate byte into B",
    },
    {
        "opcode": "0x0A",
        "mnemonic": "LD A,(BC)",
        "description": "Load A from memory at BC",
    },
    {
        "opcode": "0x0E",
        "mnemonic": "LD C,n",
        "description": "Load immediate byte into C",
    },
    {
        "opcode": "0x11",
        "mnemonic": "LD DE,nn",
        "description": "Load immediate 16-bit value into DE",
    },
    {
        "opcode": "0x12",
        "mnemonic": "LD (DE),A",
        "description": "Store A into memory at DE",
    },
    {
        "opcode": "0x16",
        "mnemonic": "LD D,n",
        "description": "Load immediate byte into D",
    },
    {
        "opcode": "0x1A",
        "mnemonic": "LD A,(DE)",
        "description": "Load A from memory at DE",
    },
    {
        "opcode": "0x1E",
        "mnemonic": "LD E,n",
        "description": "Load immediate byte into E",
    },
    {
        "opcode": "0x21",
        "mnemonic": "LD HL,nn",
        "description": "Load immediate 16-bit value into HL",
    },
    {
        "opcode": "0x22",
        "mnemonic": "LD (nn),HL",
        "description": "Store HL to absolute memory address",
    },
    {
        "opcode": "0x26",
        "mnemonic": "LD H,n",
        "description": "Load immediate byte into H",
    },
    {
        "opcode": "0x2A",
        "mnemonic": "LD HL,(nn)",
        "description": "Load HL from absolute memory address",
    },
    {
        "opcode": "0x2E",
        "mnemonic": "LD L,n",
        "description": "Load immediate byte into L",
    },
    {
        "opcode": "0x31",
        "mnemonic": "LD SP,nn",
        "description": "Load immediate 16-bit value into SP",
    },
    {
        "opcode": "0x32",
        "mnemonic": "LD (nn),A",
        "description": "Store A to absolute memory address",
    },
    {
        "opcode": "0x36",
        "mnemonic": "LD (HL),n",
        "description": "Store immediate byte to memory at HL",
    },
    {
        "opcode": "0x3A",
        "mnemonic": "LD A,(nn)",
        "description": "Load A from absolute memory address",
    },
    {
        "opcode": "0x3E",
        "mnemonic": "LD A,n",
        "description": "Load immediate byte into A",
    },
    {
        "opcode": "0x40-0x7F",
        "mnemonic": "LD r,r",
        "description": "Load register to register",
    },
    {"opcode": "0xF9", "mnemonic": "LD SP,HL", "description": "Load HL into SP"},
]


def _matches_opcode(opcode, entry):
    value = entry["opcode"]
    if "-" in value:
        start, end = value.split("-", 1)
        return int(start, 16) <= opcode <= int(end, 16)
    return opcode == int(value, 16)


# Opcode: 0x01
# Mnemonic: LD BC,nn
# Description: Load immediate 16-bit value into BC


def _ld_bc_nn(self):
    nn = self.ingest_next_word()
    self.BC.set(nn)
    return 10


# Opcode: 0x02
# Mnemonic: LD (BC),A
# Description: Store A into memory at BC


def _ld_bc_a(self):
    return None


# Opcode: 0x06
# Mnemonic: LD B,n
# Description: Load immediate byte into B


def _ld_b_n(self):
    n = self.ingest_next_byte()
    self.B.set(n)
    return 7


# Opcode: 0x0A
# Mnemonic: LD A,(BC)
# Description: Load A from memory at BC


def _ld_a_bc(self):
    return None


# Opcode: 0x0E
# Mnemonic: LD C,n
# Description: Load immediate byte into C


def _ld_c_n(self):
    n = self.ingest_next_byte()
    self.C.set(n)
    return 7

# Opcode: 0x11
# Mnemonic: LD DE,nn
# Description: Load immediate 16-bit value into DE


def _ld_de_nn(self):
    nn = self.ingest_next_word()
    self.DE.set(nn)
    return 10


# Opcode: 0x12
# Mnemonic: LD (DE),A
# Description: Store A into memory at DE


def _ld_de_a(self):
    self.memory.write8(self.DE.get(), self.A.get())
    return 7


# Opcode: 0x16
# Mnemonic: LD D,n
# Description: Load immediate byte into D


def _ld_d_n(self):
    n = self.ingest_next_byte()
    self.D.set(n)
    return 7

# Opcode: 0x1A
# Mnemonic: LD A,(DE)
# Description: Load A from memory at DE


def _ld_a_de(self):
    return None


# Opcode: 0x1E
# Mnemonic: LD E,n
# Description: Load immediate byte into E


def _ld_e_n(self):
    n = self.ingest_next_byte()
    self.E.set(n)
    return 7


# Opcode: 0x21
# Mnemonic: LD HL,nn
# Description: Load immediate 16-bit value into HL


def _ld_hl_nn(self):
    self.HL.set(self.ingest_next_word())
    return 10


# Opcode: 0x22
# Mnemonic: LD (nn),HL
# Description: Store HL to absolute memory address


def _ld_hl_addr(self):

    self.memory.write16(
        self.ingest_next_word(),
        self.HL.get()
    )

    return 16

# Opcode: 0x26
# Mnemonic: LD H,n
# Description: Load immediate byte into H


def _ld_h_n(self):
    n = self.ingest_next_byte()
    self.H.set(n)
    return 7

# Opcode: 0x2A
# Mnemonic: LD HL,(nn)
# Description: Load HL from absolute memory address


def _ld_hl_a(self):
    return None


# Opcode: 0x2E
# Mnemonic: LD L,n
# Description: Load immediate byte into L


def _ld_l_n(self):
    return None


# Opcode: 0x31
# Mnemonic: LD SP,nn
# Description: Load immediate 16-bit value into SP


def _ld_sp_nn(self):
    nn = self.ingest_next_word()
    self.SP.set(nn)
    return 10


# Opcode: 0x32
# Mnemonic: LD (nn),A
# Description: Store A to absolute memory address


def _ld_nn_a(self):
    nn = self.ingest_next_word()
    A = self.A.get()
    self.memory.write8(nn, A)
    return 13


# Opcode: 0x36
# Mnemonic: LD (HL),n
# Description: Store immediate byte to memory at HL


def _ld_hl_n(self):
    return None


# Opcode: 0x3A
# Mnemonic: LD A,(nn)
# Description: Load A from absolute memory address


def _ld_a_nn(self):
    return None


# Opcode: 0x3E
# Mnemonic: LD A,n
# Description: Load immediate byte into A


def _ld_a_n(self):
    self.A.set(self.ingest_next_byte())
    return 7


# Opcode: 0x40-0x7F
# Mnemonic: LD r,r
# Description: Load register to register


def _ld_r_r(self, opcode):
    self.write_to_opcode_y(opcode, self.read_from_opcode_r(opcode))
    return 4


# Opcode: 0xF9
# Mnemonic: LD SP,HL
# Description: Load HL into SP


def _ld_sp_hl(self):
    self.SP.set(self.HL.get())
    return 6


def execute(self, opcode):
    for entry in OPCODES:
        if _matches_opcode(opcode, entry):
            if opcode == 0x01:
                return _ld_bc_nn(self)
            if opcode == 0x02:
                return _ld_bc_a(self)
            if opcode == 0x06:
                return _ld_b_n(self)
            if opcode == 0x0A:
                return _ld_a_bc(self)
            if opcode == 0x0E:
                return _ld_c_n(self)
            if opcode == 0x11:
                return _ld_de_nn(self)
            if opcode == 0x12:
                return _ld_de_a(self)
            if opcode == 0x16:
                return _ld_d_n(self)
            if opcode == 0x1A:
                return _ld_a_de(self)
            if opcode == 0x1E:
                return _ld_e_n(self)
            if opcode == 0x21:
                return _ld_hl_nn(self)
            if opcode == 0x22:
                return _ld_hl_addr(self)
            if opcode == 0x26:
                return _ld_h_n(self)
            if opcode == 0x2A:
                return _ld_hl_a(self)
            if opcode == 0x2E:
                return _ld_l_n(self)
            if opcode == 0x31:
                return _ld_sp_nn(self)
            if opcode == 0x32:
                return _ld_nn_a(self)
            if opcode == 0x36:
                return _ld_hl_n(self)
            if opcode == 0x3A:
                return _ld_a_nn(self)
            if opcode == 0x3E:
                return _ld_a_n(self)
            if 0x40 <= opcode <= 0x7F and opcode != 0x76:
                return _ld_r_r(self, opcode)
            if opcode == 0xF9:
                return _ld_sp_hl(self)

            raise NotImplementedError(
                f"{__name__}: {entry['opcode']} {entry['mnemonic']} ({entry['description']}) is not implemented"
            )

    raise NotImplementedError(
        f"{__name__}: opcode 0x{opcode:02X} is not defined in the load table"
    )
