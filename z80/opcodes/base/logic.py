# A0-A7  AND r
# A8-AF  XOR r
# B0-B7  OR r

# E6      AND n
# EE      XOR n
# F6      OR n


def execute(self, opcode):
    match opcode:
        # XOR A
        # Exclusive OR A with itself
        # ...which will always be zero, so this essentially clears A
        case 0xAF:
            opcode_t_states = 4

            # -----
            # Opcode logic:
            self.a ^= self.a

            self.flag_s = False
            self.flag_z = True
            self.flag_h = False
            self.flag_pv = True
            self.flag_n = False
            self.flag_c = False
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="XOR A",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"A cleared to 00",
                implemented=True,
            )
            return opcode_t_states

    return None
