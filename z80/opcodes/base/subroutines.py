# CD      CALL nn
# C4      CALL NZ

# CC      CALL Z

# C9      RET

# C0      RET NZ
# C8      RET Z


def execute(self, opcode):

    match opcode:

        # CALL nn nn
        # TODO: Define
        # TODO: Implement
        case 0xCD:
            opcode_cycles = 1 # TODO: Check correct

            # Opcode function goes here

            self.log_opcode(
                opcode = opcode,
                asm = "CALL nn nn",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"",
                implemented=False,
            )
            return opcode_cycles

        # RET
        # TODO: Define
        # TODO: Implement
        case 0xC9:
            opcode_cycles = 1 # TODO: Check correct

            # Opcode function goes here

            self.log_opcode(
                opcode = opcode,
                asm = "RET",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"",
                implemented=False,
            )
            return opcode_cycles

    return None