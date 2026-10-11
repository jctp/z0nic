# 80-87   ADD A,r
# 88-8F   ADC A,r

# 90-97   SUB r
# 98-9F   SBC A,r

# C6       ADD A,n
# CE       ADC A,n
# D6       SUB n
# DE       SBC A,n


def execute(self, opcode):

    match opcode:
        # ADD A,B
        # TODO: Define
        # TODO: Implement
        case 0x80:
            opcode_t_states = 1  # TODO: Check correct

            # Opcode function goes here

            self.log_opcode(
                opcode=opcode,
                asm="ADD A,B",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"",
                implemented=False,
            )
            return opcode_t_states

        # SUB B
        # TODO: Define
        # TODO: Implement
        case 0x90:
            opcode_t_states = 1  # TODO: Check correct

            # Opcode function goes here

            self.log_opcode(
                opcode=opcode,
                asm="SUB B",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"",
                implemented=False,
            )
            return opcode_t_states

        # INC B
        # TODO: Define
        # TODO: Implement
        case 0x04:
            opcode_t_states = 1  # TODO: Check correct

            # Opcode function goes here

            self.log_opcode(
                opcode=opcode,
                asm="INC B",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"",
                implemented=False,
            )
            return opcode_t_states

        # DEC B
        # TODO: Define
        # TODO: Implement
        case 0x05:
            opcode_t_states = 1  # TODO: Check correct

            # Opcode function goes here

            self.log_opcode(
                opcode=opcode,
                asm="DEC B",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"",
                implemented=False,
            )
            return opcode_t_states

    return None
