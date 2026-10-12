from z80.opcodes.base import load

# FD xx
# Prefix for IY instructions
def execute(self):
    opcode = self.memory.read8(self.pc)
    self.pc += 1

    match opcode:

        # For this, it's essentially just a LD (nn),A so we push it there
        case 0x32:
            return load.execute(self, opcode)

        # Further prefix of CB
        case 0xCB:
            self.execute_prefix_0xFDCB()

        # Not implemented
        case _:
            self.opcode_not_implemented(f"FD {opcode:02X}", "Unknown mnemonic")

    return None
