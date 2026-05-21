import pygame


class Button:
    def __init__(self, rect: pygame.typing.SequenceLike[int], texture: pygame.Surface) -> None:
        self.rect: pygame.Rect = pygame.Rect(rect)
        self.texture = texture

    def is_hovered(self) -> bool:
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_just_pressed(self, button: int = 0) -> bool:
        return self.is_hovered() and pygame.mouse.get_just_pressed()[button]

    def is_just_released(self, button: int = 0) -> bool:
        return self.is_hovered() and pygame.mouse.get_just_released()[button]

    def is_pressed(self, button: int = 0) -> bool:
        return self.is_hovered() and pygame.mouse.get_pressed()[button]

    def scale_texture_to_rect(self) -> None:
        self.texture = pygame.transform.scale(self.texture, self.rect.size)

    def draw_text(self, surface: pygame.Surface, text: str, font: pygame.Font, f_color: str, bg_color: str | None = None,
                  offset: pygame.typing.SequenceLike[int] | None = None, antialias: bool = True) -> None:
        """if offset x or y is -1 draws text at the center of a button rect"""
        render: pygame.Surface = font.render(text, antialias, f_color, bg_color)
        if offset is None:
            offset = pygame.Vector2(-1, -1)
        offset = pygame.Vector2(offset)

        if offset.x == -1:
            offset.x = self.rect.width / 2 - render.get_width() / 2
        if offset.y == -1:
            offset.y = self.rect.height / 2 - render.get_height() / 2

        surface.blit(render, self.rect.topleft + offset)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.texture, self.rect)
