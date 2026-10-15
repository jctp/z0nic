# B8-BF   CP r
# FE      CP n


def execute(self, opcode):
    match opcode:
        # CP nn
        # Compare A with operand

        case 0xFE:
            opcode_t_states = 7

            # -----
            # Opcode logic:
            operand = self.memory.read8(self.pc)
            self.inc_pc(increment=1)

            result = self.a - operand

            self.flag_s = bool((result & 0xFF) & 0x80)

            self.flag_z = (result & 0xFF) == 0

            self.flag_h = (self.a & 0x0F) < (operand & 0x0F)

            self.flag_pv = ((self.a ^ operand) & (self.a ^ result) & 0x80) != 0

            self.flag_c = result < 0

            self.flag_n = True
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="CP nn",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Compared {operand:02X} with A ({self.a:02X})",
                implemented=True,
            )

            return opcode_t_states

    # CP r
    if 0xB8 <= opcode <= 0xBF:
        opcode_t_states = 7 if (opcode & 0x07) == 6 else 4
        # TODO: Implement

        self.log_opcode(
            opcode=opcode,
            asm="CP r",
            prefix="",
            opcode_t_states=opcode_t_states,
            message="Not implemented",
            implemented=False,
        )

        return opcode_t_states

    return None
