# NOTE: The opcode table below is agent-generated. The code in this file is not.
# Stub = placeholder that raises via log_opcode(implemented=False).
#
# | Opcode         | Mnemonic                 | Status      | Notes |
# |----------------|--------------------------|-------------|-------|
# | C1, D1, E1, F1 | POP qq (BC, DE, HL, AF)  | Implemented |       |
# | C5, D5, E5, F5 | PUSH qq (BC, DE, HL, AF) | Implemented |       |


def execute(self, opcode):
    # PUSH qq
    if opcode in (0xC5, 0xD5, 0xE5, 0xF5):
        # -----
        # Opcode logic:
        pair = (opcode >> 4) & 0x03

        value = self.push_register_pair(self.get_register_pair(pair, allow_af=True))

        opcode_t_states = 11
        # -----

        self.log_opcode(
            opcode=opcode,
            asm="PUSH qq",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Pushed {value:04X}",
            implemented=True,
        )

        return opcode_t_states

    # POP qq
    if opcode in (0xC1, 0xD1, 0xE1, 0xF1):
        # -----
        # Opcode logic:
        pair = (opcode >> 4) & 0x03

        value = self.pop16()

        self.set_register_pair(pair, value, allow_af=True)

        opcode_t_states = 10
        # -----

        self.log_opcode(
            opcode=opcode,
            asm="POP qq",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Popped {value:04X}",
            implemented=True,
        )

        return opcode_t_states

    return None
