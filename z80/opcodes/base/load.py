# NOTE: The opcode table below is agent-generated. The code in this file is not.
# Stub = placeholder that raises via log_opcode(implemented=False).
#
# | Opcode                     | Mnemonic              | Status      | Notes                   |
# |----------------------------|-----------------------|-------------|-------------------------|
# | 01, 11, 21                 | LD rr,nn (BC, DE, HL) | Implemented |                         |
# | 31                         | LD SP,nn              | Implemented | Bug: loads AF, not SP   |
# | 02, 12                     | LD (BC),A / LD (DE),A | Implemented |                         |
# | 0A, 1A                     | LD A,(BC) / LD A,(DE) | Implemented |                         |
# | 06, 0E, 16, 1E, 26, 2E, 3E | LD r,n                | Implemented |                         |
# | 22                         | LD (nn),HL            | Implemented |                         |
# | 2A                         | LD HL,(nn)            | Implemented |                         |
# | 32                         | LD (nn),A             | Implemented |                         |
# | 36                         | LD (HL),n             | Stub        |                         |
# | 3A                         | LD A,(nn)             | Stub        |                         |
# | 40-75, 77-7F               | LD r,r                | Stub        | 76 is HALT (control.py) |
# | F9                         | LD SP,HL              | Implemented |                         |


def execute(self, opcode):
    # LD r,n
    # 8-bit loads
    if opcode in (
        0x06,
        0x0E,
        0x16,
        0x1E,
        0x26,
        0x2E,
        0x3E,
    ):
        # -----
        # Opcode logic:
        dest = (opcode >> 3) & 0x07
        value = self.memory.read8(self.pc)
        self.inc_pc(increment=1)
        self.set_register(dest, value)
        # -----

        opcode_t_states = 7

        self.log_opcode(
            opcode=opcode,
            asm="LD r,n",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Value {value:02X} loaded to register {dest:02X}",
            implemented=True,
        )
        return opcode_t_states

    # LD rr,nn
    # 16-bit loads
    if opcode in (0x01, 0x11, 0x21, 0x31):
        opcode_t_states = 10

        # -----
        # Opcode logic:
        low = self.memory.read8(self.pc)
        self.inc_pc(increment=1)
        high = self.memory.read8(self.pc)
        self.inc_pc(increment=1)
        value = (high << 8) | low
        dest = (opcode >> 4) & 0x03
        self.set_register_pair(dest, value)
        # -----

        self.log_opcode(
            opcode=opcode,
            asm="LD rr,nn",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Loaded {value:04X} into {dest:02X}",
            implemented=True,
        )

        return opcode_t_states

    # LD (BC),A / LD (DE),A
    if opcode in (0x02, 0x12):
        opcode_t_states = 7

        # -----
        # Opcode logic:
        pair = (opcode >> 4) & 0x01
        if pair == 0:
            address = (self.b << 8) | self.c
        else:
            address = (self.d << 8) | self.e
        self.memory.write8(address, self.a)
        # -----

        self.log_opcode(
            opcode=opcode,
            asm="LD rr,A",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Loaded {pair:04X} into {address:04X}",
            implemented=True,
        )

        return opcode_t_states

    # LD A,(rr)
    if opcode in (0x0A, 0x1A):
        opcode_t_states = 7

        # -----
        # Opcode logic:
        pair = (opcode >> 4) & 0x01

        if pair == 0:
            address = (self.b << 8) | self.c
            pair_name = "BC"
        else:
            address = (self.d << 8) | self.e
            pair_name = "DE"

        self.a = self.memory.read8(address)
        # -----

        self.log_opcode(
            opcode=opcode,
            asm="LD A,(rr)",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Loaded {self.a:02X} from ({pair_name}) at {address:04X} into A",
            implemented=True,
        )

        return opcode_t_states

    # LD r,r
    # 40-7F, except 76 which is HALT
    if 0x40 <= opcode <= 0x7F and opcode != 0x76:
        opcode_t_states = (
            7 if (opcode & 0x07) == 6 or ((opcode >> 3) & 0x07) == 6 else 4
        )
        # TODO: Implement

        self.log_opcode(
            opcode=opcode,
            asm="LD r,r",
            prefix="",
            opcode_t_states=opcode_t_states,
            message="Not implemented",
            implemented=False,
        )

        return opcode_t_states

    match opcode:
        # LD (nn),HL
        case 0x22:
            # -----
            # Opcode logic:

            address = self.store_register_pair(self.get_hl())

            opcode_t_states = 16

            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD (nn),HL",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=(
                    f"Stored HL ({self.get_hl():04X}) into memory at {address:04X}"
                ),
            )

            return opcode_t_states

        # LD HL,(nn)
        case 0x2A:
            # -----
            # Opcode logic:

            value, address = self.load_register_pair(self.set_hl)

            opcode_t_states = 16

            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD HL,(nn)",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=(f"Loaded {value:04X} from memory at {address:04X} into HL"),
            )

            return opcode_t_states

        # LD (HL),n
        # Store immediate byte n at the address in HL
        case 0x36:
            opcode_t_states = 10
            # TODO: Implement

            self.log_opcode(
                opcode=opcode,
                asm="LD (HL),n",
                prefix="",
                opcode_t_states=opcode_t_states,
                message="Not implemented",
                implemented=False,
            )

            return opcode_t_states

        # LD A,(nn)
        # Load A from the address nn
        case 0x3A:
            opcode_t_states = 13
            # TODO: Implement

            self.log_opcode(
                opcode=opcode,
                asm="LD A,(nn)",
                prefix="",
                opcode_t_states=opcode_t_states,
                message="Not implemented",
                implemented=False,
            )

            return opcode_t_states

        # LD (nn),A
        case 0x32:
            opcode_t_states = 13

            # -----
            # Opcode logic:
            low = self.memory.read8(self.pc)
            self.inc_pc(increment=1)
            high = self.memory.read8(self.pc)
            self.inc_pc(increment=1)
            address = (high << 8) | low
            self.memory.write8(address, self.a)
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD (nn),A",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Stored A ({self.a:02X}) at {address:04X}",
                implemented=True,
            )

            return opcode_t_states

        # LD SP, HL
        # Contents of register pair HL are loaded into Stack Pointer SP
        case 0xF9:
            opcode_t_states = 6

            # -----
            # Opcode logic:
            hl = (self.h << 8) | self.l
            self.sp = hl
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD SP, HL",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Loaded HL ({hl:04X}) into SP",
                implemented=True,
            )

            return opcode_t_states

        case _:
            pass

    return None
