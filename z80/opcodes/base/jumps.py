from logger import logger

# NOTE: The opcode table below is agent-generated. The code in this file is not.
# Stub = placeholder that raises via log_opcode(implemented=False).
#
# | Opcode | Mnemonic | Status      | Notes |
# |--------|----------|-------------|-------|
# | 10     | DJNZ e   | Implemented |       |
# | 18     | JR e     | Implemented |       |
# | 20     | JR NZ,e  | Implemented |       |
# | 28     | JR Z,e   | Implemented |       |
# | 30     | JR NC,e  | Stub        |       |
# | 38     | JR C,e   | Implemented |       |
# | C2     | JP NZ,nn | Stub        |       |
# | C3     | JP nn    | Implemented |       |
# | CA     | JP Z,nn  | Stub        |       |
# | D2     | JP NC,nn | Stub        |       |
# | DA     | JP C,nn  | Stub        |       |
# | E2     | JP PO,nn | Stub        |       |
# | E9     | JP (HL)  | Stub        |       |
# | EA     | JP PE,nn | Stub        |       |
# | F2     | JP P,nn  | Stub        |       |
# | FA     | JP M,nn  | Stub        |       |


def execute(self, opcode):
    match opcode:
        # JP nn
        # Jump directly to nn
        case 0xC3:
            opcode_t_states = 10

            source_address = self.pc

            # -----
            # Opcode logic:
            # Low byte of 2-byte opcode
            low = self.memory.read8(self.pc)
            self.inc_pc(increment=1)
            # High byte
            high = self.memory.read8(self.pc)
            self.pc = (high << 8) | low  # Takes two bytes, combines into one 16b addr
            # -----

            dest_address = self.pc

            logger.info(
                f"JP nn: {source_address:04X} -> {dest_address:04X}"
            )

            self.log_opcode(
                opcode=opcode,
                asm="JP nn",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Jumped directly from {source_address:04X} to {dest_address:04X}",
                implemented=True,
            )
            return opcode_t_states

        # JR e
        # Jump by offset e
        case 0x18:
            opcode_t_states = 12  # TODO: Check correct

            source_address = self.pc

            # -----
            # Opcode logic:
            offset = self.memory.read8(self.pc)
            self.inc_pc(increment=1)
            # Convert an unsigned byte into a signed byte
            if offset & 0x80:
                offset -= 0x100
            self.pc = (self.pc + offset) & 0xFFFF
            # -----

            dest_address = self.pc

            logger.info(
                f"JR e: {source_address:04X} -> {dest_address:04X}"
            )

            self.log_opcode(
                opcode=opcode,
                asm="JR e",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Jumped by offset {offset} from {source_address} to {dest_address}",
                implemented=True,
            )
            return opcode_t_states

        # JR C,e
        case 0x38:
            source_address = self.pc

            # -----
            # Opcode logic:
            offset = self.memory.read8(self.pc)
            self.inc_pc(increment=1)
            if offset & 0x80:
                offset -= 0x100
            if self.flag_c:
                self.pc = (self.pc + offset) & 0xFFFF
                opcode_t_states = 12
            else:
                opcode_t_states = 7
            dest_address = self.pc
            # -----

            logger.info(
                f"JR C, e: {source_address:04X} -> {dest_address:04X}"
            )

            self.log_opcode(
                opcode=opcode,
                asm="JR C,e",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=(
                    f"C={int(self.flag_c)} "
                    f"jumped from "
                    f"{source_address:04X} "
                    f"to {dest_address:04X}"
                ),
                implemented=True,
            )

            return opcode_t_states

        # DJNZ e
        # Decrement B and jump relative if B is not zero
        case 0x10:
            opcode_t_states = 8

            # -----
            # Opcode logic:
            source_address = self.pc
            offset = self.memory.read8(self.pc)
            self.inc_pc(increment=1)
            self.b = (self.b - 1) & 0xFF
            if self.b != 0:
                if offset & 0x80:
                    offset -= 0x100
                self.pc = (self.pc + offset) & 0xFFFF
                opcode_t_states = 13
            dest_address = self.pc
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="DJNZ e",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=(
                    f"B={self.b:02X} "
                    f"C={self.c:02X} "
                    f"jumped from {source_address:04X} "
                    f"to {dest_address:04X}"
                ),
                implemented=True,
            )

            return opcode_t_states

        # JR NZ,e
        # Jump by offset e if condition is true
        case 0x20:

            before_pc = self.pc

            offset_e = self.memory.read8(self.pc)
            self.inc_pc(1)

            # Convert offset to signed 8-bit int
            if offset_e >= 0x80:
                offset_e -= 0x100
                
            if self.flag_z == 0: # This is NZ
                self.pc = (self.pc + offset_e) & 0xFFFF
                opcode_t_states = 12
            else:
                opcode_t_states = 7

            after_pc = self.pc

            self.log_opcode(
                opcode=opcode,
                asm=f"JR NZ,e",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Jumped from {before_pc:04X} to {after_pc:04X}",
                implemented=True,
            )

            return opcode_t_states

        # JR Z,e
        # Jump by offset e if condition is true
        case 0x28:

            before_pc = self.pc

            offset_e = self.memory.read8(self.pc)
            self.inc_pc(1)

            # Convert offset to signed 8-bit int
            if offset_e >= 0x80:
                offset_e -= 0x100
                
            if self.flag_z == 1: # This is Z
                self.pc = (self.pc + offset_e) & 0xFFFF
                opcode_t_states = 12
            else:
                opcode_t_states = 7

            after_pc = self.pc

            self.log_opcode(
                opcode=opcode,
                asm=f"JR Z,e",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Jumped from {before_pc:04X} to {after_pc:04X}",
                implemented=True,
            )

            return opcode_t_states
        # JR NC,e
        # Jump by offset e if condition is true
        case 0x30:
            opcode_t_states = 7

            case 

            self.log_opcode(
                opcode=opcode,
                asm=f"JR NC,e",
                prefix="",
                opcode_t_states=opcode_t_states,
                message="Not implemented",
                implemented=False,
            )

            return opcode_t_states


        # JP cc,nn
        # Jump to nn if condition cc is true
        case 0xC2 | 0xCA | 0xD2 | 0xDA | 0xE2 | 0xEA | 0xF2 | 0xFA:
            opcode_t_states = 10
            # TODO: Implement

            condition = ("NZ", "Z", "NC", "C", "PO", "PE", "P", "M")[
                (opcode >> 3) & 0x07
            ]

            self.log_opcode(
                opcode=opcode,
                asm=f"JP {condition},nn",
                prefix="",
                opcode_t_states=opcode_t_states,
                message="Not implemented",
                implemented=False,
            )

            return opcode_t_states

        # JP (HL)
        # Jump to the address in HL
        case 0xE9:
            opcode_t_states = 4
            # TODO: Implement

            self.log_opcode(
                opcode=opcode,
                asm="JP (HL)",
                prefix="",
                opcode_t_states=opcode_t_states,
                message="Not implemented",
                implemented=False,
            )

            return opcode_t_states

    return None
