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

            # -----
            # Opcode logic:
            self.interrupt_mode = 1
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="IM 1",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message="Interrupt mode set to 1",
                implemented=True,
            )
            return opcode_t_states

        # ED B0
        # LDIR
        case 0xB0:

            # -----
            # Opcode logic:
            hl = (self.h << 8) | self.l
            de = (self.d << 8) | self.e
            bc = (self.b << 8) | self.c

            start_hl = hl
            start_de = de
            bytes_copied = bc

            while bc > 0:

                value = self.memory.read8(hl)

                self.memory.write8(
                    de,
                    value
                )

                hl += 1
                de += 1
                bc -= 1

            self.h = (hl >> 8) & 0xFF
            self.l = hl & 0xFF

            self.d = (de >> 8) & 0xFF
            self.e = de & 0xFF

            self.b = (bc >> 8) & 0xFF
            self.c = bc & 0xFF

            opcode_t_states = 21 * bytes_copied
            # -----
            
            self.log_opcode(
                opcode=opcode,
                asm="LDIR",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message=(
                    f"Copied {bytes_copied} bytes "
                    f"from {start_hl:04X} "
                    f"to {start_de:04X}"
                ),
                implemented=True,
            )
            return opcode_t_states
        
        # Not implemented
        case _:
            self.opcode_not_implemented(f"ED {opcode:02X}", "Unknown mnemonic")

    return None
