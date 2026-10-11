import time
from memory import Memory
from cartridge import Cartridge
from z80 import Z80

cart = Cartridge()
cart.load("sonic1sms.bin")

system_memory = Memory(cart)
system_cpu = Z80(
    memory = system_memory,
    clock_hz = 10, # Real CPU is 3.58 Mhz
    exception_on_non_implemented = True
    )

while True:
    system_cpu.step()
