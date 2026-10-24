from logger import logger
from vdp import VDP


class Input_Output:
    def __init__(self):
        self.vdp = VDP()

        # Generic port storage for unimplemented devices
        self.ports = [0xFF] * 256

    def read(self, port):
        port &= 0xFF

        # V counter
        if port == 0x7E:
            return self.vdp._get_v_counter()

        # H counter
        if port == 0x7F:
            return self.vdp._get_h_counter()

        # VDP
        if port in (0xBE, 0xBF):
            value = self.vdp.read(port)

            logger.debug(f"VDP READ  port={port:02X} value={value:02X}")

            return value

        value = self.ports[port]

        return value

    def write(self, port, value):
        port &= 0xFF
        value &= 0xFF

        # VDP
        if port in (0xBE, 0xBF):
            self.vdp.write(port, value)
            return

        self.ports[port] = value
