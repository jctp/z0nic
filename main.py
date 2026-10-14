from memory import Memory
from cartridge import Cartridge
from input_output import Input_Output
from vdp import VDP

from z80.z80 import Z80

cart = Cartridge()
cart.load("sonic1sms.sms")

system_memory = Memory(cart)
system_io = Input_Output()
system_cpu = Z80(
    memory=system_memory,
    io=system_io,
    clock_hz=3.58 * 1000000,  # Real CPU is 3.58 Mhz
    exception_on_non_implemented=True,
    register_check=True,
    heartbeat_seconds=0.2,
    opcode_trace=None,
)

while True:
    system_cpu.step()
