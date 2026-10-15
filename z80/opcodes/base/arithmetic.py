from logger import logger

# NOTE: The opcode table below is agent-generated. The code in this file is not.
# Stub = placeholder that raises via log_opcode(implemented=False).
#
# | Opcode                     | Mnemonic               | Status      | Notes                               |
# |----------------------------|------------------------|-------------|-------------------------------------|
# | 03, 13, 23                 | INC rr (BC, DE, HL)    | Implemented |                                     |
# | 33                         | INC SP                 | Implemented | Bug: operates on AF, not SP         |
# | 04, 0C, 14, 1C, 24, 2C, 3C | INC r                  | Implemented |                                     |
# | 34                         | INC (HL)               | Stub        |                                     |
# | 05, 0D, 15, 1D, 25, 2D, 3D | DEC r                  | Implemented |                                     |
# | 35                         | DEC (HL)               | Implemented |                                     |
# | 0B, 1B, 2B                 | DEC rr (BC, DE, HL)    | Implemented |                                     |
# | 3B                         | DEC SP                 | Implemented | Bug: operates on AF, not SP         |
# | 09, 19, 29                 | ADD HL,rr (BC, DE, HL) | Implemented |                                     |
# | 39                         | ADD HL,SP              | Implemented | Bug: operates on AF, not SP         |
# | 80-87                      | ADD A,r                | Implemented |                                     |
# | 88-8F                      | ADC A,r                | Implemented |                                     |
# | 90-97                      | SUB r                  | Implemented |                                     |
# | 98-9F                      | SBC A,r                | Implemented | Second SBC A,r block is unreachable |
# | C6                         | ADD A,n                | Stub        |                                     |
# | CE                         | ADC A,n                | Stub        |                                     |
# | D6                         | SUB n                  | Stub        |                                     |
# | DE                         | SBC A,n                | Stub        |                                     |


def execute(self, opcode):
    # GROUPED OPCODES
    # Some opcodes are very similar, and have things like
    # source addresses embedded in the opcode itself

    # Decoding this lets us save a lot of repetition
    # see get_register() in Z80 for more

    # INC r
    if opcode in (0x04, 0x0C, 0x14, 0x1C, 0x24, 0x2C, 0x3C):

        register = (opcode >> 3) & 0x07

        value_before = self.get_register(register)

        result = (value_before + 1) & 0xFF

        self.set_register(register, result)

        # -----
        # Opcode logic:
        self.flag_s = bool(result & 0x80)
        self.flag_z = result == 0
        self.flag_h = ((value_before & 0x0F) + 1) > 0x0F
        self.flag_pv = value_before == 0x7F
        self.flag_n = False
        # Carry unaffected
        # -----

        opcode_t_states = 4

        self.log_opcode(
            opcode=opcode,
            asm="INC r",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Incremented register {register} from {value_before:02X} to {result:02X}",
            implemented=True,
        )

        return opcode_t_states

    # DEC r
    if opcode in (0x05, 0x0D, 0x15, 0x1D, 0x25, 0x2D, 0x3D):

        register = (opcode >> 3) & 0x07

        value_before = self.get_register(register)

        result = (value_before - 1) & 0xFF

        self.set_register(register, result)

        # -----
        self.flag_s = bool(result & 0x80)
        self.flag_z = result == 0
        self.flag_h = (value_before & 0x0F) == 0x00
        self.flag_pv = value_before == 0x80
        self.flag_n = True
        # Carry unaffected
        # -----

        opcode_t_states = 4

        self.log_opcode(
            opcode=opcode,
            asm="DEC r",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Decremented register {register} from {value_before:02X} to {result:02X}",
            implemented=True,
        )

        return opcode_t_states

    # INC rr
    if opcode in (0x03, 0x13, 0x23, 0x33):

        pair = (opcode >> 4) & 0x03

        value_before = self.get_register_pair(pair)

        result = (value_before + 1) & 0xFFFF

        self.set_register_pair(pair, result)

        opcode_t_states = 6

        self.log_opcode(
            opcode=opcode,
            asm="INC rr",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Incremented register pair from {value_before:04X} to {result:04X}",
            implemented=True,
        )

        return opcode_t_states

    # 0B,1B,2B,3B    DEC rr
    if opcode in (0x0B, 0x1B, 0x2B, 0x3B):

        pair = (opcode >> 4) & 0x03

        value_before = self.get_register_pair(pair)

        result = (value_before - 1) & 0xFFFF

        self.set_register_pair(pair, result)

        opcode_t_states = 6

        self.log_opcode(
            opcode=opcode,
            asm="DEC rr",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Decremented register pair from {value_before:04X} to {result:04X}",
            implemented=True,
        )

        return opcode_t_states

    # 09,19,29,39    ADD HL,rr
    if opcode in (0x09, 0x19, 0x29, 0x39):

        pair = (opcode >> 4) & 0x03

        hl_before = self.get_hl()

        value = self.get_register_pair(pair)

        result = hl_before + value

        self.set_hl(result & 0xFFFF)

        # -----
        self.flag_h = ((hl_before & 0x0FFF) + (value & 0x0FFF)) > 0x0FFF
        self.flag_c = result > 0xFFFF
        self.flag_n = False
        # S/Z/PV unaffected
        # -----

        opcode_t_states = 11

        self.log_opcode(
            opcode=opcode,
            asm="ADD HL,rr",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Added {value:04X} to HL {hl_before:04X}, result {self.get_hl():04X}",
            implemented=True,
        )

        return opcode_t_states

    # 35 DEC (HL)
    if opcode == 0x35:

        address = self.get_hl()

        value_before = self.memory.read8(address)

        result = (value_before - 1) & 0xFF

        self.memory.write8(address, result)

        self.flag_s = bool(result & 0x80)
        self.flag_z = result == 0
        self.flag_h = (value_before & 0x0F) == 0
        self.flag_pv = value_before == 0x80
        self.flag_n = True

        opcode_t_states = 11

        self.log_opcode(
            opcode=opcode,
            asm="DEC (HL)",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Decremented memory at {address:04X} from {value_before:02X} to {result:02X}",
            implemented=True,
        )

        return opcode_t_states

    # 80-87   ADD A,r
    # Contents of register r are added to A and stored in A
    if 0x80 <= opcode <= 0x87:
        self_a_before = self.a

        # -----
        # Opcode logic:
        source = opcode & 0x07
        value = self.get_register(source)
        result = self.a + value
        self.a = result & 0xFF
        self.flag_z = (result & 0xFF) == 0
        self.flag_c = result > 0xFF
        self.flag_n = False
        self.flag_s = bool(self.a & 0x80)
        self.flag_pv = (~(self_a_before ^ value) & (self_a_before ^ result) & 0x80) != 0
        self.flag_h = ((self_a_before & 0x0F) + (value & 0x0F)) > 0x0F
        # -----

        opcode_t_states = 7 if source == 6 else 4

        self.log_opcode(
            opcode=opcode,
            asm="ADD A,r",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Added {value:02X} to {self_a_before:02X} in A, result {self.a:02X}",
            implemented=True,
        )
        return opcode_t_states

    # 88-8F   ADC A,r
    # Contents of register r and carry are added to A and stored in A

    if 0x88 <= opcode <= 0x8F:
        self_a_before = self.a

        # -----
        # Opcode logic:
        carry = 1 if self.flag_c else 0
        source = opcode & 0x07
        value = self.get_register(source)

        result = self_a_before + value + carry

        self.a = result & 0xFF

        self.flag_s = bool(self.a & 0x80)
        self.flag_z = self.a == 0

        self.flag_h = ((self_a_before & 0x0F) + (value & 0x0F) + carry) > 0x0F

        self.flag_pv = (~(self_a_before ^ value) & (self_a_before ^ result) & 0x80) != 0

        self.flag_n = False
        self.flag_c = result > 0xFF
        # -----

        opcode_t_states = 7 if source == 6 else 4

        self.log_opcode(
            opcode=opcode,
            asm="ADC A,r",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Added {value:02X} and carry bit ({carry}) to {self_a_before:02X} in A, result {self.a:02X}",
            implemented=True,
        )

        return opcode_t_states

    # 98-9F    SBC A,r
    # TODO: Define

    if 0x98 <= opcode <= 0x9F:
        # -----
        # Opcode logic:
        self_a_before = self.a
        source = opcode & 0x07
        value = self.get_register(source)

        carry = 1 if self.flag_c else 0

        result = self_a_before - value - carry

        self.a = result & 0xFF

        self.flag_s = bool(self.a & 0x80)
        self.flag_z = self.a == 0

        self.flag_h = (self_a_before & 0x0F) < ((value & 0x0F) + carry)

        self.flag_pv = ((self_a_before ^ value) & (self_a_before ^ result) & 0x80) != 0

        self.flag_n = True
        self.flag_c = result < 0
        # -----

        opcode_t_states = 7 if source == 6 else 4

        self.log_opcode(
            opcode=opcode,
            asm="SBC A,r",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Subtracted {value:02X} and carry bit ({carry}) from {self_a_before:02X} in A, result {self.a:02X}",
            implemented=True,
        )

        return opcode_t_states

    # 90-97    SUB r
    # Subtract r from A and store in A
    if 0x90 <= opcode <= 0x97:
        self_a_before = self.a

        # -----
        # Opcode logic:
        source = opcode & 0x07
        value = self.get_register(source)

        result = self_a_before - value

        self.a = result & 0xFF

        self.flag_s = bool(self.a & 0x80)
        self.flag_z = self.a == 0

        self.flag_h = (self_a_before & 0x0F) < (value & 0x0F)

        self.flag_pv = ((self_a_before ^ value) & (self_a_before ^ result) & 0x80) != 0

        self.flag_c = result < 0
        self.flag_n = True
        # -----

        opcode_t_states = 7 if source == 6 else 4

        self.log_opcode(
            opcode=opcode,
            asm="SUB r",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Subtracted {value:02X} from {self_a_before:02X} in A, result {self.a:02X}",
            implemented=True,
        )

        return opcode_t_states

    # 98-9F    SBC A,r
    # TODO: Define
    if 0x98 <= opcode <= 0x9F:
        # -----
        # Opcode logic:
        self_a_before = self.a
        source = opcode & 0x07
        value = self.get_register(source)
        carry = 1 if self.flag_c else 0
        result = self.a - value - carry
        self.a = result & 0xFF
        self.flag_z = (result & 0xFF) == 0
        self.flag_c = result > 0xFF
        self.flag_n = True
        self.flag_s = bool(self.a & 0x80)
        self.flag_pv = (~(self_a_before ^ value) & (self_a_before ^ result) & 0x80) != 0
        # -----

        opcode_t_states = 7 if source == 6 else 4

        self.log_opcode(
            opcode=opcode,
            asm="SBC A,r",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Subtracted {value:02X} and carry bit ({carry}) from {self_a_before:02X} in A, result {self.a:02x}",
            implemented=True,
        )
        return opcode_t_states

    # Individual opcodes
    match opcode:
        # INC (HL)
        case 0x34:
            opcode_t_states = 11
            # TODO: Implement

            self.log_opcode(
                opcode=opcode,
                asm="INC (HL)",
                prefix="",
                opcode_t_states=opcode_t_states,
                message="Not implemented",
                implemented=False,
            )

            return opcode_t_states

        # ADD A,n / ADC A,n / SUB n / SBC A,n
        case 0xC6 | 0xCE | 0xD6 | 0xDE:
            opcode_t_states = 7
            # TODO: Implement

            asm = {
                0xC6: "ADD A,n",
                0xCE: "ADC A,n",
                0xD6: "SUB n",
                0xDE: "SBC A,n",
            }[opcode]

            self.log_opcode(
                opcode=opcode,
                asm=asm,
                prefix="",
                opcode_t_states=opcode_t_states,
                message="Not implemented",
                implemented=False,
            )

            return opcode_t_states

        case _:
            pass

    logger.info(f"Arithmetic handler fell through for opcode {opcode:02X}")

    return None
