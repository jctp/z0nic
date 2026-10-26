import pygame

SMS_WIDTH = 256
SMS_HEIGHT = 192
SCALE = 3
# NTSC SMS refresh rate is ~59.92 Hz
TARGET_FPS = 60


class Display:
    def __init__(self, title="Z0nic"):
        pygame.init()
        self.screen = pygame.display.set_mode((SMS_WIDTH * SCALE, SMS_HEIGHT * SCALE))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

    # Converts a frame (192 rows of 256 RGB tuples) to a scaled window surface and shows it.
    def present(self, frame):
        # The first frame can still have unrendered rows; skip it until complete
        if frame is None or None in frame:
            return

        surface = pygame.image.frombytes(b"".join(frame), (SMS_WIDTH, SMS_HEIGHT), "RGB")
        scaled = pygame.transform.scale(surface, self.screen.get_size())
        self.screen.blit(scaled, (0, 0))
        pygame.display.flip()

    # Sleeps as needed so the loop runs at real time, called once per presented frame.
    def wait_for_next_frame(self):
        self.clock.tick(TARGET_FPS)

    # Pumps the window event queue; returns the events for the controls to consume.
    def poll_events(self):
        return pygame.event.get()

    def close(self):
        pygame.quit()
