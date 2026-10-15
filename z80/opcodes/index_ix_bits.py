# DD CB d xx
# IX + displacement bit operations
#
# NOTE: The opcode table below is agent-generated. The code in this file is not.
# Stub = placeholder that raises via log_opcode(implemented=False).
# Opcodes are the byte after the displacement.
#
# | Opcode | Mnemonic                  | Status      | Notes |
# |--------|---------------------------|-------------|-------|
# | 40-7F  | BIT b,(IX+d)              | Implemented |       |
# | 00-3F  | Rotates and shifts (IX+d) | Not handled |       |
# | 80-BF  | RES b,(IX+d)              | Not handled |       |
# | C0-FF  | SET b,(IX+d)              | Not handled |       |
def execute(self):
    displacement = self.memory.read8(self.pc)
    self.inc_pc(increment=1)

    opcode = self.memory.read8(self.pc)
    self.inc_pc(increment=1)

    if (opcode & 0xC0) == 0x40:
        bit = (opcode >> 3) & 0x07

        self.bit_ix_displacement(displacement, bit)

        opcode_t_states = 20

        self.log_opcode(
            opcode=opcode,
            asm=f"BIT {bit},(IX+d)",
            prefix="DD CB",
            opcode_t_states=opcode_t_states,
            message=f"Tested bit {bit} at IX+{displacement:02X}",
        )

        return opcode_t_states

    match opcode:
        case _:
            self.opcode_not_implemented(
                f"DD CB {displacement:02X} {opcode:02X}", "Unknown mnemonic"
            )

    return None
