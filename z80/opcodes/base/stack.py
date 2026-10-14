# C1      POP BC
# D1      POP DE
# E1      POP HL
# F1      POP AF

# C5      PUSH BC
# D5      PUSH DE
# E5      PUSH HL
# F5      PUSH AF


def execute(self, opcode):
    # PUSH qq
    if opcode in (0xC5, 0xD5, 0xE5, 0xF5):
        # -----
        # Opcode logic:
        pair = (opcode >> 4) & 0x03

        value = self.push_register_pair(self.get_register_pair(pair))

        opcode_t_states = 11
        # -----

        self.log_opcode(
            opcode=opcode,
            asm="PUSH qq",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Pushed {value:04X}",
            implemented=True,
        )

        return opcode_t_states

    # POP qq
    if opcode in (0xC1, 0xD1, 0xE1, 0xF1):
        # -----
        # Opcode logic:
        pair = (opcode >> 4) & 0x03

        value = self.pop16()

        self.set_register_pair(pair, value)

        opcode_t_states = 10
        # -----

        self.log_opcode(
            opcode=opcode,
            asm="POP qq",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Popped {value:04X}",
            implemented=True,
        )

        return opcode_t_states

    return None
