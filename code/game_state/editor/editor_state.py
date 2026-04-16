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
        self.__mouse_pressed_pos: pygame.Vector2 | None = None  # coordinates in level not on screen!
        self.__selection_rect: pygame.Rect | None = None

        self.__tile_panel_surface: pygame.Surface = pygame.Surface((Window.SIZE[0], Window.SIZE[1] / 5))
        self.__tile_icon_size: tuple[int, int] = (24, 24)
        self.__tile_icon_padding: int = 8
        self.__placeable_tile: str = ""
        self.__selected_tiles: set = set()

        # https://icons8.com/icon/DwTO-Bs0fTYD/hammer icon by https://icons8.com Icons8
        self.__hammer_icon: pygame.Surface = pygame.image.load("../resources/textures/hammer_icon.png").convert_alpha()
        self.__hammer_icon = pygame.transform.flip(self.__hammer_icon, True, False)

        self.__update_tile_panel_surface()

    def __update_tile_panel_surface(self) -> None:
        self.__tile_panel_surface.fill((178, 178, 178))
        x = self.__tile_icon_padding
        y = self.__tile_icon_padding
        for tile in TileManager.TILE_DATA.items():
            if tile[1].get("texture", None) is None:
                continue

            texture = pygame.transform.scale(tile[1].get("texture"), self.__tile_icon_size)
            if tile[0] == self.__placeable_tile:
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
        keys_just_pressed = pygame.key.get_just_pressed()
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        # camera movement
        if keys_pressed[pygame.K_d]:
            self.__camera_offset.x += 8
        elif keys_pressed[pygame.K_a]:
            self.__camera_offset.x -= 8
        if keys_pressed[pygame.K_s]:
            self.__camera_offset.y += 8
        elif keys_pressed[pygame.K_w]:
            self.__camera_offset.y -= 8

        if keys_just_pressed[pygame.K_m]:
            if self.__cursor_mode == CursorMode.SELECT:
                self.__cursor_mode = CursorMode.BUILD
            elif self.__cursor_mode == CursorMode.BUILD:
                self.__cursor_mode = CursorMode.SELECT

        if not mouse_pressed[0]:
            self.__mouse_pressed_pos = None
            self.__selection_rect = None
            return
        if self.__mouse_pressed_pos is None:
            self.__mouse_pressed_pos = mouse_pos.copy() + self.__camera_offset

        # tile panel
        if mouse_pos.y >= Window.SIZE[1] - self.__tile_panel_surface.get_height():
            self.__placeable_tile = ""
            x = self.__tile_icon_padding
            y = self.__tile_icon_padding + Window.SIZE[1] - self.__tile_panel_surface.get_height()
            for tile in TileManager.TILE_DATA.items():
                if tile[1].get("texture", None) is None:
                    continue

                if pygame.Rect((x, y), self.__tile_icon_size).collidepoint(mouse_pos):
                    self.__placeable_tile = tile[0]
                    self.__update_tile_panel_surface()
                    return

                x += self.__tile_icon_size[0] + self.__tile_icon_padding
                if x >= Window.SIZE[0]:
                    x = self.__tile_icon_padding
                    y += self.__tile_icon_size[1] + self.__tile_icon_padding
            self.__update_tile_panel_surface()
            return

        pressed_tile: Tile | None = None
        for tile in self.__tiles:
            if tile.rect.collidepoint(mouse_pos + self.__camera_offset):
                pressed_tile = tile
                break

        if self.__cursor_mode == CursorMode.BUILD and self.__placeable_tile and pressed_tile is None:
            placeable_tile_pos = (mouse_pos + self.__camera_offset) // Tile.SIZE * Tile.SIZE
            new_tile: Tile = TileManager.create_tile(self.__placeable_tile, placeable_tile_pos)
            self.__tiles.append(new_tile)

        if self.__cursor_mode == CursorMode.SELECT:
            # creates selection rectangle
            self.__selection_rect = pygame.Rect(
                self.__mouse_pressed_pos,
                [mouse_pos.x - self.__mouse_pressed_pos.x + self.__camera_offset.x + 1,
                 mouse_pos.y - self.__mouse_pressed_pos.y + self.__camera_offset.y + 1]
                # +1 is if mouse was not moving but tile must be selected
                # (if self.__mouse_pressed_pos - mouse_pos = 0, width and height equals 0 => rect don't collide, so adding 1 fixes it)
            )
            if self.__selection_rect.width < 0:
                self.__selection_rect.width = abs(self.__selection_rect.width)
                self.__selection_rect.x -= self.__selection_rect.width
            if self.__selection_rect.height < 0:
                self.__selection_rect.height = abs(self.__selection_rect.height)
                self.__selection_rect.y -= self.__selection_rect.height
            # check if tiles in this rectangle
            for tile in self.__tiles:
                if self.__selection_rect.colliderect(tile.rect):
                    self.__selected_tiles.add(tile)
                elif tile in self.__selected_tiles:
                    self.__selected_tiles.remove(tile)

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
            if tile in self.__selected_tiles:
                selection_surface = pygame.Surface(tile.rect.size, flags=pygame.SRCALPHA)
                selection_surface.fill((0, 255, 0, 127))
                surface.blit(selection_surface, tile.rect.topleft - self.__camera_offset)

        if self.__cursor_mode == CursorMode.BUILD:
            surface.blit(self.__hammer_icon, pygame.Vector2(pygame.mouse.get_pos()) - pygame.Vector2(12, -6))

        if self.__selection_rect is not None:
            selection_surface = pygame.Surface(self.__selection_rect.size, flags=pygame.SRCALPHA)
            selection_surface.fill((0, 255, 0, 127))
            surface.blit(selection_surface, self.__selection_rect.topleft - self.__camera_offset)

        surface.blit(self.__tile_panel_surface, (0, Window.SIZE[1] - self.__tile_panel_surface.get_height()))
