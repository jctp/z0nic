from logger import logger

# NOTE: The opcode table below is agent-generated. The code in this file is not.
# Stub = placeholder that raises via log_opcode(implemented=False).
#
# | Opcode                         | Mnemonic   | Status      | Notes |
# |--------------------------------|------------|-------------|-------|
# | C0                             | RET NZ     | Stub        |       |
# | C8                             | RET Z      | Stub        |       |
# | C9                             | RET        | Implemented |       |
# | D0                             | RET NC     | Stub        |       |
# | D8                             | RET C      | Stub        |       |
# | E0                             | RET PO     | Stub        |       |
# | E8                             | RET PE     | Stub        |       |
# | F0                             | RET P      | Stub        |       |
# | F8                             | RET M      | Stub        |       |
# | C4                             | CALL NZ,nn | Stub        |       |
# | CC                             | CALL Z,nn  | Stub        |       |
# | CD                             | CALL nn    | Implemented |       |
# | D4                             | CALL NC,nn | Stub        |       |
# | DC                             | CALL C,nn  | Stub        |       |
# | E4                             | CALL PO,nn | Stub        |       |
# | EC                             | CALL PE,nn | Stub        |       |
# | F4                             | CALL P,nn  | Stub        |       |
# | FC                             | CALL M,nn  | Stub        |       |
# | C7, CF, D7, DF, E7, EF, F7, FF | RST p      | Implemented |       |


def execute(self, opcode):
    match opcode:
        # CALL nn
        # Push current PC onto stack and jump to nn
        case 0xCD:
            opcode_t_states = 17

            source_address = self.pc

            # -----
            # Opcode logic:
            low = self.memory.read8(self.pc)
            self.inc_pc(increment=1)
            high = self.memory.read8(self.pc)
            self.inc_pc(increment=1)
            destination = (high << 8) | low
            return_address = self.pc
            self.push16(return_address)
            self.pc = destination
            # -----
        
            logger.info(
                f"CALL nn: {source_address:04X} -> {destination:04X}"
            )

            self.log_opcode(
                opcode=opcode,
                asm="CALL nn",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Called {destination:04X}, return address {return_address:04X}",
                implemented=True,
            )

            return opcode_t_states

        # RET
        # Return to caller
        case 0xC9:
            opcode_t_states = 10

            source_address = self.pc

            # -----
            # Opcode logic:
            return_address = self.pop16()
            self.pc = return_address
            # -----

            logger.info(
                f"RET: {source_address:04X} -> {return_address:04X}"
            )

            self.log_opcode(
                opcode=opcode,
                asm="RET",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Returned to {return_address:04X}",
                implemented=True,
            )

            return opcode_t_states

        # RST
        case 0xC7 | 0xCF | 0xD7 | 0xDF | 0xE7 | 0xEF | 0xF7 | 0xFF:
            opcode_t_states = 11

            self.push16(self.pc)

            self.pc = opcode & 0x38

            return opcode_t_states

        # RET cc
        # Return from subroutine if condition cc is true
        case 0xC0 | 0xC8 | 0xD0 | 0xD8 | 0xE0 | 0xE8 | 0xF0 | 0xF8:
            opcode_t_states = 5
            # TODO: Implement

            condition = ("NZ", "Z", "NC", "C", "PO", "PE", "P", "M")[
                (opcode >> 3) & 0x07
            ]

            self.log_opcode(
                opcode=opcode,
                asm=f"RET {condition}",
                prefix="",
                opcode_t_states=opcode_t_states,
                message="Not implemented",
                implemented=False,
            )

            return opcode_t_states

        # CALL cc,nn
        # Call subroutine at nn if condition cc is true
        case 0xC4 | 0xCC | 0xD4 | 0xDC | 0xE4 | 0xEC | 0xF4 | 0xFC:
            opcode_t_states = 10
            # TODO: Implement

            condition = ("NZ", "Z", "NC", "C", "PO", "PE", "P", "M")[
                (opcode >> 3) & 0x07
            ]

            self.log_opcode(
                opcode=opcode,
                asm=f"CALL {condition},nn",
                prefix="",
                opcode_t_states=opcode_t_states,
                message="Not implemented",
                implemented=False,
            )

            return opcode_t_states

    return None
