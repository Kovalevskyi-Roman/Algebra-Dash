import pygame

from common import TILE_SIZE


class Player:
    def __init__(self) -> None:
        self.rect: pygame.FRect = pygame.FRect(0, 0, TILE_SIZE, TILE_SIZE)
        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)
        self.move_speed: float = 4
        self.jump_height: float = -5

    def update(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.velocity.x = self.move_speed
        elif keys[pygame.K_a]:
            self.velocity.x = -self.move_speed
        else:
            self.velocity.x = 0

        self.rect.topleft += self.velocity

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, "#ffffff", self.rect)
