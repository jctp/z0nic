from system import SegaMasterSystem

from memory import Memory
from cartridge import Cartridge
from input_output import Input_Output
from z80.z80 import Z80

from logger import logger

sms_cartridge = Cartridge()
sms_cartridge.load("sonic1sms.sms")

sms_memory = Memory(cartridge=sms_cartridge)
sms_io = Input_Output()
z80 = Z80(
    memory=sms_memory,
    io=sms_io,
    clock_hz=3.56 * 100000,  # Real CPU is 3.58 Mhz
    log_opcodes=False,
)

console = SegaMasterSystem(
    cpu=z80,
    cartridge=sms_cartridge,
    io=sms_io,
    memory=sms_memory,
    logger=logger,
    frame_dump_dir="frames",
    frame_dump_interval=60,
)

console.run()
