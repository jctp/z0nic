# NOTE: The opcode table below is agent-generated. The code in this file is not.
# Stub = placeholder that raises via log_opcode(implemented=False).
#
# | Opcode | Mnemonic | Status      | Notes |
# |--------|----------|-------------|-------|
# | 00     | NOP      | Implemented |       |
# | 76     | HALT     | Stub        |       |


def execute(self, opcode):
    match opcode:
        # NOP
        # No operation
        case 0x00:
            opcode_t_states = 1
            self.log_opcode(
                opcode=opcode,
                asm="NOP",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"No operation",
                implemented=True,
            )
            return opcode_t_states

        # HALT
        # Suspend the CPU until an interrupt occurs
        case 0x76:
            opcode_t_states = 4
            # TODO: Implement
            self.log_opcode(
                opcode=opcode,
                asm="HALT",
                prefix="",
                opcode_t_states=opcode_t_states,
                message="Not implemented",
                implemented=False,
            )
            return opcode_t_states

        case _:
            pass

    return None
