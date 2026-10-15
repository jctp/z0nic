# NOTE: The opcode table below is agent-generated. The code in this file is not.
# Stub = placeholder that raises via log_opcode(implemented=False).
#
# | Opcode | Mnemonic | Status      | Notes |
# |--------|----------|-------------|-------|
# | A0-A7  | AND r    | Stub        |       |
# | A8-AE  | XOR r    | Stub        |       |
# | AF     | XOR A    | Implemented |       |
# | B0-B7  | OR r     | Stub        |       |
# | E6     | AND n    | Stub        |       |
# | EE     | XOR n    | Stub        |       |
# | F6     | OR n     | Stub        |       |


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

    # AND r
    if 0xA0 <= opcode <= 0xA7:
        opcode_t_states = 7 if (opcode & 0x07) == 6 else 4
        # TODO: Implement

        self.log_opcode(
            opcode=opcode,
            asm="AND r",
            prefix="",
            opcode_t_states=opcode_t_states,
            message="Not implemented",
            implemented=False,
        )

        return opcode_t_states

    # XOR r
    # AF (XOR A) is handled above
    if 0xA8 <= opcode <= 0xAE:
        opcode_t_states = 7 if (opcode & 0x07) == 6 else 4
        # TODO: Implement

        self.log_opcode(
            opcode=opcode,
            asm="XOR r",
            prefix="",
            opcode_t_states=opcode_t_states,
            message="Not implemented",
            implemented=False,
        )

        return opcode_t_states

    # OR r
    if 0xB0 <= opcode <= 0xB7:
        opcode_t_states = 7 if (opcode & 0x07) == 6 else 4
        # TODO: Implement

        self.log_opcode(
            opcode=opcode,
            asm="OR r",
            prefix="",
            opcode_t_states=opcode_t_states,
            message="Not implemented",
            implemented=False,
        )

        return opcode_t_states

    # AND n / XOR n / OR n
    if opcode in (0xE6, 0xEE, 0xF6):
        opcode_t_states = 7
        # TODO: Implement

        asm = {0xE6: "AND n", 0xEE: "XOR n", 0xF6: "OR n"}[opcode]

        self.log_opcode(
            opcode=opcode,
            asm=asm,
            prefix="",
            opcode_t_states=opcode_t_states,
            message="Not implemented",
            implemented=False,
        )

        return opcode_t_states

    return None
