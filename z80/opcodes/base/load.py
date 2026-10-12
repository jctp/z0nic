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
        self.pc += 1
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
        self.pc += 1
        high = self.memory.read8(self.pc)
        self.pc += 1
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
        
    match opcode:
        
        case 0x32:

            opcode_t_states = 13

            # -----
            # Opcode logic:
            low = self.memory.read8(self.pc)
            self.pc += 1
            high = self.memory.read8(self.pc)
            self.pc += 1
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

        case _:
            pass

    return None
