# CD      CALL nn
# C4      CALL NZ

# CC      CALL Z

# C9      RET

# C0      RET NZ
# C8      RET Z


def execute(self, opcode):

    match opcode:
        # CALL nn nn
        # TODO: Define
        # TODO: Implement
        case 0xCD:
            opcode_t_states = 1  # TODO: Check correct

            # Opcode function goes here

            self.log_opcode(
                opcode=opcode,
                asm="CALL nn nn",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"",
                implemented=False,
            )
            return opcode_t_states

        # RET
        # TODO: Define
        # TODO: Implement
        case 0xC9:
            opcode_t_states = 1  # TODO: Check correct

            # Opcode function goes here

            self.log_opcode(
                opcode=opcode,
                asm="RET",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"",
                implemented=False,
            )
            return opcode_t_states

    return None
