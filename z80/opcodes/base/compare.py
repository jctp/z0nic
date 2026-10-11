# B8-BF   CP r
# FE      CP n

def execute(self, opcode):

    match opcode:

        # CP nn
        # TODO: Define
        # TODO: Implement
        case 0xFE:
            opcode_cycles = 1 # TODO: Check correct

            # Opcode function goes here

            self.log_opcode(
                opcode = opcode,
                asm = "CP nn",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"",
                implemented=False,
            )
            return opcode_cycles

    return None