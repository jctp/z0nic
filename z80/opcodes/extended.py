# LDI
# LDIR
# LDD
# LDDR

# CPIR
# CPDR

# NEG

# IN
# OUT

# RETN
# RETI

def execute(self):
    opcode = self.memory.read8(self.pc)
    self.pc += 1

    match opcode:

        # Not implemented 
        case _:
            self.opcode_not_implemented(f"ED {opcode:02X}", "Unknown mnemonic")

    return None