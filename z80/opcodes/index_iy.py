# FD xx
# Prefix for IY instructions
def execute(self):
    opcode = self.memory.read8(self.pc)
    self.pc += 1

    match opcode:
        # Further prefix of CB
        case 0xCB:
            self.execute_prefix_0xFDCB()

        # Not implemented
        case _:
            self.opcode_not_implemented(f"FD {opcode:02X}", "Unknown mnemonic")

    return None
