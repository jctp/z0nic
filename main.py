import time

import time

from memory import Memory
from cartridge import Cartridge
from z80 import Z80
from z80 import Z80

cart = Cartridge()


cart.load("sonic1sms.bin")


system_memory = Memory(cart)
system_cpu = Z80(system_memory)
system_cpu = Z80(system_memory)

while True:
    system_cpu.step()
    # time.sleep(0.01)
