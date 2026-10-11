# DD CB d xx
# IX + displacement bit operations 
def execute_0xDDCB(self):
    displacement = self.memory.read8(self.pc)
    self.pc += 1

    opcode = self.memory.read8(self.pc)
    self.pc += 1

    match opcode:

        case _:
            self.opcode_not_implemented(f"DD CB {displacement:02X} {opcode:02X}", "Unknown mnemonic")

    return None