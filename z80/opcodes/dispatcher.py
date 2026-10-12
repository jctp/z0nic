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


def execute(self, opcode):

    # Between the lines is currently LLM-generated
    # in order to speed up getting the opcode ranges in place.
    # This is not a long-term solution.
    # ------------------------------------------------------------

    # Arithmetic
    if opcode in (
        0x04,
        0x05,
        0x0C,
        0x0D,
        0x14,
        0x15,
        0x1C,
        0x1D,
        0x24,
        0x25,
        0x2C,
        0x2D,
        0x3C,
        0x3D,
    ):
        return arithmetic.execute(self, opcode)

    if 0x80 <= opcode <= 0x9F:
        return arithmetic.execute(self, opcode)

    if opcode in (0xC6, 0xCE, 0xD6, 0xDE):
        return arithmetic.execute(self, opcode)

    # Compare
    if 0xB8 <= opcode <= 0xBF:
        return compare.execute(self, opcode)

    if opcode == 0xFE:
        return compare.execute(self, opcode)

    # Interrupts
    if opcode in (0xF3, 0xFB):
        return interrupts.execute(self, opcode)

    # IO
    if opcode in (0xDB, 0xD3):
        return io.execute(self, opcode)

    # Jumps
    if opcode in (
        0x18,
        0x20,
        0x28,
        0x30,
        0x38,
        0xC2,
        0xC3,
        0xCA,
        0xD2,
        0xDA,
        0xE2,
        0xEA,
        0xF2,
        0xFA,
    ):
        return jumps.execute(self, opcode)

    # Load
    if (
        opcode in (
            0x01, 0x06, 0x0E, 0x11, 0x16,
            0x21, 0x22, 0x26,
            0x2A,
            0x31, 0x32, 0x3A, 0x3E,
            0xF9
        )
        or (0x40 <= opcode <= 0x7F)
    ):
        return load.execute(self, opcode)

    if 0x40 <= opcode <= 0x7F:
        return load.execute(self, opcode)

    # Logic
    if 0xA0 <= opcode <= 0xB7:
        return logic.execute(self, opcode)

    if opcode in (0xE6, 0xEE, 0xF6):
        return logic.execute(self, opcode)

    # Stack
    if opcode in (0xC1, 0xC5, 0xD1, 0xD5, 0xE1, 0xE5, 0xF1, 0xF5):
        return stack.execute(self, opcode)

    # Subroutines
    if opcode in (
        0xC0,
        0xC4,
        0xC8,
        0xC9,
        0xCC,
        0xCD,
        0xD0,
        0xD4,
        0xD8,
        0xDC,
        0xE0,
        0xE4,
        0xE8,
        0xEC,
        0xF0,
        0xF4,
        0xF8,
        0xFC,
    ):
        return subroutines.execute(self, opcode)

    # ------------------------------------------------------------
    # Human code resumes here

    match opcode:
        # NOP
        # No operation
        case 0x00:
            opcode_t_states = 1
            self.log_opcode(
                opcode=opcode,
                asm="NOP",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"NOP",
                implemented=True,
            )
            return opcode_t_states

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
