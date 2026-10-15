from z80.opcodes.base import logic, compare, jumps, load

from z80.opcodes import index_ix_bits


# DD xx
# Prefix for IX instructions
#
# NOTE: The opcode table below is agent-generated. The code in this file is not.
# Stub = placeholder that raises via log_opcode(implemented=False).
# Opcodes are the byte(s) after the DD prefix.
#
# | Opcode                     | Mnemonic              | Status      | Notes                                                    |
# |----------------------------|-----------------------|-------------|----------------------------------------------------------|
# | 01, 11, 21                 | LD rr,nn (BC, DE, HL) | Implemented | Prefix ignored. 21 should be LD IX,nn, which is shadowed |
# | 22                         | LD (nn),IX            | Implemented | Bug: returns None, so no cycle count                     |
# | 23                         | INC IX                | Implemented |                                                          |
# | 2A                         | LD IX,(nn)            | Implemented | Bug: returns None, so no cycle count                     |
# | 31                         | LD SP,nn              | Implemented | Broken: calls Z80.set_sp(), which does not exist         |
# | 46, 4E, 56, 5E, 66, 6E, 7E | LD r,(IX+d)           | Implemented |                                                          |
# | 70-75, 77                  | LD (IX+d),r           | Implemented |                                                          |
# | E1                         | POP IX                | Implemented |                                                          |
# | E5                         | PUSH IX               | Implemented |                                                          |
# | 18                         | JR e                  | Implemented | Prefix ignored                                           |
# | 3A                         | LD A,(nn)             | Stub        | Prefix ignored                                           |
# | E6                         | AND n                 | Stub        | Prefix ignored                                           |
# | EE                         | XOR n                 | Stub        | Prefix ignored                                           |
# | F6                         | OR n                  | Stub        | Prefix ignored                                           |
# | FE                         | CP n                  | Implemented | Prefix ignored                                           |
# | CB                         | IX bit table          | Implemented | Hands off to index_ix_bits.py                            |
# | Any other                  | -                     | Not handled | Raises 'Unknown mnemonic'                                |
def execute(self):
    opcode = self.memory.read8(self.pc)
    self.inc_pc(increment=1)

    match opcode:
        case 0xCB:
            return index_ix_bits.execute(self)

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

        # LD A,(nn)
        case 0x3A:
            return load.execute(self, opcode)

        # LD BC,nn
        # Read the next 16-bit immediate value into BC
        case 0x01:
            # -----
            # Opcode logic:
            value = self.load16_register(self.set_bc)
            opcode_t_states = 10
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD BC,nn",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Loaded {value:04X} into BC",
            )

            return opcode_t_states

        # LD DE,nn
        # Read the next 16-bit immediate value into DE
        case 0x11:
            # -----
            # Opcode logic:
            value = self.load16_register(self.set_de)
            opcode_t_states = 10
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD DE,nn",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Loaded {value:04X} into DE",
            )

            return opcode_t_states

        # LD HL,nn
        # Read the next 16-bit immediate value into HL
        # DD 21 is really LD IX,nn, but this case matches first
        case 0x21:
            # -----
            # Opcode logic:
            value = self.load16_register(self.set_hl)
            opcode_t_states = 10
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD HL,nn",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Loaded {value:04X} into HL",
            )

            return opcode_t_states

        # LD (nn),IX
        case 0x22:
            # -----
            # Opcode logic:

            address = self.store_register_pair(self.ix)

            opcode_t_states = 20

            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD (nn),IX",
                prefix="DD",
                opcode_t_states=opcode_t_states,
                message=(f"Stored IX ({self.ix:04X}) into memory at {address:04X}"),
            )

        # LD IX,(nn)
        case 0x2A:
            # -----
            # Opcode logic:

            value, address = self.load_register_pair(self.set_ix)

            opcode_t_states = 20

            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD IX,(nn)",
                prefix="DD",
                opcode_t_states=opcode_t_states,
                message=(f"Loaded {value:04X} from memory at {address:04X} into IX"),
            )

        # LD SP,nn
        # Read the next 16-bit immediate value into SP
        case 0x31:
            # -----
            # Opcode logic:
            value = self.load16_register(self.set_sp)
            opcode_t_states = 10
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD SP,nn",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Loaded {value:04X} into SP",
            )

            return opcode_t_states

        # LD IX,nn
        # Read the next 16-bit immediate value into IX
        # Unreachable: DD 21 is matched by LD HL,nn above
        case 0x21:
            # -----
            # Opcode logic:
            value = self.load16_register(self.set_ix)
            opcode_t_states = 14
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD IX,nn",
                prefix="DD",
                opcode_t_states=opcode_t_states,
                message=f"Loaded {value:04X} into IX",
            )

            return opcode_t_states

        # LD IY,nn
        # Read the next 16-bit immediate value into IY
        # Unreachable: this is FD 21, not a DD opcode
        case 0x21:
            # -----
            # Opcode logic:
            value = self.load16_register(self.set_iy)
            opcode_t_states = 14
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD IY,nn",
                prefix="FD",
                opcode_t_states=opcode_t_states,
                message=f"Loaded {value:04X} into IY",
            )

            return opcode_t_states

        # LD r,(IX+d)
        case 0x46 | 0x4E | 0x56 | 0x5E | 0x66 | 0x6E | 0x7E:
            opcode_t_states = 16

            register_names = [
                "B",
                "C",
                "D",
                "E",
                "H",
                "L",
                "(HL)",  # This is impossible but here for spacing
                "A",
            ]

            displacement = self.memory.read8(self.pc)
            self.inc_pc()

            register = (opcode >> 3) & 0x07

            value = self.load_register_from_ix_displacement(displacement, register)

            signed_displacement = (
                displacement if displacement < 0x80 else displacement - 0x100
            )

            self.log_opcode(
                opcode=opcode,
                asm=f"LD {register_names[register]},(IX+d)",
                prefix="DD",
                opcode_t_states=opcode_t_states,
                message=(
                    f"Loaded {value:02X} from "
                    f"(IX+{signed_displacement:02X}) into "
                    f"{register_names[register]}"
                ),
            )

            return opcode_t_states

        # LD (IX+d),r
        case 0x70 | 0x71 | 0x72 | 0x73 | 0x74 | 0x75 | 0x77:
            opcode_t_states = 19

            register_names = ["B", "C", "D", "E", "H", "L", "(HL)", "A"]

            displacement = self.memory.read8(self.pc)
            self.inc_pc()

            register = opcode & 0x07

            value = self.store_register_to_ix_displacement(displacement, register)

            signed_displacement = (
                displacement if displacement < 0x80 else displacement - 0x100
            )

            self.log_opcode(
                opcode=opcode,
                asm=f"LD (IX+d),{register_names[register]}",
                prefix="DD",
                opcode_t_states=opcode_t_states,
                message=(
                    f"Stored {value:02X} from "
                    f"{register_names[register]} into "
                    f"(IX+{signed_displacement:02X})"
                ),
            )

            return opcode_t_states

        # PUSH IX
        case 0xE5:
            # -----
            # Opcode logic:
            value = self.push_register_pair(self.ix)

            opcode_t_states = 15
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="PUSH IX",
                prefix="DD",
                opcode_t_states=opcode_t_states,
                message=f"Pushed {value:04X}",
                implemented=True,
            )

            return opcode_t_states

        # POP IX
        case 0xE1:
            # -----
            # Opcode logic:
            value = self.pop_register_pair(self.set_ix)

            opcode_t_states = 14
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="POP IX",
                prefix="DD",
                opcode_t_states=opcode_t_states,
                message=f"Popped {value:04X}",
                implemented=True,
            )

            return opcode_t_states

        # INC IX
        case 0x23:
            # -----
            # Opcode logic:
            value = self.increment_register_pair(lambda: self.ix, self.set_ix)

            opcode_t_states = 10
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="INC IX",
                prefix="DD",
                opcode_t_states=opcode_t_states,
                message=f"Incremented IX to {value:04X}",
                implemented=True,
            )

            return opcode_t_states

        case _:
            self.opcode_not_implemented(f"DD {opcode:02X}", "Unknown mnemonic")

    return None
