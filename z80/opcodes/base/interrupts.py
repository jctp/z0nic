# F3      DI
# FB      EI

# ED 45   RETN
# ED 4D   RETI

def execute(self, opcode):

    match opcode:

        # DI
        # Disable interrupts
        case 0xF3:
            opcode_cycles = 4

            self.iff1 = False
            self.iff2 = False

            self.log_opcode(
                opcode = opcode,
                asm = "DI",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"Disabled interrupts",
                implemented=True,
            )
            return opcode_cycles

    return None