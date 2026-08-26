import pygame

from .config import UIConfig
from window import Window


class Entry:
    TEXT: str = "text"
    INT: str = "int"
    FLOAT: str = "float"

    def __init__(self, rect: pygame.Rect, font: pygame.Font, f_color: str, texture: pygame.Surface | None = None,
                 text: str = "", antialias: bool = True, max_text_length: int = 999, type_: str = TEXT) -> None:
        """
        Entry types:
         - **text**: any text is valid
         - **int**: only numbers are allowed
         - **float**: only numbers or numbers with floating point are allowed
        """
        self.rect = rect
        if texture is None:
            self.texture = pygame.Surface(self.rect.size)
        else:
            self.texture = texture
        self.font = font
        self.f_color = f_color
        self.text: list[str] = list(text)
        self.antialias = antialias
        self.max_text_length = max_text_length
        self.type = type_

        self.render: pygame.Surface = self.font.render(self.get_text(), self.antialias, self.f_color)
        self.active: bool = False
        self.blink_timer: float = UIConfig.CURSOR_BLINK_TIME
        self.cursor_pos: int = -1

    def render_text(self) -> None:
        self.render = self.font.render(self.get_text(), self.antialias, self.f_color)

    def get_text(self) -> str:
        return "".join(self.text)

    def set_text(self, text: str) -> None:
        self.text = list(text)
        self.render_text()

    def update(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        mouse_just_pressed = pygame.mouse.get_just_pressed()

        if mouse_just_pressed[0] and self.rect.collidepoint(mouse_pos):
            self.active = True
            pygame.key.start_text_input()
            self.cursor_pos = len(self.text) - 1

        elif mouse_just_pressed[0]:
            self.active = False
            # pygame.key.stop_text_input()

        if not self.active:
            return

        for event in Window.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and self.text:
                    self.text.pop(self.cursor_pos)
                    self.render_text()
                    self.cursor_pos -= 1
                    self.blink_timer += UIConfig.CURSOR_BLINK_TIME

                elif event.key == pygame.K_LEFT:
                    self.cursor_pos -= 1
                    if self.cursor_pos < -1:
                        self.cursor_pos = -1

                elif event.key == pygame.K_RIGHT:
                    self.cursor_pos += 1
                    if self.cursor_pos > len(self.text) - 1:
                        self.cursor_pos = len(self.text) - 1

                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    self.active = False
                    pygame.key.stop_text_input()
                    return

            if event.type == pygame.TEXTINPUT and len(self.text) < self.max_text_length:
                self.cursor_pos += 1
                self.blink_timer += UIConfig.CURSOR_BLINK_TIME
                char: str = event.text
                if self.type == "text":
                    self.text.insert(self.cursor_pos, char)

                elif self.type == "int" and (char.isdigit() or char == "-"):
                    self.text.insert(self.cursor_pos, char)

                elif self.type == "float" and (char.isdigit() or char == "." or char == "-"):
                    self.text.insert(self.cursor_pos, char)

                self.render_text()

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.texture, self.rect)
        render_pos: pygame.Vector2 = pygame.Vector2(
            self.rect.x + self.rect.w / 2 - self.render.width / 2,
            self.rect.y + self.rect.h / 2 - self.render.height / 2
        )
        if self.type == self.INT or self.type == self.FLOAT:
            render_pos.x = self.rect.x + 2

        surface.blit(self.render, render_pos)
        # text width before cursor
        text_width = 0
        if self.text:
            text_width += self.font.size(self.get_text()[:self.cursor_pos + 1])[0]

        self.blink_timer -= Window.DELTA
        if self.blink_timer < -UIConfig.CURSOR_BLINK_TIME:
            self.blink_timer = UIConfig.CURSOR_BLINK_TIME

        if self.active and self.blink_timer > 0:  # cursor rendering
            pygame.draw.rect(
                surface,
                "#ffffff",
                [render_pos.x + text_width + 1, render_pos.y, 2, self.font.get_height()]
            )
