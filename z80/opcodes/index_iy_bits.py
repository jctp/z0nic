# FD CB d xx
# IY + displacement bit operations
def execute(self):

    displacement = self.memory.read8(self.pc)
    self.inc_pc(increment=1)

    opcode = self.memory.read8(self.pc)
    self.inc_pc(increment=1)

    if displacement & 0x80:
        displacement -= 0x100

    address = (
        self.iy + displacement
    ) & 0xFFFF

    value = self.memory.read8(
        address
    )

    # BIT b,(IY+d)
    if 0x40 <= opcode <= 0x7F:

        opcode_t_states = 20

        # -----
        # Opcode logic:
        bit = (opcode >> 3) & 0x07

        self.flag_z = not (
            value & (1 << bit)
        )

        self.flag_h = True
        self.flag_n = False
        # -----

        self.log_opcode(
            opcode=opcode,
            asm="BIT b,(IY+d)",
            prefix="FD CB",
            opcode_t_states=opcode_t_states,
            message=(
                f"Tested bit {bit} "
                f"of value {value:02X} "
                f"at {address:04X}"
            ),
            implemented=True,
        )

        return opcode_t_states


    # RES b,(IY+d)
    if 0x80 <= opcode <= 0xBF:

        opcode_t_states = 23

        # -----
        # Opcode logic:
        bit = (opcode >> 3) & 0x07

        value &= ~(1 << bit)

        self.memory.write8(
            address,
            value
        )
        # -----

        self.log_opcode(
            opcode=opcode,
            asm="RES b,(IY+d)",
            prefix="FD CB",
            opcode_t_states=opcode_t_states,
            message=(
                f"Reset bit {bit} "
                f"at {address:04X}"
            ),
            implemented=True,
        )

        return opcode_t_states


    # SET b,(IY+d)
    if 0xC0 <= opcode <= 0xFF:

        opcode_t_states = 23

        # -----
        # Opcode logic:
        bit = (opcode >> 3) & 0x07

        value |= (1 << bit)

        self.memory.write8(
            address,
            value
        )
        # -----

        self.log_opcode(
            opcode=opcode,
            asm="SET b,(IY+d)",
            prefix="FD CB",
            opcode_t_states=opcode_t_states,
            message=(
                f"Set bit {bit} "
                f"at {address:04X}"
            ),
            implemented=True,
        )

        return opcode_t_states

    match opcode:
        case _:
            self.opcode_not_implemented(
                f"FD CB {displacement:02X} {opcode:02X}", "Unknown mnemonic"
            )

    return None
