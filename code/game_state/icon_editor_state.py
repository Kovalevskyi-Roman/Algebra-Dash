import pathlib
import pygame

from ui import Entry, UIConfig
from window import Window
from .game_state import GameState
from tile import Tile


class IconEditorState(GameState):
    icons: dict[str, list[pygame.Surface]] | None = None
    # {"game_mode": [icon_0, icon_1, icon_N]}

    def __init__(self, game_state_manager, *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)
        self.__settings_state: GameState | None = None

        self.__first_color_entry: Entry = Entry(
            pygame.Rect(5, 5, Window.SIZE[0] / 2 - 10, 45),
            pygame.Surface((Window.SIZE[0] / 2 - 10, 45)),
            UIConfig.fonts.get("jetbrains_20l"),
            "#000000",
            max_text_length=7
        )
        self.__first_color_entry.texture.fill("#646464")

        self.__second_color_entry: Entry = Entry(
            pygame.Rect(Window.SIZE[0] / 2 + 5, 5, Window.SIZE[0] / 2 - 10, 45),
            pygame.Surface((Window.SIZE[0] / 2 - 10, 45)),
            UIConfig.fonts.get("jetbrains_20l"),
            "#000000",
            max_text_length=7
        )
        self.__second_color_entry.texture.fill("#646464")

        self.__colored_icons: dict[str, list[pygame.Surface]] = dict()

    def on_state_enter(self, *args, **kwargs) -> None:
        self.__settings_state = self._game_state_manager.game_states.get(self._game_state_manager.SETTINGS_STATE)
        self.__first_color_entry.set_text(self.__settings_state.player_first_color)
        self.__second_color_entry.set_text(self.__settings_state.player_second_color)
        self.__colored_icons = self.get_colored_icons(self.__settings_state.player_first_color, self.__settings_state.player_second_color)

    @classmethod
    def get_icon_form_path(cls, texture_name: str) -> pygame.Surface:
        texture_path: str = f"../resources/textures/game_modes/{texture_name}"
        texture: pygame.Surface = pygame.image.load(texture_path).convert_alpha()
        texture = pygame.transform.scale(texture, (Tile.SIZE, Tile.SIZE))

        return texture

    @classmethod
    def get_colored_icon(cls, texture: pygame.Surface, first_color: pygame.Color, second_color: pygame.Color) -> pygame.Surface:
        colored_texture: pygame.Surface = texture.copy()
        first_color_mask: pygame.Color = pygame.Color("#ff0000")
        second_color_mask: pygame.Color = pygame.Color("#00ff00")

        for y in range(texture.get_height()):
            for x in range(texture.get_width()):
                if texture.get_at((x, y)) == first_color_mask:
                    colored_texture.set_at((x, y), first_color)

                elif texture.get_at((x, y)) == second_color_mask:
                    colored_texture.set_at((x, y), second_color)

        return colored_texture

    @classmethod
    def load_icons(cls) -> None:
        cls.icons = dict()

        path: pathlib.Path = pathlib.Path("../resources/textures/game_modes/")
        for obj in path.iterdir():
            if not obj.is_file():
                continue

            if obj.suffix != ".png":
                continue

            split_file_name: list[str] = obj.stem.split("_")
            game_mode_name: str = split_file_name[0]
            texture_index: int = int(split_file_name[2])
            if cls.icons.get(game_mode_name, None) is None:
                cls.icons.setdefault(game_mode_name, list())

            cls.icons.get(game_mode_name).insert(
                texture_index,
                cls.get_icon_form_path(obj.name)
            )

    @classmethod
    def get_colored_icons(cls, first_color: pygame.Color | str, second_color: pygame.Color | str) -> dict[str, list[pygame.Surface]]:
        colored_icons: dict[str, list[pygame.Surface]] = dict()
        for key in cls.icons:
            colored_icons[key] = [cls.get_colored_icon(icon, first_color, second_color) for icon in cls.icons[key]]

        return colored_icons

    def update(self, *args, **kwargs) -> None:
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            if self.__first_color_entry.active or self.__second_color_entry.active:
                self.__first_color_entry.active = False
                self.__second_color_entry.active = False
            else:
                self._game_state_manager.change_state(self._game_state_manager.MENU_STATE)

        if not self.__first_color_entry.active and not self.__second_color_entry.active:
            pygame.key.stop_text_input()

        self.__first_color_entry.update()
        if not self.__first_color_entry.active and self.__settings_state.player_first_color != self.__first_color_entry.get_text():
            self.__first_color_entry.set_text(UIConfig.fix_hex_color(self.__first_color_entry.get_text()))
            self.__settings_state.player_first_color = self.__first_color_entry.get_text()
            self.__colored_icons = self.get_colored_icons(self.__settings_state.player_first_color, self.__settings_state.player_second_color)

        self.__second_color_entry.update()
        if not self.__second_color_entry.active and self.__settings_state.player_second_color != self.__second_color_entry.get_text():
            self.__second_color_entry.set_text(UIConfig.fix_hex_color(self.__second_color_entry.get_text()))
            self.__settings_state.player_second_color = self.__second_color_entry.get_text()
            self.__colored_icons = self.get_colored_icons(self.__settings_state.player_first_color, self.__settings_state.player_second_color)

        if not pygame.mouse.get_just_pressed()[0]:
            return

        y: int = 75
        x: int = 5
        for game_mode in self.__colored_icons.keys():
            for i in range(len(self.__colored_icons.get(game_mode, []))):
                if pygame.Rect(x, y, Tile.SIZE, Tile.SIZE).collidepoint(pygame.mouse.get_pos()):
                    self.__settings_state.player_icons[game_mode] = i

                x += Tile.SIZE + 5

            y += Tile.SIZE + 15
            x = 5

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.__first_color_entry.draw(surface)
        self.__second_color_entry.draw(surface)

        y: int = 75
        x: int = 5
        for game_mode in self.__colored_icons.keys():
            icons = self.__colored_icons.get(game_mode, [])
            for icon in icons:
                if icons.index(icon) == self.__settings_state.player_icons.get(game_mode, 0):
                    pygame.draw.rect(surface, "#00ff00", [x - 2, y - 2, Tile.SIZE + 4, Tile.SIZE + 4], 2)

                surface.blit(icon, (x, y))

                x += Tile.SIZE + 5

            y += Tile.SIZE + 15
            x = 5
