from logger import logger


# SMS memory map
# 0000-3FFF  ROM Bank 0
# 4000-7FFF  ROM Bank 1
# 8000-BFFF  ROM Bank 2 / RAM
# C000-DFFF  Work RAM
# E000-FFFF  Mirror of WRAM


class Memory:
    def __init__(self, cartridge):

        # Cartridge itself
        self.cartridge = cartridge

        # Memory banks
        self.bank0 = 0
        self.bank1 = 1
        self.bank2 = 2

        # RAM
        self.ram = bytearray(0x2000)

    def read8(self, address):
        # Bank 0
        if address < 0x4000:
            offset = self.bank0 * 0x4000 + address
            return self.cartridge.rom[offset]

        # Bank 1
        elif address < 0x8000:
            offset = self.bank1 * 0x4000 + (address - 0x4000)
            return self.cartridge.rom[offset]

        # Bank 2
        elif address < 0xC000:
            offset = self.bank2 * 0x4000 + (address - 0x8000)
            return self.cartridge.rom[offset]

        # RAM reads
        elif address <= 0xFFFF:
            return self.ram[address & 0x1FFF]

    def write8(self, address, value):
        # Keep only the lowest 8 bits; ensures valid 8-bit value
        value &= 0xFF

        if 0xC000 <= address <= 0xFFFF:
            self.ram[address & 0x1FFF] = value
