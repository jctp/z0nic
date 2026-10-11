from logger import logger


class Input_Output:
    def __init__(self):
        self.ports = [0xFF] * 256

    def read(self, port):
        port &= 0xFF  # Keep only lowest 8 bits
        logger.debug(f"IO Read: {port:02X}")
        return self.ports[port]

    def write(self, port, value):
        port &= 0xFF
        value &= 0xFF
        self.ports[port] = value
        logger.debug(f"IO Write: {value:02X} -> {port:02X}")
