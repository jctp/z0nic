# Base opcodes
from z80.opcodes.base import arithmetic
from z80.opcodes.base import compare
from z80.opcodes.base import interrupts
from z80.opcodes.base import io
from z80.opcodes.base import jumps
from z80.opcodes.base import load
from z80.opcodes.base import logic
from z80.opcodes.base import stack
from z80.opcodes.base import subroutines

# Prefixed opcodes
from z80.opcodes import bit_operations
from z80.opcodes import index_ix  # Includes index_ix_bits passoff
from z80.opcodes import extended
from z80.opcodes import index_iy  # Includes includes index_iy_bits passoff

# CPU control
from z80.opcodes import control

def execute(self, opcode):

    # Between the lines is currently LLM-generated
    # in order to speed up getting the opcode ranges in place.
    # This is not a long-term solution.
    # ------------------------------------------------------------

    # ----------------------------------------
    # ARITHMETIC
    # ----------------------------------------

    # INC r / DEC r
    if opcode in (
        0x04, 0x05,
        0x0C, 0x0D,
        0x14, 0x15,
        0x1C, 0x1D,
        0x24, 0x25,
        0x2C, 0x2D,
        0x34, 0x35,
        0x3C, 0x3D,
    ):
        return arithmetic.execute(self, opcode)

    # ADD / ADC / SUB / SBC
    if 0x80 <= opcode <= 0x9F:
        return arithmetic.execute(self, opcode)

    # Immediate arithmetic
    if opcode in (
        0xC6,  # ADD A,n
        0xCE,  # ADC A,n
        0xD6,  # SUB n
        0xDE,  # SBC A,n
    ):
        return arithmetic.execute(self, opcode)

    # 16-bit arithmetic
    if opcode in (
        0x09,  # ADD HL,BC
        0x19,  # ADD HL,DE
        0x29,  # ADD HL,HL
        0x39,  # ADD HL,SP

        0x03,  # INC BC
        0x13,  # INC DE
        0x23,  # INC HL
        0x33,  # INC SP

        0x0B,  # DEC BC
        0x1B,  # DEC DE
        0x2B,  # DEC HL
        0x3B,  # DEC SP
    ):
        return arithmetic.execute(self, opcode)

    # ----------------------------------------
    # BIT OPERATIONS
    # ----------------------------------------

    if opcode in (

        # Rotate accumulator
        0x07,  # RLCA
        0x0F,  # RRCA
        0x17,  # RLA
        0x1F,  # RRA

        # Flag/bit manipulation
        0x27,  # DAA
        0x2F,  # CPL
        0x37,  # SCF
        0x3F,  # CCF

        # Register exchange
        0x08,  # EX AF,AF'
        0xD9,  # EXX
        0xE3,  # EX (SP),HL
        0xEB   # EX DE,HL

    ):
        return bit_operations.execute(self, opcode)
    
    # ----------------------------------------
    # COMPARE
    # ----------------------------------------

    if 0xB8 <= opcode <= 0xBF:
        return compare.execute(self, opcode)

    if opcode == 0xFE:
        return compare.execute(self, opcode)

    # ----------------------------------------
    # INTERRUPTS
    # ----------------------------------------

    if opcode in (
        0xF3,  # DI
        0xFB,  # EI
    ):
        return interrupts.execute(self, opcode)

    # ----------------------------------------
    # IO
    # ----------------------------------------

    if opcode in (
        0xD3,  # OUT (n),A
        0xDB,  # IN A,(n)
    ):
        return io.execute(self, opcode)

    # ----------------------------------------
    # JUMPS
    # ----------------------------------------

    if opcode in (
        0x10,      # DJNZ e
        0x18,      # JR
        0x20,      # JR NZ
        0x28,      # JR Z
        0x30,      # JR NC
        0x38,      # JR C

        0xC2,      # JP NZ
        0xC3,      # JP
        0xCA,      # JP Z

        0xD2,      # JP NC
        0xDA,      # JP C

        0xE2,      # JP PO
        0xEA,      # JP PE

        0xF2,      # JP P
        0xFA,      # JP M

        0xE9,      # JP (HL)
    ):
        return jumps.execute(self, opcode)

    # ----------------------------------------
    # LOAD
    # ----------------------------------------

    if (

        # LD r,n
        opcode in (
            0x06, 0x0E,
            0x16, 0x1E,
            0x26, 0x2E,
            0x3E,
        )

        # LD rr,nn
        or opcode in (
            0x01,
            0x11,
            0x21,
            0x31,
        )

        # LD (BC),A / LD (DE),A
        or opcode in (
            0x02,
            0x12,
        )

        # LD A,(BC) / LD A,(DE)
        or opcode in (
            0x0A,
            0x1A,
        )

        # Direct memory loads
        or opcode in (
            0x22,  # LD (nn),HL
            0x2A,  # LD HL,(nn)

            0x32,  # LD (nn),A
            0x3A,  # LD A,(nn)
        )

        # Register-to-register loads
        or (0x40 <= opcode <= 0x7F and opcode != 0x76)

        # Special loads
        or opcode in (
            0xF9,  # LD SP,HL
        )
    ):
        return load.execute(self, opcode)

    # ----------------------------------------
    # LOGIC
    # ----------------------------------------

    if 0xA0 <= opcode <= 0xB7:
        return logic.execute(self, opcode)

    if opcode in (
        0xE6,  # AND n
        0xEE,  # XOR n
        0xF6,  # OR n
    ):
        return logic.execute(self, opcode)

    # ----------------------------------------
    # STACK
    # ----------------------------------------

    if opcode in (
        0xC1, 0xC5,   # BC
        0xD1, 0xD5,   # DE
        0xE1, 0xE5,   # HL
        0xF1, 0xF5,   # AF
    ):
        return stack.execute(self, opcode)

    # ----------------------------------------
    # SUBROUTINES
    # ----------------------------------------

    if opcode in (
        0xC0, 0xC4,
        0xC8, 0xC9, 0xCC,
        0xCD,

        0xD0, 0xD4,
        0xD8, 0xDC,

        0xE0, 0xE4,
        0xE8, 0xEC,

        0xF0, 0xF4,
        0xF8, 0xFC,

        0xC7, 0xCF,
        0xD7, 0xDF,
        0xE7, 0xEF,
        0xF7, 0xFF,   # RST
    ):
        return subroutines.execute(self, opcode)

    # ----------------------------------------
    # CPU CONTROL
    # ----------------------------------------

    if opcode in (
        0x00,  # NOP
        0x76,  # HALT
    ):
        return control.execute(self, opcode)

    # ------------------------------------------------------------
    # Human code resumes here

    match opcode:

        # Hand off to prefixed opcodes

        case 0xCB:
            bit_operations.execute(self)

        case 0xED:
            extended.execute(self)

        case 0xDD:
            index_ix.execute(self)  # Includes DDCB

        case 0xFD:
            index_iy.execute(self)  # Includes FDCB

        case _:
            self.opcode_not_implemented(opcode, "Unknown mnemonic")
