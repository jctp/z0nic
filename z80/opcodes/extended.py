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

        # OTIR
        # Output, Increment, Repeat
        case 0xB3:

            opcode_t_states = 16

            # -----
            # Opcode logic:
            source_address = self.get_hl()

            value = self.memory.read8(source_address)

            self.io.write(
                self.c,
                value
            )

            self.set_hl(
                (source_address + 1) & 0xFFFF
            )

            self.b = (self.b - 1) & 0xFF

            if self.b != 0:
                self.pc -= 2
                opcode_t_states = 21
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="OTIR",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message=(
                    f"Output {value:02X} "
                    f"from {source_address:04X} "
                    f"to port {self.c:02X}, "
                    f"B now {self.b:02X}"
                ),
                implemented=True,
            )

            return opcode_t_states

        # LD (nn),DE
        # Store DE at the specified memory address
        case 0x53:

            opcode_t_states = 20

            # -----
            # Opcode logic:
            address = self.memory.read16(self.pc)
            self.pc += 2

            self.memory.write8(
                address,
                self.e
            )

            self.memory.write8(
                (address + 1) & 0xFFFF,
                self.d
            )
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD (nn),DE",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message=(
                    f"Stored DE ({self.get_de():04X}) "
                    f"to memory location {address:04X}"
                ),
                implemented=True,
            )

            return opcode_t_states
        
        # Not implemented
        case _:
            self.opcode_not_implemented(f"ED {opcode:02X}", "Unknown mnemonic")

    return None
