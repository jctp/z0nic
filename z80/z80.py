from logger import logger
import datetime
import time

from z80.opcodes import dispatcher

# endregion
# region Z80 CPU


class Z80:
    def __init__(
        self,
        memory,
        io,
        clock_hz
    ):
        self.setup()
        self.memory = memory
        self.io = io
        self.clock_hz = clock_hz

    # endregion
    # region Components

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

    # endregion
    # region Z80 Setup

    def setup(self):

        # Main Registers
        
        self.A = self.Register8Bit()
        self.F = self.RegisterFlags()
        self.AF = self.Register8BitPair(self.A, self.F)

        self.B = self.Register8Bit()
        self.C = self.Register8Bit()
        self.BC = self.Register8BitPair(self.B, self.C)

        self.D = self.Register8Bit()
        self.E = self.Register8Bit()
        self.DE = self.Register8BitPair(self.D, self.E)

        self.H = self.Register8Bit()
        self.L = self.Register8Bit()
        self.HL = self.Register8BitPair(self.H, self.L)

        # Alternate Registers

        self.A_alt = self.Register8Bit()
        self.F_alt = self.RegisterFlags()
        self.AF_alt = self.Register8BitPair(self.A_alt, self.F_alt)

        self.B_alt = self.Register8Bit()
        self.C_alt = self.Register8Bit()
        self.BC_alt = self.Register8BitPair(self.B_alt, self.C_alt)

        self.D_alt = self.Register8Bit()
        self.E_alt = self.Register8Bit()
        self.DE_alt = self.Register8BitPair(self.D_alt, self.E_alt)

        self.H_alt = self.Register8Bit()
        self.L_alt = self.Register8Bit()
        self.HL_alt = self.Register8BitPair(self.H_alt, self.L_alt)

        # Special Purpose Registers

        self.I = self.Register8Bit()
        self.R = self.Register8Bit()
        self.IX = self.Register16Bit()
        self.IY = self.Register16Bit()
        self.PC = self.Register16Bit()
        self.SP = self.Register16Bit()

        # Lookups

        self.registers = {
            "A": self.A,
            "B": self.B,
            "C": self.C,
            "D": self.D,
            "E": self.E,
            "H": self.H,
            "L": self.L,
            "F": self.F,
        }

        self.register_pairs = {
            "AF": self.AF,
            "BC": self.BC,
            "DE": self.DE,
            "HL": self.HL,
        }

        self.registers_alt = {
            "A_alt": self.A_alt,
            "B_alt": self.B_alt,
            "C_alt": self.C_alt,
            "D_alt": self.D_alt,
            "E_alt": self.E_alt,
            "H_alt": self.H_alt,
            "L_alt": self.L_alt,
            "F_alt": self.F_alt,
        }

        self.register_pairs_alt = {
            "AF_alt": self.AF_alt,
            "BC_alt": self.BC_alt,
            "DE_alt": self.DE_alt,
            "HL_alt": self.HL_alt,
        }


    # endregion
    # region Step

    def step(self):
        opcode = self.memory.read8(self.PC)
        self.PC.inc()
        return dispatcher.execute(self, opcode)

    # endregion
