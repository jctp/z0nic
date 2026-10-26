import pygame

# SMS joypad port bits are active-low: a pressed button clears its bit.
UP = 0x01
DOWN = 0x02
LEFT = 0x04
RIGHT = 0x08
BUTTON_1 = 0x10
BUTTON_2 = 0x20

KEY_MAP = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
    pygame.K_z: BUTTON_1,
    pygame.K_x: BUTTON_2,
}


class Controls:
    def __init__(self):
        # Pressed buttons for joypad 1, as a bitmask of the SMS button bits.
        self.pad_1 = 0
        self.pad_2 = 0

    # Consumes window events and updates the pressed-button state.
    # Returns False when the window has been closed.
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                bit = KEY_MAP.get(event.key)
                if bit is None:
                    continue
                if event.type == pygame.KEYDOWN:
                    self.pad_1 |= bit
                else:
                    self.pad_1 &= ~bit
        return True

    # Port 0xDC / 0xC0: joypad 1 buttons, active-low. Bits 6-7 are unused (high).
    def read_port_a(self):
        return ((~self.pad_1) & 0x3F) | 0xC0

    # Port 0xDD / 0xC1: joypad 2 buttons and reset, active-low. No second pad is wired up.
    def read_port_b(self):
        return 0xFF
