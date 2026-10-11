# B8-BF   CP r
# FE      CP n


def execute(self, opcode):

    match opcode:
        # CP nn
        # TODO: Compare A with operand
        case 0xFE:
            opcode_t_states = 7

            # -----
            # Opcode logic:
            operand = self.memory.read8(self.pc)
            self.pc += 1
            result = self.a - operand
            self.flag_z = (result & 0xFF) == 0
            self.flag_c = self.a < operand
            self.flag_n = True
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="CP nn",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Compared {operand:02X} with A ({self.a:02X}) - was {self.flag_z:02X}",
                implemented=True,
            )
            return opcode_t_states

    return None
