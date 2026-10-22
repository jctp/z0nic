# region Imports

from logger import logger

from z80.opcodes import dispatcher
from z80.structure.registers import (
    Register8Bit,
    Register8BitPair,
    Register16Bit,
    RegisterFlags
)

# endregion
# region Z80 CPU

class Z80:
    def __init__(
        self,
        memory,
        io,
        clock_hz=1000
    ):
        self.setup()
        self.memory = memory
        self.io = io
        self.clock_hz = clock_hz
        self.reset()

    # endregion
    # region Components


    # endregion
    # region Z80 Setup

    def reset(self):
        self.PC.set(0x0000)
        self.SP.set(0xDFF0)

    def setup(self):

        # Main Registers
        
        self.A = Register8Bit()
        self.F = RegisterFlags()
        self.AF = Register8BitPair(self.A, self.F)

        self.B = Register8Bit()
        self.C = Register8Bit()
        self.BC = Register8BitPair(self.B, self.C)

        self.D = Register8Bit()
        self.E = Register8Bit()
        self.DE = Register8BitPair(self.D, self.E)

        self.H = Register8Bit()
        self.L = Register8Bit()
        self.HL = Register8BitPair(self.H, self.L)

        # Alternate Registers

        self.A_alt = Register8Bit()
        self.F_alt = RegisterFlags()
        self.AF_alt = Register8BitPair(self.A_alt, self.F_alt)

        self.B_alt = Register8Bit()
        self.C_alt = Register8Bit()
        self.BC_alt = Register8BitPair(self.B_alt, self.C_alt)

        self.D_alt = Register8Bit()
        self.E_alt = Register8Bit()
        self.DE_alt = Register8BitPair(self.D_alt, self.E_alt)

        self.H_alt = Register8Bit()
        self.L_alt = Register8Bit()
        self.HL_alt = Register8BitPair(self.H_alt, self.L_alt)

        # Special Purpose Registers

        self.I = Register8Bit()
        self.R = Register8Bit()
        self.IX = Register16Bit()
        self.IY = Register16Bit()
        self.PC = Register16Bit()
        self.SP = Register16Bit()

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

        # Interrupt flip-flops
        self.IFF1 = False
        self.IFF2 = False

        # Interrupt mode
        self.IM = 0

        # EI delay; it runs the cycle AFTER
        self.EI_delay = 0

        logger.info("Z80 setup complete!")

    # endregion
    # region Read uOps
    def read_byte(self):
        pass

    def read_word(self):
        pass

    # endregion
    # region Jump uOps

    def jump_absolute(self, target):
        self.PC.set(target & 0xFFFF)

    def jump_relative(self, offset):
        offset = self.signed_byte(offset)
        self.PC.set((self.PC.get() + offset) & 0xFFFF)

    # endregion
    # region Push uOps

    def push_byte(self):
        pass

    def push_word(self):
        pass

    # endregion
    # region Pop uOps

    def pop_byte(self):
        pass

    def pop_word(self):
        pass

    # endregion
    # region Subroutine uOps

    def call(self):
        pass

    def ret(self):
        pass

    # endregion
    # region ALU Arithmetic uOps

    def alu_add(self):
        pass

    def alu_adc(self):
        pass

    def alu_sub(self):
        pass

    def alu_sbc(self):
        pass

    def alu_cp(self):
        pass

    # endregion
    # region ALU Logic uOps

    def alu_and(self):
        pass

    def alu_or(self):
        pass

    def alu_xor(self):
        pass

    # endregion
    # region Bitwise uOps

    def bit(self):
        pass

    def set_(self):
        pass

    def res(self):
        pass

    # endregion
    # region Shift/Rotate uOps

    def rlc(self):
        pass

    def rrc(self):
        pass

    def rl(self):
        pass

    def rr(self):
        pass

    def sla(self):
        pass

    def sra(self):
        pass

    def srl(self):
        pass

    # endregion
    # region Byte Handling

    def signed_byte(self, value):

        if value & 0x80:
            return value - 0x100

        return value

    # endregion
    # region Interrupt Handling
    
    def interrupt(self):
        logger.debug("Interrupt fired! Did nothing yet...")
    
    # endregion
    # region CPU Stepping

    def step(self):
        opcode = self.memory.read8(self.PC.get())
        print(f"PC={self.PC.get():04X} opcode=0x{opcode:02X}")
        self.PC.inc()

        try:
            t_states = dispatcher.execute(self, opcode)

            # Handle delayed EI
            if self.EI_delay > 0:
                self.EI_delay -= 1

                if self.EI_delay == 0:
                    self.IFF1 = True
                    self.IFF2 = True

            # Handle frame interrupts
            if self.IFF1 and self.io.vdp.frame_interrupt_pending:
                self.interrupt()

            return t_states
            
        except NotImplementedError:
            print(f"STOP at PC={self.PC.get():04X} on unimplemented opcode 0x{opcode:02X}")
            raise


        
        # endregion
