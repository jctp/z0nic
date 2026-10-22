OPCODES = [
    {"opcode": "0x01", "mnemonic": "LD BC,nn", "description": "Load immediate 16-bit value into BC"},
    {"opcode": "0x11", "mnemonic": "LD DE,nn", "description": "Load immediate 16-bit value into DE"},
    {"opcode": "0x18", "mnemonic": "JR e", "description": "Jump relative by signed displacement"},
    {"opcode": "0x21", "mnemonic": "LD IX,nn", "description": "Load immediate 16-bit value into IX"},
    {"opcode": "0x22", "mnemonic": "LD (nn),IX", "description": "Store IX to absolute memory address"},
    {"opcode": "0x23", "mnemonic": "INC IX", "description": "Increment IX"},
    {"opcode": "0x29", "mnemonic": "ADD IX,BC", "description": "Add BC to IX"},
    {"opcode": "0x2A", "mnemonic": "LD IX,(nn)", "description": "Load IX from absolute memory address"},
    {"opcode": "0x2B", "mnemonic": "DEC IX", "description": "Decrement IX"},
    {"opcode": "0x31", "mnemonic": "LD SP,nn", "description": "Load immediate 16-bit value into SP"},
    {"opcode": "0x39", "mnemonic": "ADD IX,SP", "description": "Add SP to IX"},
    {"opcode": "0x3A", "mnemonic": "LD A,(nn)", "description": "Load A from absolute memory address"},
    {"opcode": "0x46", "mnemonic": "LD B,(IX+d)", "description": "Load B from indexed memory"},
    {"opcode": "0x4E", "mnemonic": "LD C,(IX+d)", "description": "Load C from indexed memory"},
    {"opcode": "0x56", "mnemonic": "LD D,(IX+d)", "description": "Load D from indexed memory"},
    {"opcode": "0x5E", "mnemonic": "LD E,(IX+d)", "description": "Load E from indexed memory"},
    {"opcode": "0x66", "mnemonic": "LD H,(IX+d)", "description": "Load H from indexed memory"},
    {"opcode": "0x6E", "mnemonic": "LD L,(IX+d)", "description": "Load L from indexed memory"},
    {"opcode": "0x70-0x75", "mnemonic": "LD (IX+d),r", "description": "Store a register to indexed memory"},
    {"opcode": "0x77", "mnemonic": "LD (IX+d),A", "description": "Store A to indexed memory"},
    {"opcode": "0x7E", "mnemonic": "LD A,(IX+d)", "description": "Load A from indexed memory"},
    {"opcode": "0xCB", "mnemonic": "DD CB prefix", "description": "Prefix for the IX bit-manipulation table"},
    {"opcode": "0xE1", "mnemonic": "POP IX", "description": "Pop the top of the stack into IX"},
    {"opcode": "0xE5", "mnemonic": "PUSH IX", "description": "Push IX onto the stack"},
    {"opcode": "0xE6", "mnemonic": "AND n", "description": "Logical AND A with the immediate byte"},
    {"opcode": "0xEE", "mnemonic": "XOR n", "description": "Logical XOR A with the immediate byte"},
    {"opcode": "0xF6", "mnemonic": "OR n", "description": "Logical OR A with the immediate byte"},
    {"opcode": "0xFE", "mnemonic": "CP n", "description": "Compare A with the immediate byte"},
    {"opcode": "0xDD", "mnemonic": "DD prefix", "description": "Prefix for the IX instruction table"},
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

def _ld_bc_nn_ix(self):
    return None


# Opcode: 0x11
# Mnemonic: LD DE,nn
# Description: Load immediate 16-bit value into DE

def _ld_de_nn_ix(self):
    return None


# Opcode: 0x18
# Mnemonic: JR e
# Description: Jump relative by signed displacement

def _jr_e_ix(self):
    return None


# Opcode: 0x21
# Mnemonic: LD IX,nn
# Description: Load immediate 16-bit value into IX

def _ld_ix_nn(self):
    return None


# Opcode: 0x22
# Mnemonic: LD (nn),IX
# Description: Store IX to absolute memory address

def _ld_nn_ix(self):
    return None


# Opcode: 0x23
# Mnemonic: INC IX
# Description: Increment IX

def _inc_ix(self):
    return None


# Opcode: 0x29
# Mnemonic: ADD IX,BC
# Description: Add BC to IX

def _add_ix_bc(self):
    return None


# Opcode: 0x2A
# Mnemonic: LD IX,(nn)
# Description: Load IX from absolute memory address

def _ld_ix_nn_mem(self):
    return None


# Opcode: 0x2B
# Mnemonic: DEC IX
# Description: Decrement IX

def _dec_ix(self):
    return None


# Opcode: 0x31
# Mnemonic: LD SP,nn
# Description: Load immediate 16-bit value into SP

def _ld_sp_nn_ix(self):
    return None


# Opcode: 0x39
# Mnemonic: ADD IX,SP
# Description: Add SP to IX

def _add_ix_sp(self):
    return None


# Opcode: 0x3A
# Mnemonic: LD A,(nn)
# Description: Load A from absolute memory address

def _ld_a_nn_ix(self):
    return None


# Opcode: 0x46
# Mnemonic: LD B,(IX+d)
# Description: Load B from indexed memory

def _ld_b_ix_d(self):
    return None


# Opcode: 0x4E
# Mnemonic: LD C,(IX+d)
# Description: Load C from indexed memory

def _ld_c_ix_d(self):
    return None


# Opcode: 0x56
# Mnemonic: LD D,(IX+d)
# Description: Load D from indexed memory

def _ld_d_ix_d(self):
    return None


# Opcode: 0x5E
# Mnemonic: LD E,(IX+d)
# Description: Load E from indexed memory

def _ld_e_ix_d(self):
    return None


# Opcode: 0x66
# Mnemonic: LD H,(IX+d)
# Description: Load H from indexed memory

def _ld_h_ix_d(self):
    return None


# Opcode: 0x6E
# Mnemonic: LD L,(IX+d)
# Description: Load L from indexed memory

def _ld_l_ix_d(self):
    return None


# Opcode: 0x70-0x75
# Mnemonic: LD (IX+d),r
# Description: Store a register to indexed memory

def _ld_ix_d_r(self):
    return None


# Opcode: 0x77
# Mnemonic: LD (IX+d),A
# Description: Store A to indexed memory

def _ld_ix_d_a(self):
    return None


# Opcode: 0x7E
# Mnemonic: LD A,(IX+d)
# Description: Load A from indexed memory

def _ld_a_ix_d(self):
    return None


# Opcode: 0xCB
# Mnemonic: DD CB prefix
# Description: Prefix for the IX bit-manipulation table

def _dd_cb_prefix(self):
    return None


# Opcode: 0xE1
# Mnemonic: POP IX
# Description: Pop the top of the stack into IX

def _pop_ix(self):
    return None


# Opcode: 0xE5
# Mnemonic: PUSH IX
# Description: Push IX onto the stack

def _push_ix(self):
    return None


# Opcode: 0xE6
# Mnemonic: AND n
# Description: Logical AND A with the immediate byte

def _and_n_ix(self):
    return None


# Opcode: 0xEE
# Mnemonic: XOR n
# Description: Logical XOR A with the immediate byte

def _xor_n_ix(self):
    return None


# Opcode: 0xF6
# Mnemonic: OR n
# Description: Logical OR A with the immediate byte

def _or_n_ix(self):
    return None


# Opcode: 0xFE
# Mnemonic: CP n
# Description: Compare A with the immediate byte

def _cp_n_ix(self):
    return None


def execute(self):
    opcode = self.memory.read8(self.PC)
    self.PC.inc(by=1)

    for entry in OPCODES:
        if _matches_opcode(opcode, entry):
            if opcode == 0x01:
                return _ld_bc_nn_ix(self)
            if opcode == 0x11:
                return _ld_de_nn_ix(self)
            if opcode == 0x18:
                return _jr_e_ix(self)
            if opcode == 0x21:
                return _ld_ix_nn(self)
            if opcode == 0x22:
                return _ld_nn_ix(self)
            if opcode == 0x23:
                return _inc_ix(self)
            if opcode == 0x29:
                return _add_ix_bc(self)
            if opcode == 0x2A:
                return _ld_ix_nn_mem(self)
            if opcode == 0x2B:
                return _dec_ix(self)
            if opcode == 0x31:
                return _ld_sp_nn_ix(self)
            if opcode == 0x39:
                return _add_ix_sp(self)
            if opcode == 0x3A:
                return _ld_a_nn_ix(self)
            if opcode == 0x46:
                return _ld_b_ix_d(self)
            if opcode == 0x4E:
                return _ld_c_ix_d(self)
            if opcode == 0x56:
                return _ld_d_ix_d(self)
            if opcode == 0x5E:
                return _ld_e_ix_d(self)
            if opcode == 0x66:
                return _ld_h_ix_d(self)
            if opcode == 0x6E:
                return _ld_l_ix_d(self)
            if 0x70 <= opcode <= 0x75:
                return _ld_ix_d_r(self)
            if opcode == 0x77:
                return _ld_ix_d_a(self)
            if opcode == 0x7E:
                return _ld_a_ix_d(self)
            if opcode == 0xCB:
                return _dd_cb_prefix(self)
            if opcode == 0xE1:
                return _pop_ix(self)
            if opcode == 0xE5:
                return _push_ix(self)
            if opcode == 0xE6:
                return _and_n_ix(self)
            if opcode == 0xEE:
                return _xor_n_ix(self)
            if opcode == 0xF6:
                return _or_n_ix(self)
            if opcode == 0xFE:
                return _cp_n_ix(self)

            raise NotImplementedError(
                f"{__name__}: {entry['opcode']} {entry['mnemonic']} ({entry['description']}) is not implemented"
            )

    raise NotImplementedError(f"{__name__}: opcode 0x{opcode:02X} is not defined in the DD-prefixed instruction table")
