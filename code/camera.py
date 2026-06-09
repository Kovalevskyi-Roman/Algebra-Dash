import pygame

from window import Window
from tile import Tile


class Camera:
    def __init__(self, target: pygame.Vector2 | pygame.typing.SequenceLike[int | float]) -> None:
        self.target = pygame.Vector2(target)
        self.offset: pygame.Vector2 = pygame.Vector2(0, 0)
        self.smoothness: float = 0.085
        # then value closer to 0 then smoother camera will be

        self.set_offset()

    def set_offset(self, offset: pygame.Vector2 | None = None) -> None:
        """Sets target at the center of the screen if offset is None."""
        if offset is None:
            self.offset.x += round(self.target.x - (Window.SIZE[0] // 2) - self.offset.x)
            self.offset.y += round(self.target.y - (Window.SIZE[1] // 2) - self.offset.y - Tile.SIZE)
            return

        self.offset = offset

    def update(self, target: pygame.Vector2 | pygame.typing.SequenceLike[int | float]) -> None:
        self.target = pygame.Vector2(target)
        distance: pygame.Vector2 = pygame.Vector2(
            round(self.target.x - (Window.SIZE[0] // 2) - self.offset.x),
            round(self.target.y - (Window.SIZE[1] // 2) - self.offset.y - Tile.SIZE)
        )

        self.offset += distance * self.smoothness
