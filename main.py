from memory import Memory
from cartridge import Cartridge
from input_output import Input_Output
from vdp import VDP

from z80.z80 import Z80

cart = Cartridge()
cart.load("sonic1sms.sms")

sms_memory = Memory(cart)
sms_io = Input_Output()
z80 = Z80(
    memory=sms_memory,
    io=sms_io,
    clock_hz=3.58 * 1000000,  # Real CPU is 3.58 Mhz
    exception_on_non_implemented=True,
    register_check=True,
    heartbeat_seconds=None,
    opcode_trace=None,
)

while True:
    z80.step()
