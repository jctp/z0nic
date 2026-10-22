from memory import Memory
from cartridge import Cartridge

from z80.z80 import Z80

cart = Cartridge()
cart.load("sonic1sms.sms")

sms_memory = Memory(cart)
sms_io = None
z80 = Z80(
    memory=sms_memory,
    io=None,
    clock_hz=1000  # Real CPU is 3.58 Mhz
)

while True:
    z80.step()
