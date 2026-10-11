# BIT
# SET
# RES

# RLC
# RRC
# RL
# RR

# SLA
# SRA
# SRL

def execute(self):
    opcode = self.memory.read8(self.pc)
    self.pc += 1

    match opcode:
        # ROTATES AND SHIFTS

        # BIT

        # RES

        # SET

        # Not implemented 
        case _:
            self.opcode_not_implemented(f"CB {opcode:02X}", "Unknown mnemonic")

    return None
