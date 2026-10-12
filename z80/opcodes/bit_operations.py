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
        
    # ----------------------------------------
    # BIT
    # ----------------------------------------
    match opcode:
        case _:
            pass

    # ----------------------------------------
    # REGISTER EXCHANGE
    # ----------------------------------------
    match opcode:

        case 0x08:

            opcode_t_states = 4

            self.a, self.a_alt = self.a_alt, self.a
            self.f, self.f_alt = self.f_alt, self.f

            self.log_opcode(
                opcode=opcode,
                asm="EX AF,AF'",
                prefix="",
                opcode_t_states=opcode_t_states,
                message="Exchanged AF with AF'",
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
