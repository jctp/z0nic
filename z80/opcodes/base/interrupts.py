# F3      DI
# FB      EI

# ED 45   RETN
# ED 4D   RETI


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

    return None
