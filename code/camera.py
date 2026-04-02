import pygame

from window import Window
from player import Player


class Camera:
    def __init__(self, player: Player) -> None:
        self.player = player
        self.offset: pygame.Vector2 = pygame.Vector2(0, 0)
        self.smoothness: float = 0.1

        self.set_offset()

    def set_offset(self, offset: pygame.Vector2 | None = None) -> None:
        """Если offset None, то offset станет таким чтобы player отрисовывался по центру экрана."""
        if offset is None:
            self.offset.x += round(self.player.rect.centerx - (Window.SIZE[0] // 2) - self.offset.x)
            self.offset.y += round(self.player.rect.centery - (Window.SIZE[1] // 2) - self.offset.y)
            return

        self.offset = offset

    def update(self) -> None:
        distance: pygame.Vector2 = pygame.Vector2(
            round(self.player.rect.centerx - (Window.SIZE[0] // 2) - self.offset.x),
            round(self.player.rect.centery - (Window.SIZE[1] // 2) - self.offset.y)
        )

        self.offset += distance * self.smoothness
