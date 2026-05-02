import pygame


class Window:
    SIZE: tuple[int, int] = (1200, 675)
    FPS: int = 60
    DELTA: float = 1 / FPS
    events: tuple[pygame.event.Event, ...] = ()
    running: bool = True

    def __init__(self) -> None:
        self.surface: pygame.Surface = pygame.display.set_mode(self.SIZE)
        self.clock: pygame.time.Clock = pygame.time.Clock()

    @classmethod
    def update_events(cls) -> None:
        cls.events = tuple([e for e in pygame.event.get()])
        for e in cls.events:
            if e.type == pygame.QUIT:
                cls.running = False

    def fill(self, color) -> None:
        self.surface.fill(color)

    def tick(self) -> None:
        self.clock.tick(self.FPS)

    def update(self) -> None:
        pygame.display.update()
