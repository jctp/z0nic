OPCODES = [
    {"opcode": "0x00-0x3F", "mnemonic": "RLC/RRC/RL/RR/SLA/SRA/SLL/SRL (IY+d)", "description": "Indexed rotate/shift operation"},
    {"opcode": "0x40-0x7F", "mnemonic": "BIT b,(IY+d)", "description": "Test a bit in the indexed memory byte"},
    {"opcode": "0x80-0xBF", "mnemonic": "RES b,(IY+d)", "description": "Reset a bit in the indexed memory byte"},
    {"opcode": "0xC0-0xFF", "mnemonic": "SET b,(IY+d)", "description": "Set a bit in the indexed memory byte"},
]


def _matches_opcode(opcode, entry):
    value = entry["opcode"]
    if "-" in value:
        start, end = value.split("-", 1)
        return int(start, 16) <= opcode <= int(end, 16)
    return opcode == int(value, 16)


# Opcode: 0x00-0x3F
# Mnemonic: RLC/RRC/RL/RR/SLA/SRA/SLL/SRL (IY+d)
# Description: Indexed rotate/shift operation

def _rlc_rrc_rl_rr_sla_sra_sll_srl_iy_d(self):
    return None


# Opcode: 0x40-0x7F
# Mnemonic: BIT b,(IY+d)
# Description: Test a bit in the indexed memory byte

def _bit_b_iy_d(self):
    return None


# Opcode: 0x80-0xBF
# Mnemonic: RES b,(IY+d)
# Description: Reset a bit in the indexed memory byte

def _res_b_iy_d(self):
    return None


# Opcode: 0xC0-0xFF
# Mnemonic: SET b,(IY+d)
# Description: Set a bit in the indexed memory byte

def _set_b_iy_d(self):
    return None


def execute(self):
    opcode = self.memory.read8(self.PC)
    self.PC.inc(by=1)

    for entry in OPCODES:
        if _matches_opcode(opcode, entry):
            if 0x00 <= opcode <= 0x3F:
                return _rlc_rrc_rl_rr_sla_sra_sll_srl_iy_d(self)
            if 0x40 <= opcode <= 0x7F:
                return _bit_b_iy_d(self)
            if 0x80 <= opcode <= 0xBF:
                return _res_b_iy_d(self)
            if 0xC0 <= opcode <= 0xFF:
                return _set_b_iy_d(self)

            raise NotImplementedError(
                f"{__name__}: {entry['opcode']} {entry['mnemonic']} ({entry['description']}) is not implemented"
            )

    raise NotImplementedError(f"{__name__}: opcode 0x{opcode:02X} is not defined in the FD CB table")
