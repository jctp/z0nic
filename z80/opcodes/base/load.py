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
            opcode_cycles = 2

            # Reads byte following opcode
            self.a = self.memory.read8(self.pc)
            self.pc += 1

            self.log_opcode(
                opcode = opcode,
                asm = "LD A, n",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"Loaded {self.a:04X} into A",
                implemented=True,
            )
            return opcode_cycles

        # LD B, n
        # Load n into B
        case 0x06:
            opcode_cycles = 2

            # Reads byte following opcode
            self.a = self.memory.read8(self.pc)
            self.pc += 1

            self.log_opcode(
                opcode = opcode,
                asm = "LD B, n",
                opcode_cycles = opcode_cycles,
                message = f"Loaded {self.a:04X} into B",
                implemented=True,
            )
            return opcode_cycles

        # LD HL, nn
        # TODO: Define
        # TODO: Implement
        case 0x21:
            opcode_cycles = 5

            # Opcode function goes here

            self.log_opcode(
                opcode = opcode,
                asm = "LD HL, n",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"",
                implemented=False,
            )
            return opcode_cycles

    return None