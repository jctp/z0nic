from logger import logger

# SMS memory map
# 0000-03FF  ROM Bank 0 (always the first 1KB of the ROM)
# 0400-3FFF  ROM Slot 0 (paged by FFFD)
# 4000-7FFF  ROM Slot 1 (paged by FFFE)
# 8000-BFFF  ROM Slot 2 (paged by FFFF) / Cartridge RAM (enabled by FFFC)
# C000-DFFF  Work RAM
# E000-FFFF  Mirror of WRAM

# Sega mapper control registers live in the top of the WRAM mirror
# FFFC  RAM control: bit 3 = cart RAM in slot 2, bit 2 = cart RAM bank
# FFFD  Slot 0 ROM bank
# FFFE  Slot 1 ROM bank
# FFFF  Slot 2 ROM bank


class Memory:
    def __init__(self, cartridge):
        # Cartridge itself
        self.cartridge = cartridge

        # Memory banks
        self.bank0 = 0
        self.bank1 = 1
        self.bank2 = 2

        # Cartridge RAM: two 16KB banks, mapped into slot 2 by FFFC
        self.ram_control = 0
        self.cart_ram = bytearray(0x8000)

        # RAM
        self.ram = bytearray(0x2000)

    @staticmethod
    def _normalize_address(address):
        if hasattr(address, "get"):
            return address.get()
        return int(address)

    def read8(self, address_register):
        address = self._normalize_address(address_register)

        # Bank 0, the first 1KB is never paged
        if address < 0x0400:
            return self.cartridge.rom[address % len(self.cartridge.rom)]

        # Slot 0
        elif address < 0x4000:
            offset = self.bank0 * 0x4000 + address
            offset %= len(self.cartridge.rom)
            return self.cartridge.rom[offset]

        # Slot 1
        elif address < 0x8000:
            offset = self.bank1 * 0x4000 + (address - 0x4000)
            offset %= len(self.cartridge.rom)
            value = self.cartridge.rom[offset]

            logger.debug(
                f"BANK1: addr={address:04X} bank={self.bank1:02X} offset={offset:05X}"
            )

            return value

        # Slot 2
        elif address < 0xC000:
            if self.ram_control & 0x08:
                return self.cart_ram[self.cart_ram_offset(address)]

            offset = self.bank2 * 0x4000 + (address - 0x8000)
            offset %= len(self.cartridge.rom)
            return self.cartridge.rom[offset]

        # RAM reads
        elif address <= 0xFFFF:
            return self.ram[address & 0x1FFF]

    def cart_ram_offset(self, address):
        address = self._normalize_address(address)
        bank = (self.ram_control >> 2) & 0x01
        return bank * 0x4000 + (address - 0x8000)

    def write8(self, address, value):
        address = self._normalize_address(address)
        value &= 0xFF

        # Cartridge RAM
        if 0x8000 <= address < 0xC000:
            if self.ram_control & 0x08:
                self.cart_ram[self.cart_ram_offset(address)] = value

            return

        # Writes to ROM are ignored
        if address < 0xC000:
            return

        # Sega mapper registers, these also land in WRAM so they read back
        if address == 0xFFFC:
            logger.debug(f"MAPPER: ram control {self.ram_control:02X} -> {value:02X}")

            self.ram_control = value

        elif address == 0xFFFD:
            logger.debug(f"MAPPER: bank0 {self.bank0:02X} -> {value:02X}")

            self.bank0 = value

        elif address == 0xFFFE:
            logger.debug(f"MAPPER: bank1 {self.bank1:02X} -> {value:02X}")

            self.bank1 = value

        elif address == 0xFFFF:
            logger.debug(f"MAPPER: bank2 {self.bank2:02X} -> {value:02X}")

            self.bank2 = value

        # Work RAM and its mirror
        self.ram[address & 0x1FFF] = value
