class Register8Bit:
    def __init__(self):
        self.contents = 0

    def __str__(self):
        return f"{self.contents:08b}"

    def __repr__(self):
        return f"Register8Bit (0x{self.contents:02X})"

    def set(self, value: int=0):
        self.contents = (value & 0xFF)

    def get(self):
        return self.contents

    def inc(self, by=1):
        self.contents = (self.contents + by) & 0xFF

    def dec(self, by=1):
        self.contents = (self.contents - by) & 0xFF

    def shift_left(self, by=1):
        self.contents = (self.contents << by) & 0xFF

    def shift_right(self, by=1):
        self.contents = (self.contents >> by)

    def rotate_left(self, by=1):
        by %= 8
        self.contents = (
            (self.contents << by) | (self.contents >> (8 - by))
        ) & 0xFF

    def rotate_right(self, by=1):
        by %= 8
        self.contents = (
            (self.contents >> by) | (self.contents << (8 - by))
        ) & 0xFF

    def get_bit(self, bit):
        if not 0 <= bit <= 7:
            raise ValueError("Bit must be between 0 and 7.")
        return (self.contents >> bit) & 1

    def set_bit(self, bit):
        if not 0 <= bit <= 7:
            raise ValueError("Bit must be between 0 and 7.")
        self.contents |= (1 << bit)

    def clear_bit(self, bit):
        if not 0 <= bit <= 7:
            raise ValueError("Bit must be between 0 and 7")
        self.contents &= ~(1 << bit)

    def toggle_bit(self, bit):
        if not 0 <= bit <= 7:
            raise ValueError("Bit must be between 0 and 7")
        self.contents ^= (1 << bit)

class Register8BitPair:
    def __init__(self, hi_reg, lo_reg):
        self.hi_reg = hi_reg
        self.lo_reg = lo_reg

    def get(self):
        return (self.hi_reg.get() << 8) | self.lo_reg.get()

    def get_hi_byte(self):
        return self.hi_reg.get()

    def get_lo_byte(self):
        return self.lo_reg.get()

    def set(self, value):
        value &= 0xFFFF
        self.hi_reg.set((value >> 8) & 0xFF)
        self.lo_reg.set(value & 0xFF)

    def inc(self, by=1):
        self.set(self.get() + by)

    def dec(self, by=1):
        self.set(self.get() - by)

class Register16Bit:
    def __init__(self):
        self.contents = 0

    def __str__(self):
        return f"{self.contents:016b}"

    def __repr__(self):
        return f"Register16Bit (0x{self.contents:04X})"

    def set(self, value: int=0):
        self.contents = (value & 0xFFFF)

    def get(self):
        return self.contents

    def inc(self, by=1):
        self.contents = (self.contents + by) & 0xFFFF

    def dec(self, by=1):
        self.contents = (self.contents - by) & 0xFFFF

class RegisterFlags(Register8Bit):

    FLAG_BITS = {
        "S": 7,
        "Z": 6,
        "X": 5,
        "H": 4,
        "Y": 3,
        "PV": 2,
        "N": 1,
        "C": 0
    }

    BIT_FLAGS = {
        7: "S",
        6: "Z",
        5: "X",
        4: "H",
        3: "Y",
        2: "PV",
        1: "N",
        0: "C"
    }

    def __init__(self):
        super().__init__() # Inherit from Register8Bit

    def set_flag(self, flag, value):
        
        if flag not in self.FLAG_BITS:
            raise ValueError(f"Unknown flag: {flag}")

        if value:
            self.set_bit(self.FLAG_BITS[flag])
        else:
            self.clear_bit(self.FLAG_BITS[flag])

    def get_flag(self, flag):
        return self.get_bit(self.FLAG_BITS[flag])

    # Carry
    @property
    def carry(self):
        return self.get_flag("C")

    @carry.setter
    def carry(self, value):
        self.set_flag("C", value)

    # Add/Subtract
    @property
    def add_sub(self):
        return self.get_flag("N")

    @add_sub.setter
    def add_sub(self, value):
        self.set_flag("N", value)

    # Parity/Overflow
    @property
    def parity_overflow(self):
        return self.get_flag("PV")

    @parity_overflow.setter
    def parity_overflow(self, value):
        self.set_flag("PV", value)

    # Undocumented Y
    @property
    def undoc_y(self):
        return self.get_flag("Y")

    @undoc_y.setter
    def undoc_y(self, value):
        self.set_flag("Y", value)

    # Half Carry
    @property
    def half_carry(self):
        return self.get_flag("H")

    @half_carry.setter
    def half_carry(self, value):
        self.set_flag("H", value)

    # Undocumented X
    @property
    def undoc_x(self):
        return self.get_flag("X")

    @undoc_x.setter
    def undoc_x(self, value):
        self.set_flag("X", value)

    # Zero
    @property
    def zero(self):
        return self.get_flag("Z")

    @zero.setter
    def zero(self, value):
        self.set_flag("Z", value)

    # Sign
    @property
    def sign(self):
        return self.get_flag("S")

    @sign.setter
    def sign(self, value):
        self.set_flag("S", value)