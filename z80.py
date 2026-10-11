from logger import logger
import time


class Z80:
    def __init__(self, memory, clock_hz, exception_on_non_implemented):
        self.setup()
        self.memory = memory
        self.clock_hz = clock_hz
        self.exception_on_non_implemented = exception_on_non_implemented

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

        # Interrupt enable flip-flops
        self.iff1 = False
        self.iff2 = False

    def step(self):
        opcode = self.memory.read8(self.pc)
        self.pc += 1

        opcode_cycles = self.execute(opcode)

        # Ensure that opcode_cycles is always valid and avoids divide by zero
        if opcode_cycles in (None, 0):
            opcode_cycles = 1

        time.sleep((1 / self.clock_hz) * opcode_cycles)

    def opcode_not_implemented(self, opcode=0, asm="Unknown"):
        if self.exception_on_non_implemented == True:
                with open('debug/crash_opcode.txt', 'w') as f: f.write(f"{opcode:02X}")
                raise Exception(f"Opcode not implemented: {opcode:02X} ({asm})")
        else:
            opcode_cycles = 1 # No opcode is executed but we pretend one cycle has passed 
            return(opcode_cycles) 

    def log_opcode(self, opcode, asm, prefix, opcode_cycles, message, implemented=True):
        logger.debug(
            f"{self.pc:04X}: Prefix: {prefix}: {opcode:02X}: {asm} ({opcode_cycles} cycles) - {message}"
        )

        if implemented == False:
            self.opcode_not_implemented(opcode, asm)

    # PREFIXED OPCODES

    def execute_prefix_0xCB(self):
        opcode = self.memory.read8(self.pc)
        self.pc += 1

        match opcode:
            # ROTATES AND SHIFTS

            # BIT

            # RES

            # SET

            # Not implemented 
            case _:
                self.opcode_not_implemented(f"CB {opcode:02X}", "Unknown mnemonic")

    def execute_prefix_0xED(self):
        opcode = self.memory.read8(self.pc)
        self.pc += 1

        match opcode:

            # Not implemented 
            case _:
                self.opcode_not_implemented(f"ED {opcode:02X}", "Unknown mnemonic")

    # DD xx
    # Prefix for IX instructions  
    def execute_prefix_0xDD(self):
        opcode = self.memory.read8(self.pc)
        self.pc += 1

        match opcode:

            case 0xCB:
                self.execute_prefix_0xDDCB()

            # Not implemented 
            case _:
                self.opcode_not_implemented(f"DD {opcode:02X}", "Unknown mnemonic")

    # DD CB d xx
    # IX + displacement bit operations 
    def execute_prefix_0xDDCB(self):
        displacement = self.memory.read8(self.pc)
        self.pc += 1

        opcode = self.memory.read8(self.pc)
        self.pc += 1
        
        match opcode:

            case _:
                self.opcode_not_implemented(f"DD CB {displacement:02X} {opcode:02X}", "Unknown mnemonic")

    # FD xx
    # Prefix for IY instructions  
    def execute_prefix_0xFD(self):
        opcode = self.memory.read8(self.pc)
        self.pc += 1

        match opcode:

            # Further prefix of CB
            case 0xCB:
                self.execute_prefix_0xFDCB()

            # Not implemented 
            case _:
                self.opcode_not_implemented(f"FD {opcode:02X}", "Unknown mnemonic")

    # FD CB d xx
    # IY + displacement bit operations
    def execute_prefix_0xFDCB(self):

        displacement = self.memory.read8(self.pc)
        self.pc += 1

        opcode = self.memory.read8(self.pc)
        self.pc += 1

        match opcode:
                
            case _:
                self.opcode_not_implemented(f"FD CB {displacement:02X} {opcode:02X}", "Unknown mnemonic")

    # REGULAR OPCODES

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
                self.execute_prefix_0xCB()

            case 0xED:
                self.execute_prefix_0xED()

            case 0xDD:
                self.execute_prefix_0xDD() # Includes DDCB

            case 0xFD:
                self.execute_prefix_0xFD() # Includes FDCB

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
