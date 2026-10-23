OPCODES = [
    {"opcode": "0x01", "mnemonic": "LD BC,nn", "description": "Load immediate 16-bit value into BC"},
    {"opcode": "0x11", "mnemonic": "LD DE,nn", "description": "Load immediate 16-bit value into DE"},
    {"opcode": "0x18", "mnemonic": "JR e", "description": "Jump relative by signed displacement"},
    {"opcode": "0x21", "mnemonic": "LD IY,nn", "description": "Load immediate 16-bit value into IY"},
    {"opcode": "0x22", "mnemonic": "LD (nn),IY", "description": "Store IY to absolute memory address"},
    {"opcode": "0x23", "mnemonic": "INC IY", "description": "Increment IY"},
    {"opcode": "0x29", "mnemonic": "ADD IY,BC", "description": "Add BC to IY"},
    {"opcode": "0x2A", "mnemonic": "LD IY,(nn)", "description": "Load IY from absolute memory address"},
    {"opcode": "0x2B", "mnemonic": "DEC IY", "description": "Decrement IY"},
    {"opcode": "0x31", "mnemonic": "LD SP,nn", "description": "Load immediate 16-bit value into SP"},
    {"opcode": "0x39", "mnemonic": "ADD IY,SP", "description": "Add SP to IY"},
    {"opcode": "0x3A", "mnemonic": "LD A,(nn)", "description": "Load A from absolute memory address"},
    {"opcode": "0x46", "mnemonic": "LD B,(IY+d)", "description": "Load B from indexed memory"},
    {"opcode": "0x4E", "mnemonic": "LD C,(IY+d)", "description": "Load C from indexed memory"},
    {"opcode": "0x56", "mnemonic": "LD D,(IY+d)", "description": "Load D from indexed memory"},
    {"opcode": "0x5E", "mnemonic": "LD E,(IY+d)", "description": "Load E from indexed memory"},
    {"opcode": "0x66", "mnemonic": "LD H,(IY+d)", "description": "Load H from indexed memory"},
    {"opcode": "0x6E", "mnemonic": "LD L,(IY+d)", "description": "Load L from indexed memory"},
    {"opcode": "0x70-0x75", "mnemonic": "LD (IY+d),r", "description": "Store a register to indexed memory"},
    {"opcode": "0x77", "mnemonic": "LD (IY+d),A", "description": "Store A to indexed memory"},
    {"opcode": "0x7E", "mnemonic": "LD A,(IY+d)", "description": "Load A from indexed memory"},
    {"opcode": "0xCB", "mnemonic": "FD CB prefix", "description": "Prefix for the IY bit-manipulation table"},
    {"opcode": "0xE1", "mnemonic": "POP IY", "description": "Pop the top of the stack into IY"},
    {"opcode": "0xE5", "mnemonic": "PUSH IY", "description": "Push IY onto the stack"},
    {"opcode": "0xE6", "mnemonic": "AND n", "description": "Logical AND A with the immediate byte"},
    {"opcode": "0xEE", "mnemonic": "XOR n", "description": "Logical XOR A with the immediate byte"},
    {"opcode": "0xF6", "mnemonic": "OR n", "description": "Logical OR A with the immediate byte"},
    {"opcode": "0xFE", "mnemonic": "CP n", "description": "Compare A with the immediate byte"},
    {"opcode": "0xFD", "mnemonic": "FD prefix", "description": "Prefix for the IY instruction table"},
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

def _ld_bc_nn_iy(self):
    return None


# Opcode: 0x11
# Mnemonic: LD DE,nn
# Description: Load immediate 16-bit value into DE

def _ld_de_nn_iy(self):
    return None


# Opcode: 0x18
# Mnemonic: JR e
# Description: Jump relative by signed displacement

def _jr_e_iy(self):
    return None


# Opcode: 0x21
# Mnemonic: LD IY,nn
# Description: Load immediate 16-bit value into IY

def _ld_iy_nn(self):
    return None


# Opcode: 0x22
# Mnemonic: LD (nn),IY
# Description: Store IY to absolute memory address

def _ld_nn_iy(self):
    return None


# Opcode: 0x23
# Mnemonic: INC IY
# Description: Increment IY

def _inc_iy(self):
    return None


# Opcode: 0x29
# Mnemonic: ADD IY,BC
# Description: Add BC to IY

def _add_iy_bc(self):
    return None


# Opcode: 0x2A
# Mnemonic: LD IY,(nn)
# Description: Load IY from absolute memory address

def _ld_iy_nn_mem(self):
    return None


# Opcode: 0x2B
# Mnemonic: DEC IY
# Description: Decrement IY

def _dec_iy(self):
    return None


# Opcode: 0x31
# Mnemonic: LD SP,nn
# Description: Load immediate 16-bit value into SP

def _ld_sp_nn_iy(self):
    return None


# Opcode: 0x39
# Mnemonic: ADD IY,SP
# Description: Add SP to IY

def _add_iy_sp(self):
    return None


# Opcode: 0x3A
# Mnemonic: LD A,(nn)
# Description: Load A from absolute memory address

def _ld_a_nn_iy(self):
    return None


# Opcode: 0x46
# Mnemonic: LD B,(IY+d)
# Description: Load B from indexed memory

def _ld_b_iy_d(self):
    return None


# Opcode: 0x4E
# Mnemonic: LD C,(IY+d)
# Description: Load C from indexed memory

def _ld_c_iy_d(self):
    return None


# Opcode: 0x56
# Mnemonic: LD D,(IY+d)
# Description: Load D from indexed memory

def _ld_d_iy_d(self):
    return None


# Opcode: 0x5E
# Mnemonic: LD E,(IY+d)
# Description: Load E from indexed memory

def _ld_e_iy_d(self):
    return None


# Opcode: 0x66
# Mnemonic: LD H,(IY+d)
# Description: Load H from indexed memory

def _ld_h_iy_d(self):
    return None


# Opcode: 0x6E
# Mnemonic: LD L,(IY+d)
# Description: Load L from indexed memory

def _ld_l_iy_d(self):
    return None


# Opcode: 0x70-0x75
# Mnemonic: LD (IY+d),r
# Description: Store a register to indexed memory

def _ld_iy_d_r(self):
    return None


# Opcode: 0x77
# Mnemonic: LD (IY+d),A
# Description: Store A to indexed memory

def _ld_iy_d_a(self):
    return None


# Opcode: 0x7E
# Mnemonic: LD A,(IY+d)
# Description: Load A from indexed memory

def _ld_a_iy_d(self):
    return None


# Opcode: 0xCB
# Mnemonic: FD CB prefix
# Description: Prefix for the IY bit-manipulation table

def _fd_cb_prefix(self):
    return None


# Opcode: 0xE1
# Mnemonic: POP IY
# Description: Pop the top of the stack into IY

def _pop_iy(self):
    return None


# Opcode: 0xE5
# Mnemonic: PUSH IY
# Description: Push IY onto the stack

def _push_iy(self):
    return None


# Opcode: 0xE6
# Mnemonic: AND n
# Description: Logical AND A with the immediate byte

def _and_n_iy(self):
    return None


# Opcode: 0xEE
# Mnemonic: XOR n
# Description: Logical XOR A with the immediate byte

def _xor_n_iy(self):
    return None


# Opcode: 0xF6
# Mnemonic: OR n
# Description: Logical OR A with the immediate byte

def _or_n_iy(self):
    return None


# Opcode: 0xFE
# Mnemonic: CP n
# Description: Compare A with the immediate byte

def _cp_n_iy(self):
    return None


def execute(self, opcode):
    prefix = opcode
    opcode = self.ingest_next_byte()

    for entry in OPCODES:
        if _matches_opcode(opcode, entry):
            if opcode == 0x01:
                return _ld_bc_nn_iy(self)
            if opcode == 0x11:
                return _ld_de_nn_iy(self)
            if opcode == 0x18:
                return _jr_e_iy(self)
            if opcode == 0x21:
                return _ld_iy_nn(self)
            if opcode == 0x22:
                return _ld_nn_iy(self)
            if opcode == 0x23:
                return _inc_iy(self)
            if opcode == 0x29:
                return _add_iy_bc(self)
            if opcode == 0x2A:
                return _ld_iy_nn_mem(self)
            if opcode == 0x2B:
                return _dec_iy(self)
            if opcode == 0x31:
                return _ld_sp_nn_iy(self)
            if opcode == 0x39:
                return _add_iy_sp(self)
            if opcode == 0x3A:
                return _ld_a_nn_iy(self)
            if opcode == 0x46:
                return _ld_b_iy_d(self)
            if opcode == 0x4E:
                return _ld_c_iy_d(self)
            if opcode == 0x56:
                return _ld_d_iy_d(self)
            if opcode == 0x5E:
                return _ld_e_iy_d(self)
            if opcode == 0x66:
                return _ld_h_iy_d(self)
            if opcode == 0x6E:
                return _ld_l_iy_d(self)
            if 0x70 <= opcode <= 0x75:
                return _ld_iy_d_r(self)
            if opcode == 0x77:
                return _ld_iy_d_a(self)
            if opcode == 0x7E:
                return _ld_a_iy_d(self)
            if opcode == 0xCB:
                return _fd_cb_prefix(self)
            if opcode == 0xE1:
                return _pop_iy(self)
            if opcode == 0xE5:
                return _push_iy(self)
            if opcode == 0xE6:
                return _and_n_iy(self)
            if opcode == 0xEE:
                return _xor_n_iy(self)
            if opcode == 0xF6:
                return _or_n_iy(self)
            if opcode == 0xFE:
                return _cp_n_iy(self)

            raise NotImplementedError(
                f"{__name__}: {prefix:02X} {opcode:02X} {entry['mnemonic']} ({entry['description']}) is not implemented"
            )

    raise NotImplementedError(
        f"{__name__}: {prefix:02X} {opcode:02X} is not defined in the FD-prefixed instruction table"
    )
