import os

class SegaMasterSystem:
    def __init__(self, cpu, cartridge, io, memory, logger):

        self.splash_screen()
        
        self.cpu = cpu
        self.cartridge = cartridge
        self.io = io
        self.memory = memory

        self.logger = logger

        self.logger.info("Sega Master System setup complete!")

    def run(self):
        self.logger.info("Starting emulation...")
        while True:
            t_states = self.cpu.step()
            self.io.vdp.tick(t_states)

    def splash_screen(self):
        def clear_screen():
            os.system("clear")

        clear_screen()
        print("-" * 80)
        print(" _______  _______  __    _  ___   _______")
        print("|       ||  _    ||  |  | ||   | |       |")
        print("|____   || | |   ||   |_| ||   | |       |")
        print(" ____|  || | |   ||       ||   | |       |")
        print("| ______|| |_|   ||  _    ||   | |      _|")
        print("| |_____ |       || | |   ||   | |     |_ ")
        print("|_______||_______||_|  |__||___| |_______| v0.???")
        print("")
        print("-" * 80)
        print("PRE-PRE-PRE-ALPHA")
        print("-" * 80)