# region Imports

from logger import logger

from z80.opcodes import dispatcher
from z80.structure.flag_setters import FlagSetters
from z80.structure.registers import (
    Register8Bit,
    Register8BitPair,
    Register16Bit,
    RegisterFlags,
)
from z80.structure.uops import UOps

# endregion
# region Z80 CPU


class Z80(FlagSetters, UOps):
    def __init__(self, memory, io, clock_hz=1000, log_opcodes=False):
        self.setup()
        self.memory = memory
        self.io = io
        self.clock_hz = clock_hz
        self.reset()
        self.log_opcodes = log_opcodes

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

        # Reads and writes for registers referred to by 3-bit numbers
        # For example, SRA r

        self.read_3bit = [
            lambda: self.B.get(),
            lambda: self.C.get(),
            lambda: self.D.get(),
            lambda: self.E.get(),
            lambda: self.H.get(),
            lambda: self.L.get(),
            lambda: self.memory.read8(self.HL.get()),
            lambda: self.A.get(),
        ]

        self.write_3bit = [
            lambda v: self.B.set(v),
            lambda v: self.C.set(v),
            lambda v: self.D.set(v),
            lambda v: self.E.set(v),
            lambda v: self.H.set(v),
            lambda v: self.L.set(v),
            lambda v: self.memory.write8(self.HL.get(), v),
            lambda v: self.A.set(v),
        ]

        # Interrupt flip-flops

        self.IFF1 = False
        self.IFF2 = False

        # Interrupt mode

        self.IM = 0

        # EI delay; it runs the cycle AFTER

        self.EI_delay = 0

        logger.info("Z80 setup complete!")

    # endregion
    # Fields

    # R

    # Get the last three bits from an opcode , r, to feed into the lookup table
    def get_r(self, opcode):
        return opcode & 0b111

    def read_from_r(self, r):
        return self.read_3bit[r]()

    def write_to_r(self, r, value):
        self.write_3bit[r](value)

    def read_from_opcode_r(self, opcode):
        r = self.get_r(opcode)
        return self.read_from_r(r)

    def write_to_opcode_r(self, opcode, value):
        r = self.get_r(opcode)
        self.write_to_r(r, value)

    # Y

    def get_y(self, opcode):
        return (opcode >> 3) & 0b111

    def read_from_y(self, y):
        return self.read_3bit[y]()

    def write_to_y(self, y, value):
        self.write_3bit[y](value)

    def read_from_opcode_y(self, opcode):
        y = self.get_y(opcode)
        return self.read_from_y(y)

    def write_to_opcode_y(self, opcode, value):
        y = self.get_y(opcode)
        self.write_to_y(y, value)

    # endregion
    # region Interrupt Handling

    def interrupt(self):
        logger.debug("Interrupt fired! Did nothing yet...")

    # endregion
    # region CPU Stepping

    def step(self):
        opcode = self.memory.read8(self.PC.get())

        if self.log_opcodes:
            print(f"PC={self.PC.get():04X} opcode=0x{opcode:02X}")

        self.PC.inc()

        try:
            t_states = dispatcher.execute(self, opcode)

            self.io.vdp.tick(t_states)

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

        except NotImplementedError as exc:
            description = str(exc)
            if "opcode " in description:
                description = description.split("opcode ", 1)[1]
                description = description.replace(" is not implemented", "")
            else:
                description = f"0x{opcode:02X}"

            RED = "\033[31m"
            ORANGE = "\033[38;5;208m"
            YELLOW = "\033[33m"
            GREEN = "\033[32m"
            CYAN = "\033[36m"
            BLUE = "\033[34m"
            MAGENTA = "\033[35m"
            WHITE = "\033[37m"
            RESET = "\033[0m"

            BOLD = "\033[1m"
            BLINK = "\033[5m"

            print(f"{RED}={RESET}" * 80)
            print(
                f"{BOLD}{BLINK}{GREEN}O-{CYAN}^v^v^{GREEN}-{RED} WELCOME TO BUG LAND {GREEN}-{CYAN}^v^v^{GREEN}-O{RESET}"
            )
            print(
                f"Hello, my name is: {RED}{BOLD}STOP{RESET} at PC={self.PC.get():04X} on unimplemented Z80 opcode: {GREEN}{description}{RESET}"
            )
            print(f"{RED}={RESET}" * 80)
            raise SystemExit(1)

        # endregion
