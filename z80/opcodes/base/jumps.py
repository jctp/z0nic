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
            opcode_cycles = 1 # TODO: Check correct

            source_address = self.pc

            # Low byte of 2-byte opcode
            low = self.memory.read8(self.pc)
            self.pc += 1
            # High byte
            high = self.memory.read8(self.pc)
            self.pc = (
                high << 8
            ) | low  # Takes two bytes, combines into one 16b addr

            dest_address = self.pc

            self.log_opcode(
                opcode = opcode,
                asm = "JP nn",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"Jumped directly from {source_address} to {dest_address}",
                implemented=True,
            )
            return opcode_cycles

        # JR e
        # Jump by offset e
        case 0x18:
            opcode_cycles = 1 # TODO: Check correct

            source_address = self.pc

            offset = self.memory.read8(self.pc)
            self.pc += 1
            # Convert an unsigned byte into a signed byte
            if offset & 0x80:
                offset -= 0x100
            self.pc += offset

            dest_address = self.pc

            self.log_opcode(
                opcode = opcode,
                asm = "JR e",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"Jumped by offset {offset} from {source_address} to {dest_address}",
                implemented=True,
            )
            return opcode_cycles

    return None