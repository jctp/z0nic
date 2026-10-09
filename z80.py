from logger import logger


class Z80:
    def __init__(self, memory):
        self.setup()
        self.memory = memory

    def setup(self):
        # Main registers
        self.a = 0  # Pair
        self.f = 0
        self.b = 0  # Pair
        self.c = 0
        self.d = 0  # Pair
        self.e = 0
        self.h = 0  # Pair
        self.l = 0
        # Special registers
        self.pc = 0
        self.sp = 0
        self.ix = 0
        self.iy = 0

    def step(self):
        opcode = self.memory.read8(self.pc)
        self.pc += 1
        self.execute(opcode)

    def log_opcode(self, opcode, asm, implemented=True):
        logger.debug("-" * 40)
        logger.debug(f"{self.pc:04X}: {opcode:02X}: {asm}")

        if implemented == False:
            logger.debug(f"{opcode:02X} ({asm}) NOT IMPLEMENTED, TREATED AS NOP!")

    def execute(self, opcode):
        match opcode:
            # ----------------------------------------
            # NO OPERATION
            # ----------------------------------------

            # NOP
            # No operation
            case 0x00:
                self.log_opcode(opcode, "NOP", implemented=True)
                pass

            # ----------------------------------------
            # LOAD
            # ----------------------------------------

            # LD A, n
            # Load n into A
            case 0x3E:
                # Reads byte following opcode
                self.a = self.memory.read8(self.pc)
                self.log_opcode(opcode, "LD A, n", implemented=True)
                logger.debug(f"Loaded {self.a:04X} into A")
                self.pc += 1

            # LD B, n
            # Load n into B
            # TODO: Implement
            case 0x06:
                self.log_opcode(opcode, "LD B, n", implemented=False)
                pass

            # LD HL, nn
            # TODO: Define
            # TODO: Implement
            case 0x21:
                self.log_opcode(opcode, "LD HL, nn", implemented=False)
                pass

            # ----------------------------------------
            # LOGIC
            # ----------------------------------------

            # XOR A
            # TODO: Define
            # TODO: Implement
            case 0xAF:
                self.log_opcode(opcode, "XOR A", implemented=False)
                pass

            # ----------------------------------------
            # MATHS
            # ----------------------------------------

            # ADD A,B
            # TODO: Define
            # TODO: Implement
            case 0x80:
                self.log_opcode(opcode, "ADD A,B", implemented=False)
                pass

            # SUB B
            # TODO: Define
            # TODO: Implement
            case 0x90:
                self.log_opcode(opcode, "SUB B", implemented=False)
                pass

            # ----------------------------------------
            # PUSH/POP
            # ----------------------------------------

            # PUSH HL
            # TODO: Define
            # TODO: Implement
            case 0xE5:
                self.log_opcode(opcode, "PUSH HL", implemented=False)
                pass

            # POP HL
            # TODO: Define
            # TODO: Implement
            case 0xE1:
                self.log_opcode(opcode, "POP HL", implemented=False)
                pass

            # ----------------------------------------
            # SUBROUTINES
            # ----------------------------------------

            # CALL nn nn
            # TODO: Define
            # TODO: Implement
            case 0xCD:
                self.log_opcode(opcode, "CALL nn nn", implemented=False)
                pass

            # RET
            # TODO: Define
            # TODO: Implement
            case 0xC9:
                self.log_opcode(opcode, "RET", implemented=False)
                pass

            # ----------------------------------------
            # INCREMENT/DECREMENT
            # ----------------------------------------

            # INC B
            # TODO: Define
            # TODO: Implement
            case 0x04:
                self.log_opcode(opcode, "INC B", implemented=False)
                pass

            # DEC B
            # TODO: Define
            # TODO: Implement
            case 0x05:
                self.log_opcode(opcode, "DEC B", implemented=False)
                pass

            # ----------------------------------------
            # COMPARE
            # ----------------------------------------

            # CP nn
            # TODO: Define
            # TODO: Implement
            case 0xFE:
                self.log_opcode(opcode, "CP nn", implemented=False)
                pass

            # ----------------------------------------
            # JUMP
            # ----------------------------------------

            # JP nn
            # Jump directly to nn
            case 0xC3:
                # Low byte of 2-byte opcode
                low = self.memory.read8(self.pc)
                self.pc += 1
                # High byte
                high = self.memory.read8(self.pc)
                self.pc = (
                    high << 8
                ) | low  # Takes two bytes, combines into one 16b addr
                self.log_opcode(opcode, "JP nn", implemented=True)
                logger.debug(f"Jumped directly to {self.pc}")

            # JR e
            # Jump by offset e
            case 0x18:
                offset = self.memory.read8(self.pc)
                self.pc += 1
                # Convert an unsigned byte into a signed byte
                if offset & 0x80:
                    offset -= 0x100

                pc_before_jump = self.pc
                self.pc += offset
                pc_after_jump = self.pc

                self.log_opcode(opcode, "JR e", implemented=True)
                logger.debug(
                    f"Jumped from {pc_before_jump:04X} to {pc_after_jump:04x} with offset {offset:04x}"
                )

            # ----------------------------------------
            # UNKNOWN OPCODE
            # ----------------------------------------

            case _:
                logger.debug("-" * 40)
                logger.debug(f"Not implemented: {opcode:02X}")
                # raise Exception(
                #    f"Not implemented opcode {opcode:02X}"
                # )
