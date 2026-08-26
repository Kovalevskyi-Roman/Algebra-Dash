import pygame


class UIConfig:
    fonts: dict[str: pygame.Font] | None = None
    CURSOR_BLINK_TIME: float = 0.45

    CHECKBOX_SIZE: tuple[int, int] = (32, 32)
    CHECKBOX_TEXTURE: pygame.Surface | None = None
    CHECKBOX_ACTIVE_TEXTURE: pygame.Surface | None = None

    @classmethod
    def init(cls) -> None:
        cls.fonts = {
            "jetbrains_16l": pygame.font.Font("../resources/fonts/JetBrainsMono-Light.ttf", 16),
            "jetbrains_20l": pygame.font.Font("../resources/fonts/JetBrainsMono-Light.ttf", 20),
            "jetbrains_20m": pygame.font.Font("../resources/fonts/JetBrainsMono-Medium.ttf", 20),
            "jetbrains_26m": pygame.font.Font("../resources/fonts/JetBrainsMono-Medium.ttf", 26),
            "jetbrains_40m": pygame.font.Font("../resources/fonts/JetBrainsMono-Medium.ttf", 40)
        }

        cls.CHECKBOX_TEXTURE = pygame.image.load("../resources/textures/ui/checkbox.png").convert_alpha()
        cls.CHECKBOX_TEXTURE = pygame.transform.scale(cls.CHECKBOX_TEXTURE, cls.CHECKBOX_SIZE)
        cls.CHECKBOX_ACTIVE_TEXTURE = pygame.image.load("../resources/textures/ui/checkbox_active.png").convert_alpha()
        cls.CHECKBOX_ACTIVE_TEXTURE = pygame.transform.scale(cls.CHECKBOX_ACTIVE_TEXTURE, cls.CHECKBOX_SIZE)

    @classmethod
    def create_label(cls, font_name: str, text: str, f_color: str = "#ffffff",
                     bg_color: str | None = None, antialias: bool = True) -> pygame.Surface:
        font = cls.fonts.get(font_name, None)
        if font is None:
            raise ValueError(f"Font '{font_name}' does not exist")

        return font.render(text, antialias, f_color, bg_color)

    @classmethod
    def fix_hex_color(cls, color: str) -> str:
        if not color:
            color = "#000000"

        if color[0] != "#":
            color = "#" + color.strip("#")

        if len(color) != 7:
            color = (color + "000000")[:7]

        return color
