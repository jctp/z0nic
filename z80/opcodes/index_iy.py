from z80.opcodes.base import (
    load,
    arithmetic,
    compare,
    jumps,
    stack,
    logic,
    subroutines,
    interrupts,
)

from z80.opcodes import control, bit_operations, index_iy_bits

# FD xx
# Prefix for IY instructions
#
# NOTE: The opcode table below is agent-generated. The code in this file is not.
# Stub = placeholder that raises via log_opcode(implemented=False).
# Opcodes are the byte(s) after the FD prefix.
#
# | Opcode                     | Mnemonic              | Status      | Notes                                |
# |----------------------------|-----------------------|-------------|--------------------------------------|
# | 00                         | NOP                   | Implemented | Prefix ignored                       |
# | 02, 12                     | LD (BC),A / LD (DE),A | Implemented | Prefix ignored                       |
# | 08                         | EX AF,AF'             | Implemented | Prefix ignored                       |
# | 21                         | LD IY,nn              | Implemented |                                      |
# | 22                         | LD (nn),IY            | Implemented | Bug: returns None, so no cycle count |
# | 23                         | INC IY                | Implemented |                                      |
# | 2A                         | LD IY,(nn)            | Implemented | Bug: returns None, so no cycle count |
# | 32                         | LD (nn),A             | Implemented | Prefix ignored                       |
# | 36                         | LD (IY+d),n           | Implemented |                                      |
# | 46, 4E, 56, 5E, 66, 6E, 7E | LD r,(IY+d)           | Implemented |                                      |
# | 70-75, 77                  | LD (IY+d),r           | Implemented |                                      |
# | C9                         | RET                   | Implemented | Prefix ignored                       |
# | E1                         | POP IY                | Implemented |                                      |
# | E5                         | PUSH IY               | Implemented |                                      |
# | CB                         | IY bit table          | Implemented | Hands off to index_iy_bits.py        |
# | Any other                  | -                     | Not handled | Raises 'IY instruction'              |


def execute(self):
    opcode = self.memory.read8(self.pc)
    self.inc_pc(increment=1)

    # FD 70-FD 75, FD 77
    # LD (IY+d),r
    if 0x70 <= opcode <= 0x77 and opcode != 0x76:
        opcode_t_states = 19

        # -----
        # Opcode logic:
        displacement = self.memory.read8(self.pc)
        self.inc_pc(increment=1)

        if displacement & 0x80:
            displacement -= 0x100

        source = opcode & 0x07

        value = self.get_register(source)

        address = (self.iy + displacement) & 0xFFFF

        self.memory.write8(address, value)
        # -----

        self.log_opcode(
            opcode=opcode,
            asm="LD (IY+d),r",
            prefix="FD",
            opcode_t_states=opcode_t_states,
            message=(f"Stored {value:02X} to {address:04X} (IY{displacement:+d})"),
            implemented=True,
        )

        return opcode_t_states

    match opcode:
        # FDCB table
        case 0xCB:
            return index_iy_bits.execute(self)

        # Instructions where FD has no effect

        case 0x00:
            return control.execute(self, opcode)

        case 0x08:
            return bit_operations.execute(self, opcode)

        case 0x02 | 0x12 | 0x32:
            return load.execute(self, opcode)

        case 0xC9:
            return subroutines.execute(self, opcode)

        # LD IY,nn
        case 0x21:
            opcode_t_states = 14

            # -----
            # Opcode logic:
            low = self.memory.read8(self.pc)
            self.inc_pc(increment=1)

            high = self.memory.read8(self.pc)
            self.inc_pc(increment=1)

            self.iy = (high << 8) | low
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD IY,nn",
                prefix="FD",
                opcode_t_states=opcode_t_states,
                message=f"Loaded {self.iy:04X} into IY",
                implemented=True,
            )

            return opcode_t_states
        
        # FD 46, 4E, 56, 5E, 66, 6E, 7E
        # LD r,(IY+d)
        case 0x46 | 0x4E | 0x56 | 0x5E | 0x66 | 0x6E | 0x7E:
            opcode_t_states = 19

            # -----
            # Opcode logic:
            displacement = self.memory.read8(self.pc)
            self.inc_pc(increment=1)

            if displacement & 0x80:
                displacement -= 0x100

            address = (self.iy + displacement) & 0xFFFF

            value = self.memory.read8(address)

            destination = (opcode >> 3) & 0x07

            self.set_register(destination, value)
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD r,(IY+d)",
                prefix="FD",
                opcode_t_states=opcode_t_states,
                message=(
                    f"Loaded {value:02X} from {address:04X} (IY{displacement:+d})"
                ),
                implemented=True,
            )

            return opcode_t_states

        # LD A,(IY+d)
        # Unreachable: FD 7E is matched by LD r,(IY+d) above
        case 0x7E:
            opcode_t_states = 19

            # -----
            # Opcode logic:
            displacement = self.memory.read8(self.pc)
            self.inc_pc(increment=1)

            if displacement & 0x80:
                displacement -= 0x100

            address = (self.iy + displacement) & 0xFFFF

            self.a = self.memory.read8(address)
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD A,(IY+d)",
                prefix="FD",
                opcode_t_states=opcode_t_states,
                message=(
                    f"Loaded {self.a:02X} from {address:04X} (IY{displacement:+d})"
                ),
                implemented=True,
            )

            return opcode_t_states

        # LD (nn),IY
        case 0x22:
            # -----
            # Opcode logic:

            address = self.store_register_pair(self.iy)

            opcode_t_states = 20

            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD (nn),IY",
                prefix="FD",
                opcode_t_states=opcode_t_states,
                message=(f"Stored IY ({self.iy:04X}) into memory at {address:04X}"),
            )

        # LD IY,(nn)
        case 0x2A:
            # -----
            # Opcode logic:

            value, address = self.load_register_pair(self.set_iy)

            opcode_t_states = 20

            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD IY,(nn)",
                prefix="FD",
                opcode_t_states=opcode_t_states,
                message=(f"Loaded {value:04X} from memory at {address:04X} into IY"),
            )

        # FD 36
        # LD (IY+d),n
        case 0x36:
            opcode_t_states = 19

            # -----
            # Opcode logic:
            displacement = self.memory.read8(self.pc)
            self.inc_pc(increment=1)

            if displacement & 0x80:
                displacement -= 0x100

            value = self.memory.read8(self.pc)
            self.inc_pc(increment=1)

            address = (self.iy + displacement) & 0xFFFF

            self.memory.write8(address, value)
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD (IY+d),n",
                prefix="FD",
                opcode_t_states=opcode_t_states,
                message=(f"Stored {value:02X} to {address:04X} (IY{displacement:+d})"),
                implemented=True,
            )

            return opcode_t_states

        # PUSH IY
        case 0xE5:
            # -----
            # Opcode logic:
            value = self.push_register_pair(self.iy)

            opcode_t_states = 15
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="PUSH IY",
                prefix="FD",
                opcode_t_states=opcode_t_states,
                message=f"Pushed {value:04X}",
                implemented=True,
            )

            return opcode_t_states

        # POP IY
        case 0xE1:
            # -----
            # Opcode logic:
            value = self.pop_register_pair(self.set_iy)

            opcode_t_states = 14
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="POP IY",
                prefix="FD",
                opcode_t_states=opcode_t_states,
                message=f"Popped {value:04X}",
                implemented=True,
            )

            return opcode_t_states

        # INC IY
        case 0x23:
            # -----
            # Opcode logic:
            value = self.increment_register_pair(lambda: self.iy, self.set_iy)

            opcode_t_states = 10
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="INC IY",
                prefix="FD",
                opcode_t_states=opcode_t_states,
                message=f"Incremented IY to {value:04X}",
                implemented=True,
            )

            return opcode_t_states

        # Real IY instruction
        case _:
            self.opcode_not_implemented(f"FD {opcode:02X}", "IY instruction")

    return None
