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

        case _:
            pass

    return None
