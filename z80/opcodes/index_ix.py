from z80.opcodes.base import (
    logic,
    compare,
    jumps,
    load
)

from z80.opcodes import (
    index_ix_bits
)

# DD xx
# Prefix for IX instructions
def execute(self):

    opcode = self.memory.read8(self.pc)
    self.pc += 1

    match opcode:
        case 0xCB:
            index_ix_bits.execute(self)

        # AND n
        case 0xE6:
            return logic.execute(self, opcode)

        # OR n
        case 0xF6:
            return logic.execute(self, opcode)

        # XOR n
        case 0xEE:
            return logic.execute(self, opcode)

        # CP n
        case 0xFE:
            return compare.execute(self, opcode)

        # JR e
        case 0x18:
            return jumps.execute(self, opcode)

        # LD A, (nn)
        case 0x3A:
            return load.execute(self, opcode)

        case _:
            self.opcode_not_implemented(
                f"DD {opcode:02X}",
                "Unknown mnemonic"
            )

    return None