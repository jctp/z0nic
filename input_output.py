from logger import logger
from vdp import VDP
from controls import Controls


class Input_Output:
    def __init__(self):
        self.vdp = VDP()
        self.controls = Controls()

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
            return value

        # Joypad
        if port in (0xDC, 0xC0):
            return self.controls.read_port_a()
        if port in (0xDD, 0xC1):
            return self.controls.read_port_b()

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
