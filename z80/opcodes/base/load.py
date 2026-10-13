# 01    LD BC,nn
# 06    LD B,n
# 0E    LD C,n
# 11    LD DE,nn
# 16    LD D,n
# 21    LD HL,nn
# 26    LD H,n
# 31    LD SP,nn
# 3E    LD A,n

# 40-7F LD r,r


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

    # LD r,nn
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

    # LD rr,A
    if opcode in (0x02, 0x12):
        opcode_t_states = 7

        # -----
        # Opcode logic:
        pair = (opcode >> 4) & 0x01
        if pair == 0:
            address = (self.b << 8) | self.c
        else:
            address = (self.d << 8) | self.e
        self.memory.write8(
            address,
            self.a
        )
        # -----

        self.log_opcode(
            opcode=opcode,
            asm="LD rr,A",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Loaded {pair:04X} into {address:04X}",
            implemented=True,
        )

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


    match opcode:

        # LD (nn),HL
        case 0x22:

            # -----
            # Opcode logic:

            address = self.store_register_pair(
                self.get_hl()
            )

            opcode_t_states = 16

            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD (nn),HL",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=(
                    f"Stored HL ({self.get_hl():04X}) "
                    f"into memory at {address:04X}"
                )
            )

        # LD HL,(nn)
        case 0x2A:

            # -----
            # Opcode logic:

            value, address = self.load_register_pair(
                self.set_hl
            )

            opcode_t_states = 16

            # -----

            self.log_opcode(
                opcode=opcode,
                asm="LD HL,(nn)",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=(
                    f"Loaded {value:04X} from "
                    f"memory at {address:04X} into HL"
                )
            )
                
        case 0x32:

            opcode_t_states = 13

            # -----
            # Opcode logic:
            low = self.memory.read8(self.pc)
            self.inc_pc(increment=1)
            high = self.memory.read8(self.pc)
            self.inc_pc(increment=1)
            address = (high << 8) | low
            self.memory.write8(
                address,
                self.a
            )
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
