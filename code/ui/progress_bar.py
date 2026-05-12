import pygame

class ProgressBar:
    def __init__(self, rect: pygame.Rect, min_value: float | int, max_value: float | int,
                 bg_color: str = "#272727", progress_color: str = "#ff0000", border_radius: int = -1) -> None:
        self.rect = rect
        self.min_value = min_value
        self.max_value = max_value
        self.bg_color = bg_color
        self.progress_color = progress_color
        self.border_radius = border_radius
        self.progress: float = 0

    def set_progress(self, progress: float | int) -> None:
        """progress must be passed in percents."""
        self.progress = progress / 100

    def set_progress_from_value(self, value: float | int) -> None:
        self.progress = round((value - self.min_value) / self.max_value, 2)

    def draw_text(self, surface: pygame.Surface, text: str, font: pygame.Font, f_color: str, bg_color: str | None = None,
                  offset: pygame.typing.SequenceLike[int] | None = None, antialias: bool = True, centered_x: bool= False, centered_y: bool = False) -> None:
        render: pygame.Surface = font.render(text, antialias, f_color, bg_color)
        if offset is None:
            offset = pygame.Vector2(-1, -1)
        offset = pygame.Vector2(offset)

        if offset.x == -1:
            offset.x = self.rect.width / 2 - render.get_width() / 2
        if offset.y == -1:
            offset.y = self.rect.height / 2 - render.get_height() / 2

        if centered_x:
            offset.x += surface.width / 2 - self.rect.width / 2

        if centered_y:
            offset.y += surface.height / 2 - self.rect.height / 2

        surface.blit(render, self.rect.topleft + offset)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.bg_color,  self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, self.progress_color,
                         [self.rect.x, self.rect.y, self.rect.width * self.progress, self.rect.height],
                         border_radius=self.border_radius)

    def draw_centered(self, surface: pygame.Surface, by_x: bool, by_y: bool) -> None:
        x_pos = self.rect.x
        if by_x:
            x_pos = surface.width / 2 - self.rect.width / 2

        y_pos = self.rect.y
        if by_y:
            y_pos = surface.height / 2 - self.rect.height / 2

        pygame.draw.rect(surface, self.bg_color, [x_pos, y_pos, self.rect.width, self.rect.height], border_radius=self.border_radius)
        pygame.draw.rect(surface, self.progress_color,
                         [x_pos, y_pos, self.rect.width * self.progress, self.rect.height],
                         border_radius=self.border_radius)
