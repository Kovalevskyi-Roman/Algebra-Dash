import pygame


class Window:
    SIZE: tuple[int, int] = (1200, 675)
    FPS: int = 60
    events: tuple[pygame.event.Event, ...] = ()
    running: bool = True

    def __init__(self) -> None:
        self.surface: pygame.Surface = pygame.display.set_mode(self.SIZE)
        self.clock: pygame.time.Clock = pygame.time.Clock()

    @classmethod
    def update_events(cls) -> None:
        cls.events = tuple(pygame.event.get())
        if pygame.QUIT in cls.events:
            cls.running = False

    def fill(self, color) -> None:
        self.surface.fill(color)

    def tick(self) -> None:
        self.clock.tick(self.FPS)

    def update(self) -> None:
        pygame.display.update()
