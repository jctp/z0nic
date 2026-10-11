from logger import logger
import time


class Z80:
    def __init__(self, memory, clock_hz):
        self.setup()
        self.memory = memory
        self.clock_hz = clock_hz

    def setup(self):
        # Main registers
        self.a = 0  # Accumulator
        self.f = 0  # Flag
        self.b = 0  # Accumulator
        self.c = 0  # Flag
        self.d = 0  # Accumulator
        self.e = 0  # Flag
        self.h = 0  # Accumulator
        self.l = 0  # Flag
        # Special registers
        self.pc = 0
        self.sp = 0
        self.ix = 0
        self.iy = 0

    def step(self):
        opcode = self.memory.read8(self.pc)
        self.pc += 1
        opcode_cycles = self.execute(opcode)
        time.sleep((1 / self.clock_hz) * opcode_cycles)

    def opcode_not_implemented(self, opcode=0, asm="Unknown"):
        raise Exception(f"Opcode not implemented: {opcode:02X} ({asm})")

    def log_opcode(self, opcode, asm, opcode_cycles, message, implemented=True):
        logger.debug(
            f"{self.pc:04X}: {opcode:02X}: {asm} ({opcode_cycles} cycles) - {message}"
        )

        if implemented == False:
            self.opcode_not_implemented(opcode, asm)

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
                    opcode_cycles = opcode_cycles,
                    message = f"NOP",
                    implemented=True,
                )
                return opcode_cycles

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
                    opcode_cycles = opcode_cycles,
                    message = f"Jumped by offset {offset} from {source_address} to {dest_address}",
                    implemented=True,
                )
                return opcode_cycles

            # ----------------------------------------
            # UNKNOWN OPCODE
            # ----------------------------------------

            case _:
                self.opcode_not_implemented(opcode, "Unknown mnemonic")
