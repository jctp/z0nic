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
    self.inc_pc(increment=1)

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

        # LD A,nn
        case 0x3A:
            return load.execute(self, opcode)

        # LD BC,nn
        # Read the next 16-bit immediate value into BC
        case 0x01:

            # -----
            # Opcode logic:
            value = self.load16_register(
                self.set_bc
            )
            opcode_t_states = 10
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD BC,nn",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Loaded {value:04X} into BC"
            )

        # LD DE,nn
        # Read the next 16-bit immediate value into DE
        case 0x11:

            # -----
            # Opcode logic:
            value = self.load16_register(
                self.set_de
            )
            opcode_t_states = 10
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD DE,nn",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Loaded {value:04X} into DE"
            )

        # LD HL,nn
        # Read the next 16-bit immediate value into HL
        case 0x21:

            # -----
            # Opcode logic:
            value = self.load16_register(
                self.set_hl
            )
            opcode_t_states = 10
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD HL,nn",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Loaded {value:04X} into HL"
            )

        # LD SP,nn
        # Read the next 16-bit immediate value into SP
        case 0x31:

            # -----
            # Opcode logic:
            value = self.load16_register(
                self.set_sp
            )
            opcode_t_states = 10
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD SP,nn",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Loaded {value:04X} into SP"
            )

        # LD IX,nn
        # Read the next 16-bit immediate value into IX
        case 0x21:

            # -----
            # Opcode logic:
            value = self.load16_register(
                self.set_ix
            )
            opcode_t_states = 14
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD IX,nn",
                prefix="DD",
                opcode_t_states=opcode_t_states,
                message=f"Loaded {value:04X} into IX"
            )

        # LD IY,nn
        # Read the next 16-bit immediate value into IY
        case 0x21:

            # -----
            # Opcode logic:
            value = self.load16_register(
                self.set_iy
            )
            opcode_t_states = 14
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD IY,nn",
                prefix="FD",
                opcode_t_states=opcode_t_states,
                message=f"Loaded {value:04X} into IY"
            )

        case _:
            self.opcode_not_implemented(
                f"DD {opcode:02X}",
                "Unknown mnemonic"
            )

    return None