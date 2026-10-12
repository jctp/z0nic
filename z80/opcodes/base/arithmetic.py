# 80-87   ADD A,r - Implemented
# 88-8F   ADC A,r - Implemented

# 90-97   SUB r = Implemented
# 98-9F   SBC A,r - Implemented

# C6       ADD A,n
# CE       ADC A,n
# D6       SUB n
# DE       SBC A,n


def execute(self, opcode):

    # GROUPED OPCODES
    # Some opcodes are very similar, and have things like
    # source addresses embedded in the opcode itself

    # Decoding this lets us save a lot of repetition
    # see get_register() in Z80 for more

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
        self.flag_z = ((result & 0xFF) == 0)
        self.flag_c = (result > 0xFF)
        self.flag_n = False
        # -----

        opcode_t_states = 7 if source == 6 else 4

        self.log_opcode(
            opcode=opcode,
            asm="ADD A,r",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Added {value:02X} to {self_a_before:02X} in A, result {result:02X}",
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
        result = self.a + value + carry
        self.a = result & 0xFF
        self.flag_z = ((result & 0xFF) == 0)
        self.flag_c = (result > 0xFF)
        self.flag_n = False
        # -----

        opcode_t_states = 7 if source == 6 else 4

        self.log_opcode(
            opcode=opcode,
            asm="ADC A,r",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Added {value:02X} and carry bit ({carry}) to {self_a_before:02X} in A, result {result:02X}",
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
        result = self.a - value
        self.a = result & 0xFF
        self.flag_z = ((result & 0xFF) == 0)
        self.flag_c = (self.a < value)
        self.flag_n = True
        # -----

        opcode_t_states = 7 if source == 6 else 4

        self.log_opcode(
            opcode=opcode,
            asm="SUB r",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Subtracted {value:02X} from {self_a_before:02X} in A, result {result:02x}",
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
        self.flag_z = ((result & 0xFF) == 0)
        self.flag_c = (self_a_before < (value + carry)) # Borrow required?
        self.flag_n = True 
        # -----

        opcode_t_states = 7 if source == 6 else 4

        self.log_opcode(
            opcode=opcode,
            asm="SBC A,r",
            prefix="",
            opcode_t_states=opcode_t_states,
            message=f"Subtracted {value:02X} and carry bit ({carry}) from {self_a_before:02X} in A, result {result:02x}",
            implemented=True,
        )
        return opcode_t_states

    # Individual opcodes
    match opcode:
        case _:
            pass

    return None
