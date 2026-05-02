import pygame

from .config import UIConfig
from window import Window


class Entry:
    def __init__(self, rect: pygame.Rect, texture: pygame.Surface, font: pygame.Font, f_color: str,
                 text: str = "", antialias: bool = True, max_text_length: int = 999) -> None:
        self.rect = rect
        self.texture = texture
        self.font = font
        self.f_color = f_color
        self.text: list[str] = list(text)
        self.antialias = antialias
        self.max_text_length = max_text_length

        self.active: bool = False
        self.blink_timer: float = UIConfig.CURSOR_BLINK_TIME
        self.cursor_pos: int = -1

    def get_text(self) -> str:
        return "".join(self.text)

    def set_text(self, text: str) -> None:
        self.text = list(text)

    def update(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        mouse_just_pressed = pygame.mouse.get_just_pressed()

        if mouse_just_pressed[0] and self.rect.collidepoint(mouse_pos):
            self.active = True
            pygame.key.start_text_input()
            self.cursor_pos = len(self.text) - 1

        elif mouse_just_pressed[0]:
            self.active = False
            pygame.key.stop_text_input()

        if not self.active:
            return

        for event in Window.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and self.text:
                    self.text.pop(self.cursor_pos)
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

            if event.type == pygame.TEXTINPUT and len(self.text) < self.max_text_length:
                self.cursor_pos += 1
                self.text.insert(self.cursor_pos, event.text)
                self.blink_timer += UIConfig.CURSOR_BLINK_TIME

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.texture, self.rect)
        render: pygame.Surface = self.font.render(self.get_text(), self.antialias, self.f_color)
        render_pos: pygame.Vector2 = pygame.Vector2(
            self.rect.x + self.rect.w / 2 - render.width / 2,
            self.rect.y + self.rect.h / 2 - render.height / 2
        )
        surface.blit(render, render_pos)
        # text width before cursor
        width = 0
        if self.text:
            width += self.font.size(self.get_text()[:self.cursor_pos + 1])[0]

        self.blink_timer -= Window.DELTA
        if self.blink_timer < -UIConfig.CURSOR_BLINK_TIME:
            self.blink_timer = UIConfig.CURSOR_BLINK_TIME

        if self.active and self.blink_timer > 0:  # cursor rendering
            pygame.draw.rect(
                surface,
                "#ffffff",
                [render_pos.x + width,
                 render_pos.y, 2, self.font.get_height()]
            )
