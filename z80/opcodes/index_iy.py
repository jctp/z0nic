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


def execute(self):
    opcode = self.memory.read8(self.pc)
    self.inc_pc(increment=1)

    # FD 70-FD 77
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
            index_iy_bits.execute(self)

        # Instructions where FD has no effect
        case 0x00:
            return control.execute(self, opcode)

        case 0x08:
            return bit_operations.execute(self, opcode)

        case 0x01 | 0x11 | 0x21 | 0x31:
            return load.execute(self, opcode)

        case 0x02 | 0x12 | 0x32:
            return load.execute(self, opcode)

        case 0xC9:
            return subroutines.execute(self, opcode)

        # FD 46-FD 7E
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
