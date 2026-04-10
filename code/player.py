import pygame

from tile import Tile


class Player:
    def __init__(self) -> None:
        self.rect: pygame.FRect = pygame.FRect(0, 0, Tile.SIZE, Tile.SIZE)
        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)
        self.move_speed: float = 4
        self.jump_height: float = -5
        self.collision: dict[str, bool] = {
            "top": False, "left": False, "bottom": False, "right": False
        }

    def update(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.velocity.x = self.move_speed
        elif keys[pygame.K_a]:
            self.velocity.x = -self.move_speed
        else:
            self.velocity.x = 0

        if self.collision["bottom"] and keys[pygame.K_SPACE]:
            self.velocity.y = self.jump_height
        else:
            self.velocity.y += 0.1

    def draw(self, surface: pygame.Surface, camera_offset: pygame.Vector2) -> None:
        pygame.draw.rect(surface, "#ffffff", [self.rect.topleft - camera_offset, self.rect.size])
