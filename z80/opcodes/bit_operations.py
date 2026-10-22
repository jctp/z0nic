OPCODES = [
    {"opcode": "0x00-0x07", "mnemonic": "RLC r", "description": "Rotate left circular through carry"},
    {"opcode": "0x08-0x0F", "mnemonic": "RRC r", "description": "Rotate right circular through carry"},
    {"opcode": "0x10-0x17", "mnemonic": "RL r", "description": "Rotate left through carry"},
    {"opcode": "0x18-0x1F", "mnemonic": "RR r", "description": "Rotate right through carry"},
    {"opcode": "0x20-0x27", "mnemonic": "SLA r", "description": "Shift left arithmetic"},
    {"opcode": "0x28-0x2F", "mnemonic": "SRA r", "description": "Shift right arithmetic"},
    {"opcode": "0x30-0x37", "mnemonic": "SLL r", "description": "Shift left logical"},
    {"opcode": "0x38-0x3F", "mnemonic": "SRL r", "description": "Shift right logical"},
    {"opcode": "0x40-0x7F", "mnemonic": "BIT b,r", "description": "Test a bit in the selected register or memory byte"},
    {"opcode": "0x80-0xBF", "mnemonic": "RES b,r", "description": "Reset a bit in the selected register or memory byte"},
    {"opcode": "0xC0-0xFF", "mnemonic": "SET b,r", "description": "Set a bit in the selected register or memory byte"},
    {"opcode": "0x07", "mnemonic": "RLCA", "description": "Rotate A left through carry"},
    {"opcode": "0x08", "mnemonic": "EX AF,AF'", "description": "Exchange AF with AF'"},
    {"opcode": "0x0F", "mnemonic": "RRCA", "description": "Rotate A right through carry"},
    {"opcode": "0x17", "mnemonic": "RLA", "description": "Rotate A left through carry"},
    {"opcode": "0x1F", "mnemonic": "RRA", "description": "Rotate A right through carry"},
    {"opcode": "0x27", "mnemonic": "DAA", "description": "Decimal adjust accumulator"},
    {"opcode": "0x2F", "mnemonic": "CPL", "description": "Complement accumulator"},
    {"opcode": "0x37", "mnemonic": "SCF", "description": "Set carry flag"},
    {"opcode": "0x3F", "mnemonic": "CCF", "description": "Complement carry flag"},
    {"opcode": "0xCB", "mnemonic": "CB prefix", "description": "Prefix for the bit-manipulation table"},
    {"opcode": "0xD9", "mnemonic": "EXX", "description": "Exchange BC, DE, and HL with their shadow registers"},
    {"opcode": "0xE3", "mnemonic": "EX (SP),HL", "description": "Exchange HL with the top of stack"},
    {"opcode": "0xEB", "mnemonic": "EX DE,HL", "description": "Exchange DE and HL"},
]


def _matches_opcode(opcode, entry):
    value = entry["opcode"]
    if "-" in value:
        start, end = value.split("-", 1)
        return int(start, 16) <= opcode <= int(end, 16)
    return opcode == int(value, 16)


# Opcode: 0x00-0x07
# Mnemonic: RLC r
# Description: Rotate left circular through carry

def _rlc_r(self):
    return None


# Opcode: 0x08-0x0F
# Mnemonic: RRC r
# Description: Rotate right circular through carry

def _rrc_r(self):
    return None


# Opcode: 0x10-0x17
# Mnemonic: RL r
# Description: Rotate left through carry

def _rl_r(self):
    return None


# Opcode: 0x18-0x1F
# Mnemonic: RR r
# Description: Rotate right through carry

def _rr_r(self):
    return None


# Opcode: 0x20-0x27
# Mnemonic: SLA r
# Description: Shift left arithmetic

def _sla_r(self):
    return None


# Opcode: 0x28-0x2F
# Mnemonic: SRA r
# Description: Shift right arithmetic

def _sra_r(self):
    return None


# Opcode: 0x30-0x37
# Mnemonic: SLL r
# Description: Shift left logical

def _sll_r(self):
    return None


# Opcode: 0x38-0x3F
# Mnemonic: SRL r
# Description: Shift right logical

def _srl_r(self):
    return None


# Opcode: 0x40-0x7F
# Mnemonic: BIT b,r
# Description: Test a bit in the selected register or memory byte

def _bit_b_r(self):
    return None


# Opcode: 0x80-0xBF
# Mnemonic: RES b,r
# Description: Reset a bit in the selected register or memory byte

def _res_b_r(self):
    return None


# Opcode: 0xC0-0xFF
# Mnemonic: SET b,r
# Description: Set a bit in the selected register or memory byte

def _set_b_r(self):
    return None


# Opcode: 0x07
# Mnemonic: RLCA
# Description: Rotate A left through carry

def _rlca(self):
    return None


# Opcode: 0x08
# Mnemonic: EX AF,AF'
# Description: Exchange AF with AF'

def _ex_af_af_prime(self):
    return None


# Opcode: 0x0F
# Mnemonic: RRCA
# Description: Rotate A right through carry

def _rrca(self):
    return None


# Opcode: 0x17
# Mnemonic: RLA
# Description: Rotate A left through carry

def _rla(self):
    return None


# Opcode: 0x1F
# Mnemonic: RRA
# Description: Rotate A right through carry

def _rra(self):
    return None


# Opcode: 0x27
# Mnemonic: DAA
# Description: Decimal adjust accumulator

def _daa(self):
    return None


# Opcode: 0x2F
# Mnemonic: CPL
# Description: Complement accumulator

def _cpl(self):
    return None


# Opcode: 0x37
# Mnemonic: SCF
# Description: Set carry flag

def _scf(self):
    return None


# Opcode: 0x3F
# Mnemonic: CCF
# Description: Complement carry flag

def _ccf(self):
    return None


# Opcode: 0xCB
# Mnemonic: CB prefix
# Description: Prefix for the bit-manipulation table

def _cb_prefix(self):
    return None


# Opcode: 0xD9
# Mnemonic: EXX
# Description: Exchange BC, DE, and HL with their shadow registers

def _exx(self):
    return None


# Opcode: 0xE3
# Mnemonic: EX (SP),HL
# Description: Exchange HL with the top of stack

def _ex_sp_hl(self):
    return None


# Opcode: 0xEB
# Mnemonic: EX DE,HL
# Description: Exchange DE and HL

def _ex_de_hl(self):
    return None


def execute(self, opcode):
    for entry in OPCODES:
        if _matches_opcode(opcode, entry):
            if 0x00 <= opcode <= 0x07:
                return _rlc_r(self)
            if 0x08 <= opcode <= 0x0F:
                return _rrc_r(self)
            if 0x10 <= opcode <= 0x17:
                return _rl_r(self)
            if 0x18 <= opcode <= 0x1F:
                return _rr_r(self)
            if 0x20 <= opcode <= 0x27:
                return _sla_r(self)
            if 0x28 <= opcode <= 0x2F:
                return _sra_r(self)
            if 0x30 <= opcode <= 0x37:
                return _sll_r(self)
            if 0x38 <= opcode <= 0x3F:
                return _srl_r(self)
            if 0x40 <= opcode <= 0x7F:
                return _bit_b_r(self)
            if 0x80 <= opcode <= 0xBF:
                return _res_b_r(self)
            if 0xC0 <= opcode <= 0xFF:
                return _set_b_r(self)
            if opcode == 0x07:
                return _rlca(self)
            if opcode == 0x08:
                return _ex_af_af_prime(self)
            if opcode == 0x0F:
                return _rrca(self)
            if opcode == 0x17:
                return _rla(self)
            if opcode == 0x1F:
                return _rra(self)
            if opcode == 0x27:
                return _daa(self)
            if opcode == 0x2F:
                return _cpl(self)
            if opcode == 0x37:
                return _scf(self)
            if opcode == 0x3F:
                return _ccf(self)
            if opcode == 0xCB:
                return _cb_prefix(self)
            if opcode == 0xD9:
                return _exx(self)
            if opcode == 0xE3:
                return _ex_sp_hl(self)
            if opcode == 0xEB:
                return _ex_de_hl(self)

            raise NotImplementedError(
                f"{__name__}: {entry['opcode']} {entry['mnemonic']} ({entry['description']}) is not implemented"
            )

    raise NotImplementedError(f"{__name__}: opcode 0x{opcode:02X} is not defined in the bit-operation table")
