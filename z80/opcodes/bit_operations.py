from logger import logger

# 07  RLCA
# 0F  RRCA
# 17  RLA
# 1F  RRA

# 27  DAA
# 2F  CPL

# 37  SCF
# 3F  CCF

# 76  HALT

# 00  NOP


def execute(self, opcode):
    # ----------------------------------------
    # ROTATES AND SHIFTS
    # ----------------------------------------
    match opcode:
        # RRA
        # Rotate Right Accumulator through Carry
        case 0x1F:
            opcode_t_states = 4

            # -----
            # Opcode logic:
            old_carry = 1 if self.flag_c else 0
            new_carry = self.a & 0x01
            self.a = ((self.a >> 1) | (old_carry << 7)) & 0xFF
            self.flag_c = bool(new_carry)
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="RRA",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"A rotated right through carry to {self.a:02X}",
                implemented=True,
            )

            return opcode_t_states

        # RLCA / RRCA / RLA
        # Rotate Accumulator
        case 0x07 | 0x0F | 0x17:
            opcode_t_states = 4
            # TODO: Implement

            asm = {0x07: "RLCA", 0x0F: "RRCA", 0x17: "RLA"}[opcode]

            self.log_opcode(
                opcode=opcode,
                asm=asm,
                prefix="",
                opcode_t_states=opcode_t_states,
                message="Not implemented",
                implemented=False,
            )

            return opcode_t_states

        # DAA / CPL / SCF / CCF
        # Accumulator and carry flag adjustments
        case 0x27 | 0x2F | 0x37 | 0x3F:
            opcode_t_states = 4
            # TODO: Implement

            asm = {0x27: "DAA", 0x2F: "CPL", 0x37: "SCF", 0x3F: "CCF"}[opcode]

            self.log_opcode(
                opcode=opcode,
                asm=asm,
                prefix="",
                opcode_t_states=opcode_t_states,
                message="Not implemented",
                implemented=False,
            )

            return opcode_t_states

    # ----------------------------------------
    # BIT
    # ----------------------------------------
    match opcode:
        # CB xx
        # Rotate, shift, BIT, RES and SET table
        case 0xCB:
            sub_opcode = self.memory.read8(self.pc)
            self.inc_pc(increment=1)

            opcode_t_states = 8
            # TODO: Implement the CB table

            self.log_opcode(
                opcode=sub_opcode,
                asm="CB prefix",
                prefix="CB",
                opcode_t_states=opcode_t_states,
                message="Not implemented",
                implemented=False,
            )

            return opcode_t_states

        case _:
            pass

    # ----------------------------------------
    # REGISTER EXCHANGE
    # ----------------------------------------

    if opcode in (
        0x08,  # EX AF,AF'
        0xD9,  # EXX
    ):
        opcode_t_states = 4

        logger.debug(
            f"A={self.a:02X} "
            f"Z={int(self.flag_z)} "
            f"C={int(self.flag_c)} "
            f"S={int(self.flag_s)} "
            f"PV={int(self.flag_pv)} "
            f"N={int(self.flag_n)}"
        )

        # -----
        # Opcode logic:
        if opcode == 0x08:
            self.exchange_af()
            asm = "EX AF,AF'"
            message = "Exchanged AF with AF'"
        else:
            self.exchange_bcdEhl()
            asm = "EXX"
            message = "Exchanged BC, DE and HL with alternate registers"
        # -----

        logger.debug(
            f"A={self.a:02X} "
            f"Z={int(self.flag_z)} "
            f"C={int(self.flag_c)} "
            f"S={int(self.flag_s)} "
            f"PV={int(self.flag_pv)} "
            f"N={int(self.flag_n)}"
        )

        self.log_opcode(
            opcode=opcode,
            asm=asm,
            prefix="",
            opcode_t_states=opcode_t_states,
            message=message,
            implemented=True,
        )

        return opcode_t_states

    match opcode:
        # EX (SP),HL
        # Exchange the value in HL with the 16b value at the top of the stack
        case 0xE3:
            opcode_t_states = 19

            # -----
            # Opcode logic:
            stack_low = self.memory.read8(self.sp)
            stack_high = self.memory.read8((self.sp + 1) & 0xFFFF)
            stack_value = (stack_high << 8) | stack_low
            hl = (self.h << 8) | self.l
            self.memory.write8(self.sp, hl & 0xFF)
            self.memory.write8((self.sp + 1) & 0xFFFF, (hl >> 8) & 0xFF)
            self.h = (stack_value >> 8) & 0xFF
            self.l = stack_value & 0xFF
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="EX (SP),HL",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Exchanged HL ({hl:04X}) with stack value ({stack_value:04X})",
                implemented=True,
            )

            return opcode_t_states

        # EX DE,HL
        # Exchange DE and HL
        case 0xEB:
            opcode_t_states = 4

            # -----
            # Opcode logic:
            de = self.get_de()
            hl = self.get_hl()

            self.set_de(hl)
            self.set_hl(de)
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="EX DE,HL",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=(f"DE now {self.get_de():04X}, HL now {self.get_hl():04X}"),
                implemented=True,
            )

            return opcode_t_states

        case _:
            pass

    # ----------------------------------------
    # SET
    # ----------------------------------------
    match opcode:
        case _:
            pass

    # Not implemented
    return None
