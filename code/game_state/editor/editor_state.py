import enum
import pygame

from game_state.game_state import GameState
from level import Level
from tile import Tile, TileManager
from window import Window


class CursorMode(enum.Enum):
    SELECT = 0
    BUILD = 1


class EditorState(GameState):
    def __init__(self, game_state_manager, *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)

        self.__tiles: list[Tile] = list()
        self.level_path: str = ""

        self.__camera_offset: pygame.Vector2 = pygame.Vector2(-500, -500)
        self.__cursor_mode: CursorMode = CursorMode.SELECT

        self.__tile_panel_surface: pygame.Surface = pygame.Surface((Window.SIZE[0], Window.SIZE[1] / 5))
        self.__tile_icon_size: tuple[int, int] = (24, 24)
        self.__tile_icon_padding: int = 8
        self.__selected_tile: str = Tile.TILE

        self.__update_tile_panel_surface()

    def __update_tile_panel_surface(self) -> None:
        self.__tile_panel_surface.fill((178, 178, 178))
        x = self.__tile_icon_padding
        y = self.__tile_icon_padding
        for tile in TileManager.TILE_DATA.items():
            if tile[1].get("texture", None) is None:
                continue

            texture = pygame.transform.scale(tile[1].get("texture"), self.__tile_icon_size)
            if tile[0] == self.__selected_tile:
                pygame.draw.rect(
                    self.__tile_panel_surface,
                    "#17ff17",
                    [
                        x - self.__tile_icon_padding / 4,
                        y - self.__tile_icon_padding / 4,
                        self.__tile_icon_size[0] + self.__tile_icon_padding / 2,
                        self.__tile_icon_size[1] + self.__tile_icon_padding / 2
                    ],
                )
            self.__tile_panel_surface.blit(texture, (x, y))

            x += self.__tile_icon_size[0] + self.__tile_icon_padding
            if x >= Window.SIZE[0]:
                x = self.__tile_icon_padding
                y += self.__tile_icon_size[1] + self.__tile_icon_padding

    def on_state_enter(self, *args, **kwargs) -> None:
        self.__tiles = Level.get_tiles(self.level_path)
        self.__tiles.append(TileManager.create_tile(Tile.TILE, [0, 0]))

    def on_state_exit(self, *args, **kwargs) -> None:
        self.__tiles.clear()
        self.level_path = ""

    def update(self, *args, **kwargs) -> None:
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_d]:
            self.__camera_offset.x += 8
        elif keys_pressed[pygame.K_a]:
            self.__camera_offset.x -= 8
        if keys_pressed[pygame.K_s]:
            self.__camera_offset.y += 8
        elif keys_pressed[pygame.K_w]:
            self.__camera_offset.y -= 8

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        # X axis line
        pygame.draw.line(
            surface, "#0000ff",
            [0, -self.__camera_offset.y + Tile.SIZE], [surface.get_width(), -self.__camera_offset.y + Tile.SIZE]
        )
        # Y axis line
        pygame.draw.line(
            surface, "#00ff00",
            [-self.__camera_offset.x, 0], [-self.__camera_offset.x, surface.get_height()]
        )
        for tile in self.__tiles:
            TileManager.draw_tile(tile, surface, self.__camera_offset)

        surface.blit(self.__tile_panel_surface, (0, Window.SIZE[1] - self.__tile_panel_surface.get_height()))
