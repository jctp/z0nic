# A0-A7  AND r
# A8-AF  XOR r
# B0-B7  OR r

# E6      AND n
# EE      XOR n
# F6      OR n


def execute(self, opcode):

    match opcode:
        # XOR A
        # TODO: Define
        # TODO: Implement
        case 0xAF:
            opcode_t_states = 1  # TODO: Check correct

            # Opcode function goes here

            self.log_opcode(
                opcode=opcode,
                asm="XOR A",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"",
                implemented=False,
            )
            return opcode_t_states

    return None
