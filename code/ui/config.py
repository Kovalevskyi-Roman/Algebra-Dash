import pygame


class UIConfig:
    fonts: dict[str: pygame.Font] | None = None
    CURSOR_BLINK_TIME: float = 0.45

    @classmethod
    def init(cls) -> None:
        cls.fonts = {
            "tahoma_16": pygame.font.SysFont("tahoma", 16),
            "tahoma_20": pygame.font.SysFont("tahoma", 20),
            "tahoma_26": pygame.font.SysFont("tahoma", 26),
            "jetbrains_16l": pygame.font.Font("../resources/fonts/JetBrainsMono-Light.ttf", 16),
            "jetbrains_20l": pygame.font.Font("../resources/fonts/JetBrainsMono-Light.ttf", 20),
            "jetbrains_20m": pygame.font.Font("../resources/fonts/JetBrainsMono-Medium.ttf", 20),
            "jetbrains_26m": pygame.font.Font("../resources/fonts/JetBrainsMono-Medium.ttf", 26),
            "jetbrains_40m": pygame.font.Font("../resources/fonts/JetBrainsMono-Medium.ttf", 40)
        }
