from z80.opcodes import cb
from z80.opcodes import dd
from z80.opcodes import ed
from z80.opcodes import fd

def execute(self, opcode):
    match opcode:

        # ----------------------------------------
        # NO OPERATION
        # ----------------------------------------

        # NOP
        # No operation
        case 0x00:
            opcode_cycles = 1
            self.log_opcode(
                opcode = opcode,
                asm = "NOP",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"NOP",
                implemented=True,
            )
            return opcode_cycles

        # ----------------------------------------
        # PREFIXED OPCODES
        # ----------------------------------------

        case 0xCB:
            cb.execute(self)

        case 0xED:
            ed.execute(self)

        case 0xDD:
            dd.execute(self) # Includes DDCB

        case 0xFD:
            fd.execute(self) # Includes FDCB

        # ----------------------------------------
        # LOAD
        # ----------------------------------------

        # LD A, n
        # Load n into A
        case 0x3E:
            opcode_cycles = 2

            # Reads byte following opcode
            self.a = self.memory.read8(self.pc)
            self.pc += 1

            self.log_opcode(
                opcode = opcode,
                asm = "LD A, n",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"Loaded {self.a:04X} into A",
                implemented=True,
            )
            return opcode_cycles

        # LD B, n
        # Load n into B
        case 0x06:
            opcode_cycles = 2

            # Reads byte following opcode
            self.a = self.memory.read8(self.pc)
            self.pc += 1

            self.log_opcode(
                opcode = opcode,
                asm = "LD B, n",
                opcode_cycles = opcode_cycles,
                message = f"Loaded {self.a:04X} into B",
                implemented=True,
            )
            return opcode_cycles

        # LD HL, nn
        # TODO: Define
        # TODO: Implement
        case 0x21:
            opcode_cycles = 5

            # Opcode function goes here

            self.log_opcode(
                opcode = opcode,
                asm = "LD HL, n",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"",
                implemented=False,
            )
            return opcode_cycles

        # ----------------------------------------
        # LOGIC
        # ----------------------------------------

        # XOR A
        # TODO: Define
        # TODO: Implement
        case 0xAF:
            opcode_cycles = 1 # TODO: Check correct

            # Opcode function goes here

            self.log_opcode(
                opcode = opcode,
                asm = "XOR A",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"",
                implemented=False,
            )
            return opcode_cycles

        # ----------------------------------------
        # MATHS
        # ----------------------------------------

        # ADD A,B
        # TODO: Define
        # TODO: Implement
        case 0x80:
            opcode_cycles = 1 # TODO: Check correct

            # Opcode function goes here

            self.log_opcode(
                opcode = opcode,
                asm = "ADD A,B",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"",
                implemented=False,
            )
            return opcode_cycles

        # SUB B
        # TODO: Define
        # TODO: Implement
        case 0x90:
            opcode_cycles = 1 # TODO: Check correct

            # Opcode function goes here

            self.log_opcode(
                opcode = opcode,
                asm = "SUB B",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"",
                implemented=False,
            )
            return opcode_cycles

        # ----------------------------------------
        # PUSH/POP
        # ----------------------------------------

        # PUSH HL
        # TODO: Define
        # TODO: Implement
        case 0xE5:
            opcode_cycles = 1 # TODO: Check correct

            # Opcode function goes here

            self.log_opcode(
                opcode = opcode,
                asm = "PUSH HL",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"",
                implemented=False,
            )
            return opcode_cycles

        # POP HL
        # TODO: Define
        # TODO: Implement
        case 0xE1:
            opcode_cycles = 1 # TODO: Check correct

            # Opcode function goes here

            self.log_opcode(
                opcode = opcode,
                asm = "POP HL",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"",
                implemented=False,
            )
            return opcode_cycles

        # ----------------------------------------
        # SUBROUTINES
        # ----------------------------------------

        # CALL nn nn
        # TODO: Define
        # TODO: Implement
        case 0xCD:
            opcode_cycles = 1 # TODO: Check correct

            # Opcode function goes here

            self.log_opcode(
                opcode = opcode,
                asm = "CALL nn nn",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"",
                implemented=False,
            )
            return opcode_cycles

        # RET
        # TODO: Define
        # TODO: Implement
        case 0xC9:
            opcode_cycles = 1 # TODO: Check correct

            # Opcode function goes here

            self.log_opcode(
                opcode = opcode,
                asm = "RET",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"",
                implemented=False,
            )
            return opcode_cycles

        # ----------------------------------------
        # INCREMENT/DECREMENT
        # ----------------------------------------

        # INC B
        # TODO: Define
        # TODO: Implement
        case 0x04:
            opcode_cycles = 1 # TODO: Check correct

            # Opcode function goes here

            self.log_opcode(
                opcode = opcode,
                asm = "INC B",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"",
                implemented=False,
            )
            return opcode_cycles

        # DEC B
        # TODO: Define
        # TODO: Implement
        case 0x05:
            opcode_cycles = 1 # TODO: Check correct

            # Opcode function goes here

            self.log_opcode(
                opcode = opcode,
                asm = "DEC B",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"",
                implemented=False,
            )
            return opcode_cycles

        # ----------------------------------------
        # COMPARE
        # ----------------------------------------

        # CP nn
        # TODO: Define
        # TODO: Implement
        case 0xFE:
            opcode_cycles = 1 # TODO: Check correct

            # Opcode function goes here

            self.log_opcode(
                opcode = opcode,
                asm = "CP nn",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"",
                implemented=False,
            )
            return opcode_cycles

        # ----------------------------------------
        # JUMP
        # ----------------------------------------

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

        # ----------------------------------------
        # INTERRUPT HANDLING
        # ----------------------------------------

        # DI
        # Disable interrupts
        case 0xF3:
            opcode_cycles = 4

            self.iff1 = False
            self.iff2 = False

            self.log_opcode(
                opcode = opcode,
                asm = "DI",
                prefix = "None",
                opcode_cycles = opcode_cycles,
                message = f"Disabled interrupts",
                implemented=True,
            )
            return opcode_cycles

        # ----------------------------------------
        # UNKNOWN OPCODE
        # ----------------------------------------

        case _:
            self.opcode_not_implemented(opcode, "Unknown mnemonic")
