from logger import logger

from pathlib import Path


class Cartridge:
    def __init__(self):
        self.rom = bytearray()

    def load(self, filename):
        self.rom = bytearray(Path(filename).read_bytes())
        logger.info(f"Loaded ROM: {filename} of size {len(self.rom)} bytes.")

    def read_header(self):
        header_locations = [0x7FF0, 0x3FF0, 0x1FF0]
        for loc in header_locations:
            header = str(self.rom[loc : loc + 8])
            logger.info(f"ROM header: {header}")
