from logger import logger
import time

from z80.opcodes import dispatcher

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

        opcode_cycles = dispatcher.execute(self, opcode)

        # Ensure that opcode_cycles is always valid and avoids divide by zero
        if opcode_cycles in (None, 0):
            opcode_cycles = 1

        time.sleep((1 / self.clock_hz) * opcode_cycles)

    def opcode_not_implemented(self, opcode=0, asm="Unknown"):
        if self.exception_on_non_implemented == True:

            # Most of the time the opcode is handed over raw, but prefixed opcodes use strings for error messages
            if isinstance(opcode, int):
                opcode_string = f"{opcode:02X}"
            else:
                opcode_string = str(opcode)

            with open('debug/crash_opcode.txt', 'w') as f: f.write(f"PC: {str(self.pc)}\n Opcode: {opcode_string}")
            raise Exception(f"Opcode not implemented: {opcode_string} ({asm})")
        
        else:
            opcode_cycles = 1 # No opcode is executed but we pretend one cycle has passed 
            return(opcode_cycles) 

    def log_opcode(self, opcode, asm, prefix, opcode_cycles, message, implemented=True):
        logger.debug(
            f"{self.pc:04X}: Prefix: {prefix}: {opcode:02X}: {asm} ({opcode_cycles} cycles) - {message}"
        )

        if implemented == False:
            self.opcode_not_implemented(opcode, asm)

    