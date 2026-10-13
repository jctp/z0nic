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

from z80.opcodes import (
    control,
    bit_operations,
    index_iy_bits
)

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

        address = (
            self.iy + displacement
        ) & 0xFFFF

        self.memory.write8(
            address,
            value
        )
        # -----

        self.log_opcode(
            opcode=opcode,
            asm="LD (IY+d),r",
            prefix="FD",
            opcode_t_states=opcode_t_states,
            message=(
                f"Stored {value:02X} "
                f"to {address:04X} "
                f"(IY{displacement:+d})"
            ),
            implemented=True,
        )

        return opcode_t_states


    # FD 46-FD 7E
    # LD r,(IY+d)
    if opcode in (
        0x46,
        0x4E,
        0x56,
        0x5E,
        0x66,
        0x6E,
        0x7E,
    ):

        opcode_t_states = 19

        # -----
        # Opcode logic:
        displacement = self.memory.read8(self.pc)
        self.inc_pc(increment=1)

        if displacement & 0x80:
            displacement -= 0x100

        address = (
            self.iy + displacement
        ) & 0xFFFF

        value = self.memory.read8(
            address
        )

        destination = (
            (opcode >> 3) & 0x07
        )

        self.set_register(
            destination,
            value
        )
        # -----

        self.log_opcode(
            opcode=opcode,
            asm="LD r,(IY+d)",
            prefix="FD",
            opcode_t_states=opcode_t_states,
            message=(
                f"Loaded {value:02X} "
                f"from {address:04X} "
                f"(IY{displacement:+d})"
            ),
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
                    f"Loaded {self.a:02X} "
                    f"from {address:04X} "
                    f"(IY{displacement:+d})"
                ),
                implemented=True,
            )

            return opcode_t_states

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

            address = (
                self.iy + displacement
            ) & 0xFFFF

            self.memory.write8(
                address,
                value
            )
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD (IY+d),n",
                prefix="FD",
                opcode_t_states=opcode_t_states,
                message=(
                    f"Stored {value:02X} "
                    f"to {address:04X} "
                    f"(IY{displacement:+d})"
                ),
                implemented=True,
            )

            return opcode_t_states

        # Real IY instruction
        case _:
            self.opcode_not_implemented(
                f"FD {opcode:02X}",
                "IY instruction"
            )

    return None