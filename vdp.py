from logger import logger


class VDP:
    def __init__(self):
        self.vram = bytearray(0x4000)
        self.address = 0

        self.status = 0x80

        self.status_reads = 0
        self.be_reads = 0
        self.be_writes = 0
        self.bf_writes = 0

        self.control_latch = False
        self.control_low = 0

    def dump_vram(self, filename="vram.txt"):
        with open(filename, "w") as f:
            for address in range(0, 0x4000, 16):
                values = " ".join(
                    f"{byte:02X}" for byte in self.vram[address : address + 16]
                )

                f.write(f"{address:04X}: {values}\n")

    def read(self, port):
        if port == 0xBF:
            logger.debug(f"VDP STATUS READ -> {self.status:02X}")

            value = self.status

            return self.status

        if port == 0xBE:
            self.be_reads += 1

            return 0xFF

        return 0xFF

    def write(self, port, value):
        if port == 0xBF:
            self.bf_writes += 1

            if not self.control_latch:
                # First control byte
                self.control_low = value
                self.control_latch = True

            else:
                # Second control byte
                command = (value << 8) | self.control_low

                self.control_latch = False

                logger.debug(f"VDP COMMAND {command:04X}")

        if port == 0xBE:
            self.be_writes += 1

            self.vram[self.address] = value

            logger.debug(f"VRAM[{self.address:04X}] <- {value:02X}")

            self.address = (self.address + 1) & 0x3FFF

            if self.be_writes % 1000 == 0:
                self.dump_vram()

            return
