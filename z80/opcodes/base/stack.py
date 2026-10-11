# C1      POP BC
# D1      POP DE
# E1      POP HL
# F1      POP AF

# C5      PUSH BC
# D5      PUSH DE
# E5      PUSH HL
# F5      PUSH AF

def execute(self, opcode):

    match opcode:

        # PUSH HL
        # TODO: Define
        # TODO: Implement
        case 0xE5:
            opcode_cycles = 1 # TODO: Check correct

            # Opcode function goes here

            self.log_opcode(
                opcode = opcode,
                asm = "PUSH HL",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"",
                implemented=False,
            )
            return opcode_cycles

        # POP HL
        # TODO: Define
        # TODO: Implement
        case 0xE1:
            opcode_cycles = 1 # TODO: Check correct

            # Opcode function goes here

            self.log_opcode(
                opcode = opcode,
                asm = "POP HL",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"",
                implemented=False,
            )
            return opcode_cycles

    return None