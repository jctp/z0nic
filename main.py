from memory import Memory
from cartridge import Cartridge

cart = Cartridge()
cart.load("sonic1sms.bin")
cart.read_header()
system_memory = Memory(cart)

for i in range(int(0xFFFF)):
    system_memory.read8(i)
