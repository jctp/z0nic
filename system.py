import os

from display import Display


class SegaMasterSystem:
    def __init__(
        self,
        cpu,
        cartridge,
        io,
        memory,
        logger,
    ):

        self.splash_screen()

        self.cpu = cpu
        self.cartridge = cartridge
        self.io = io
        self.memory = memory

        self.logger = logger
        self.display = Display()

        self.logger.info("Sega Master System setup complete!")

    def run(self):
        self.logger.info("Starting emulation...")

        try:
            while True:
                t_states = self.cpu.step()
                self.io.vdp.tick(t_states)

                if self.io.vdp.frame_complete:
                    self.io.vdp.frame_complete = False
                    self.display.present(self.io.vdp.render_frame())
                    if not self.io.controls.handle_events(self.display.poll_events()):
                        break
                    self.display.wait_for_next_frame()
        finally:
            self.display.close()

    def splash_screen(self):
        def clear_screen():
            os.system("clear")

        clear_screen()

        RED = "\033[31m"
        ORANGE = "\033[38;5;208m"
        YELLOW = "\033[33m"
        GREEN = "\033[32m"
        CYAN = "\033[36m"
        BLUE = "\033[34m"
        MAGENTA = "\033[35m"
        WHITE = "\033[37m"
        RESET = "\033[0m"

        print(f"{BLUE}-{RESET}" * 80)

        print(f"{RED} _______  _______  __    _  ___   _______  {RESET}")
        print(f"{ORANGE}|       ||  _    ||  |  | ||   | |       | {RESET}")
        print(f"{YELLOW}|____   || | |   ||   |_| ||   | |       | {RESET}")
        print(f"{GREEN} ____|  || | |   ||       ||   | |       | {RESET}")
        print(f"{CYAN}| ______|| |_|   ||  _    ||   | |      _| {RESET}")
        print(f"{BLUE}| |_____ |       || | |   ||   | |     |_  {RESET}")
        print(
            f"{MAGENTA}|_______||_______||_|  |__||___| |_______| {WHITE}v0.0.1{RESET}"
        )

        print("")
        print(f"{BLUE}-{RESET}" * 80)
        print('"Doesn\'t crash immediately!"')
        print(f"{BLUE}-{RESET}" * 80)
        print(f"{MAGENTA}(C) {GREEN}James Plant 2026{WHITE} - {RED}MIT Licence{RESET}")
        print(f"{BLUE}-{RESET}" * 80)
