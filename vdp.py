from logger import logger


class VDP:
    def __init__(self):
        self.vram = bytearray(0x4000)
        self.cram = bytearray(0x20)
        self.registers = [0] * 16

        self.address = 0

        self.status = 0x80

        self.status_reads = 0
        self.be_reads = 0
        self.be_writes = 0
        self.bf_writes = 0

        self.control_latch = False
        self.control_low = 0

        self.code = 0

    def dump_vram(self, filename="vram.txt"):
        with open(filename, "w") as f:
            for address in range(0, 0x4000, 16):
                values = " ".join(
                    f"{byte:02X}" for byte in self.vram[address : address + 16]
                )

                f.write(f"{address:04X}: {values}\n")

    def read(self, port):
        if port == 0xBF:
            value = self.status

            logger.debug(
                f"VDP STATUS READ -> {value:02X}"
            )

            self.status = 0
            self.control_latch = False

            return value

        if port == 0xBE:
            self.be_reads += 1

            # Not implemented yet
            return 0xFF

        return 0xFF

    def write(self, port, value):

        if port == 0xBF:

            logger.info(
                f"BF WRITE value={value:02X} latch={self.control_latch}"
            )
            
            self.bf_writes += 1

            if not self.control_latch:
                self.control_low = value
                self.control_latch = True

            else:
                self.control_latch = False

                logger.info(
                    f"CONTROL low={self.control_low:02X} high={value:02X}"
                )

                # Register write
                if (value & 0xC0) == 0x80:
                    register = value & 0x0F

                    self.registers[register] = self.control_low

                    logger.info(
                        f"VDP REG {register} <- {self.control_low:02X}"
                    )

                    return

                self.code = (value >> 6) & 0x03
                self.address = (
                    ((value & 0x3F) << 8)
                    | self.control_low
                )

                logger.debug(
                    f"VDP CMD={self.code} ADDR={self.address:04X}"
                )

            return

        if port == 0xBE:
            self.be_writes += 1

            logger.debug(
                f"BE WRITE code={self.code} addr={self.address:04X} value={value:02X}"
            )

            if self.code == 1: # VRAM write
                logger.info(
                    f"VRAM[{self.address:04X}] <- {value:02X}"
                )
                self.vram[self.address] = value
            elif self.code == 3: # CRAM write
                #logger.info(
                #    f"CRAM[ {self.address & 0x1F:02X} ] <- {value:02X}"
                #)
                self.cram[self.address & 0x1F] = value

            self.address = (self.address + 1) & 0x3FFF

            if self.be_writes % 1000 == 0:
                self.dump_vram()

            return
