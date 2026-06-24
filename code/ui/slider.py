import pygame

from .config import UIConfig


class Slider:
    def __init__(self, position: pygame.Vector2, width: int, min_value: float, max_value: float) -> None:
        self.rect: pygame.Rect = pygame.Rect(position, (width, 16))
        self.min_value = min_value
        self.max_value = max_value
        self.progress: float = 0
        self.value: float | int = self.min_value + self.max_value * self.progress
        self.is_collided: bool = False

    def set_value(self, value: float | int) -> None:
        self.value = round(value, 1)
        self.progress = round((self.value - self.min_value) / (self.max_value - self.min_value), 2)

    def update(self) -> None:
        self.is_collided = False
        if not pygame.mouse.get_pressed()[0]:
            return

        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            return

        self.is_collided = True
        position = pygame.Vector2(pygame.mouse.get_pos()) - pygame.Vector2(self.rect.x, 0)
        self.progress = round(position.x / self.rect.width, 2)
        self.value = round(self.min_value + (self.max_value - self.min_value) * self.progress, 1)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, "#4e4e4e", self.rect, border_radius=4)
        pygame.draw.circle(surface, "#ff0000",
                           (self.rect.x + self.rect.width * self.progress, self.rect.centery),
                           self.rect.height / 2 + 2)

        label = UIConfig.fonts.get("jetbrains_16l").render(str(self.value), True, "#ffffff")
        surface.blit(label, (self.rect.centerx - label.get_width() / 2, self.rect.bottom))
