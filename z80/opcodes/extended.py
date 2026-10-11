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
        # ED 56
        # Set interrupt mode to 1
        case 0x56:
            opcode_t_states = 2

            self.interrupt_mode = 1

            self.log_opcode(
                opcode=opcode,
                asm="IM 1",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message="Interrupt mode set to 1",
                implemented=True,
            )
            return opcode_t_states

        # Not implemented
        case _:
            self.opcode_not_implemented(f"ED {opcode:02X}", "Unknown mnemonic")

    return None
