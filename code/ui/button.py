import pygame


class Button:
    def __init__(self, rect: pygame.typing.SequenceLike[int], texture: pygame.Surface | None = None,
                 text: str = "", font: pygame.Font | None = None, antialias: bool = True,
                 f_color: str = "#000000", bg_color: str | None = None) -> None:
        self.rect: pygame.Rect = pygame.Rect(rect)
        if texture is None:
            self.texture = pygame.Surface(self.rect.size)
        else:
            self.texture = texture

        self.text = text
        self.font = font
        self.antialias = antialias
        self.f_color = f_color
        self.bg_color = bg_color
        self.render: pygame.Surface | None = None

        if self.text:
            self.render_text()

    def render_text(self) -> None:
        if not self.font:
            raise ValueError("Unable to render text because font is None")

        self.render = self.font.render(self.text, self.antialias, self.f_color, self.bg_color)

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

    def draw_text(self, surface: pygame.Surface, offset: pygame.typing.SequenceLike[int] | None = None) -> None:
        """if offset x or y is -1 draws text at the center of a button rect"""
        if offset is None:
            offset = pygame.Vector2(-1, -1)
        offset = pygame.Vector2(offset)

        if offset.x == -1:
            offset.x = self.rect.width / 2 - self.render.get_width() / 2
        if offset.y == -1:
            offset.y = self.rect.height / 2 - self.render.get_height() / 2

        surface.blit(self.render, self.rect.topleft + offset)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.texture, self.rect)
