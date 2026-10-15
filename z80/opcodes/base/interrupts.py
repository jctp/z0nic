# F3      DI
# FB      EI

# ED 45   RETN
# ED 4D   RETI


def execute(self, opcode):
    match opcode:
        # DI
        # Disable interrupts
        case 0xF3:
            opcode_t_states = 4

            # -----
            # Opcode logic:
            self.iff1 = False
            self.iff2 = False
            self.ei_pending = False
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="DI",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Disabled interrupts",
                implemented=True,
            )
            return opcode_t_states

        # EI
        # Enable interrupts after the next instruction
        case 0xFB:
            opcode_t_states = 4

            # -----
            # Opcode logic:
            self.ei_pending = True
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="EI",
                prefix="",
                opcode_t_states=opcode_t_states,
                message="Interrupts enabled (after next instruction)",
                implemented=True,
            )

            return opcode_t_states

        # ED 45
        # RETN
        case 0x45:
            opcode_t_states = 14

            # -----
            # Opcode logic:
            self.iff1 = self.iff2

            address = self.pop16()

            self.pc = address
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="RETN",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message=f"Returned to {address:04X}",
                implemented=True,
            )

            return opcode_t_states

        # ED 4D
        # RETI
        case 0x4D:
            opcode_t_states = 14

            # -----
            # Opcode logic:
            address = self.pop16()

            self.pc = address
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="RETI",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message=f"Returned to {address:04X}",
                implemented=True,
            )

            return opcode_t_states

    return None
