import pygame


class UIConfig:
    fonts: dict[str: pygame.Font] | None = None

    @classmethod
    def init(cls) -> None:
        cls.fonts = {

        }
