# DD xx
# Prefix for IX instructions  
def execute(self):
    opcode = self.memory.read8(self.pc)
    self.pc += 1

    match opcode:

        case 0xCB:
            self.execute_prefix_0xDDCB()

        # Not implemented 
        case _:
            self.opcode_not_implemented(f"DD {opcode:02X}", "Unknown mnemonic")

    return None