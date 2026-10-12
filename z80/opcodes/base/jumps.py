# 18      JR e
# 20      JR NZ,e
# 28      JR Z,e

# 30      JR NC,e
# 38      JR C,e

# C3      JP nn

# C2      JP NZ,nn
# CA      JP Z,nn

# D2      JP NC,nn
# DA      JP C,nn


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
            self.pc += 1
            # High byte
            high = self.memory.read8(self.pc)
            self.pc = (high << 8) | low  # Takes two bytes, combines into one 16b addr
            # -----

            dest_address = self.pc

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
            self.pc += 1
            # Convert an unsigned byte into a signed byte
            if offset & 0x80:
                offset -= 0x100
            self.pc += offset
            # -----

            dest_address = self.pc

            self.log_opcode(
                opcode=opcode,
                asm="JR e",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Jumped by offset {offset} from {source_address} to {dest_address}",
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
            self.pc += 1
            self.b = (self.b - 1) & 0xFF
            if self.b != 0:
                if offset & 0x80:
                    offset -= 0x100
                self.pc += offset
                opcode_t_states = 13
            dest_address = self.pc
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="DJNZ e",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=(
                    f"Decremented B to {self.b:02X}, "
                    f"jumped from {source_address:04X} "
                    f"to {dest_address:04X}"
                ),
                implemented=True,
            )

            return opcode_t_states

    return None
