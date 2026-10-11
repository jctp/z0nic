# 01    LD BC,nn
# 06    LD B,n
# 0E    LD C,n
# 11    LD DE,nn
# 16    LD D,n
# 21    LD HL,nn
# 26    LD H,n
# 31    LD SP,nn
# 3E    LD A,n

# 40-7F LD r,r


def execute(self, opcode):

    match opcode:
        # LD A, n
        # Load n into A
        case 0x3E:
            opcode_t_states = 13

            # -----
            # Opcode logic:
            # Reads byte following opcode
            self.a = self.memory.read8(self.pc)
            self.pc += 1
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD A, n",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Loaded {self.a:04X} into A",
                implemented=True,
            )
            return opcode_t_states

        # LD B, n
        # Load n into B
        case 0x06:
            opcode_t_states = 7

            # -----
            # Opcode logic:
            # Reads byte following opcode
            self.b = self.memory.read8(self.pc)
            self.pc += 1
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD B, n",
                opcode_t_states=opcode_t_states,
                message=f"Loaded {self.a:04X} into B",
                implemented=True,
            )
            return opcode_t_states

        # LD HL, nn
        # TODO: Define
        # TODO: Implement
        case 0x21:
            opcode_t_states = 5

            # Opcode function goes here

            self.log_opcode(
                opcode=opcode,
                asm="LD HL, n",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"",
                implemented=False,
            )
            return opcode_t_states

    return None
