from memory import Memory
from cartridge import Cartridge
from input_output import Input_Output

from z80.z80 import Z80

cart = Cartridge()
cart.load("sonic1sms.bin")

system_memory = Memory(cart)

system_io = Input_Output()

system_cpu = Z80(
    memory=system_memory,
    io=system_io,
    clock_hz=30,  # Real CPU is 3.58 Mhz
    exception_on_non_implemented=True,
)

while True:
    system_cpu.step()
