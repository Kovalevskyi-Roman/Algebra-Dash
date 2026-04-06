import pygame


class UIConfig:
    fonts: dict[str: pygame.Font] | None = None

    @classmethod
    def init(cls) -> None:
        cls.fonts = {
            "tahoma_20": pygame.font.SysFont("tahoma", 20),
        }
