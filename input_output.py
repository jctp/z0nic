from logger import logger


class Input_Output:
    def __init__(self):
        self.ports = [0xFF] * 256

    def read(self, port):
        port &= 0xFF  # Keep only lowest 8 bits
        value = self.ports[port]
        logger.debug(
            f"IO READ  port={port:02X} value={value:02X}"
        )
        return value

    def write(self, port, value):
        port &= 0xFF
        value &= 0xFF

        logger.debug(
            f"IO WRITE port={port:02X} value={value:02X}"
        )

        self.ports[port] = value
