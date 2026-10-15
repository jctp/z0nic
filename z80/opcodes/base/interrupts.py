# NOTE: The opcode table below is agent-generated. The code in this file is not.
# Stub = placeholder that raises via log_opcode(implemented=False).
#
# | Opcode | Mnemonic | Status      | Notes                                                 |
# |--------|----------|-------------|-------------------------------------------------------|
# | F3     | DI       | Implemented |                                                       |
# | FB     | EI       | Implemented |                                                       |



def execute(self, opcode):
    match opcode:
        # DI
        # Disable interrupts
        case 0xF3:
            opcode_t_states = 4

            # -----
            # Opcode logic:
            self.iff1 = False
            self.iff2 = False
            self.ei_pending = False
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="DI",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Disabled interrupts",
                implemented=True,
            )
            return opcode_t_states

        # EI
        # Enable interrupts after the next instruction
        case 0xFB:
            opcode_t_states = 4

            # -----
            # Opcode logic:
            self.ei_pending = True
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="EI",
                prefix="",
                opcode_t_states=opcode_t_states,
                message="Interrupts enabled (after next instruction)",
                implemented=True,
            )

            return opcode_t_states

    return None
