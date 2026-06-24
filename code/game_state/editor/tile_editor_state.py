import enum
import pygame

from game_state.game_state import GameState
from level import Level
from music_manager import MusicManager
from tile import Tile, TileManager
from window import Window
from ui import Button, Slider


class CursorMode(enum.Enum):
    SELECT = 0
    BUILD = 1
    ROTATE = 2
    SCALE = 3


class TileEditorState(GameState):
    def __init__(self, game_state_manager, *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)

        self.__tiles: list[Tile] = list()
        self.level_path: str = ""

        self.__camera_scroll: pygame.Vector2 = pygame.Vector2(-500, -300)
        self.__cursor_mode: CursorMode = CursorMode.SELECT
        self.__mouse_pressed_pos: pygame.Vector2 | None = None  # coordinates in level not on screen!
        self.__selection_rect: pygame.Rect | None = None

        self.__tile_panel_surface: pygame.Surface = pygame.Surface((Window.SIZE[0], Window.SIZE[1] / 5), flags=pygame.SRCALPHA)
        self.__tile_icon_size: tuple[int, int] = (24, 24)
        self.__tile_icon_padding: int = 8
        self.__placeable_tile: str = ""
        self.__selected_tiles: set = set()
        self.__draw_hitboxes: bool = False
        self.__was_redacted: bool = False
        self.__bg_color: str = ""

        # https://icons8.com/icon/DwTO-Bs0fTYD/hammer icon by https://icons8.com Icons8
        self.__hammer_icon: pygame.Surface = pygame.image.load("../resources/textures/hammer_icon.png").convert_alpha()
        self.__hammer_icon = pygame.transform.flip(self.__hammer_icon, True, False)

        # tile grid surface
        self.__grid_surface: pygame.Surface = pygame.Surface(Window.SIZE + pygame.Vector2(Tile.SIZE, Tile.SIZE) * 2, flags=pygame.SRCALPHA)
        for i in range(self.__grid_surface.height // Tile.SIZE):
            pygame.draw.line(
                self.__grid_surface, "#323232",
                [0, Tile.SIZE * i], [self.__grid_surface.get_width(), Tile.SIZE * i]
            )
        for i in range(self.__grid_surface.width // Tile.SIZE):
            pygame.draw.line(
                self.__grid_surface, "#323232",
                [Tile.SIZE * i, 0], [Tile.SIZE * i, self.__grid_surface.get_height()]
            )

        # music control
        self.__play_music_btn: Button = Button(
            pygame.Rect(8, Window.SIZE[1] / 2 - 32, 24, 24),
            pygame.Surface((24, 24))
        )
        self.__play_music_btn.texture.fill("#ffffff")

        self.__remote_music_btn: Button = Button(
            pygame.Rect(8, Window.SIZE[1] / 2, 24, 24),
            pygame.Surface((24, 24))
        )
        self.__remote_music_btn.texture.fill("#0000ff")

        self.__stop_music_btn: Button = Button(
            pygame.Rect(8, Window.SIZE[1] / 2 + 32, 24, 24),
            pygame.Surface((24, 24))
        )
        self.__stop_music_btn.texture.fill("#ff0000")
        self.__music_pos: float = 0
        self.__music_speed: float = 4.25

        self.__tile_rotation_slider: Slider = Slider(
            pygame.Vector2(Window.SIZE[0] / 2 - 190, Window.SIZE[1] / 2), 500,
            -180, 180
        )

        self.__tile_scale_x_slider: Slider = Slider(
            pygame.Vector2(Window.SIZE[0] / 2 - 190, Window.SIZE[1] / 2 - 40), 380,
            0.5, 4
        )
        self.__tile_scale_y_slider: Slider = Slider(
            pygame.Vector2(Window.SIZE[0] / 2 - 190, Window.SIZE[1] / 2 + 40), 380,
            0.5, 4
        )

        self.__x_scroll_slider: Slider = Slider(
            pygame.Vector2(Window.SIZE[0] / 4, 0), Window.SIZE[0] // 2,
            -1000, 1000
        )

    def on_state_enter(self, *args, **kwargs) -> None:
        self.__tiles = Level.get_tiles(self.level_path)
        self.__camera_scroll = pygame.Vector2(Level.levels.get(self.level_path).get("editor_scroll"))
        self.__x_scroll_slider.max_value = Level.get_finish_pos(self.__tiles).x + 1000
        self.__x_scroll_slider.set_value(self.__camera_scroll.x)
        self.__update_tile_panel_surface()
        self.__bg_color = Level.levels.get(self.level_path).get("bg_color", "#171727")
        MusicManager.load(Level.levels.get(self.level_path).get("music_name"))
        self.__music_pos = 0
        self.__music_speed = 4.25

    def on_state_exit(self, *args, **kwargs) -> None:
        Level.save_tiles(self.level_path, self.__tiles)
        if self.__was_redacted:
            Level.save_data(self.level_path, max_progress=0, editor_scroll=self.__camera_scroll)
            self.__was_redacted = False
        else:
            Level.save_data(self.level_path, editor_scroll=self.__camera_scroll)

        self.__tiles.clear()
        self.level_path = ""
        self.__camera_scroll = pygame.Vector2(-500, -300)
        self.__cursor_mode = CursorMode.SELECT
        self.__placeable_tile = ""
        self.__selected_tiles.clear()
        self.__mouse_pressed_pos = None
        self.__selection_rect = None
        self.__draw_hitboxes = False
        MusicManager.stop()
        MusicManager.unload()

    def __update_music_line_pos(self, position: float) -> float:
        position += self.__music_speed
        for tile in self.__tiles:
            if tile.__dict__.get("speed", None) is None:
                continue

            if self.__music_pos > tile.rect.x:
                self.__music_speed = tile.__dict__.get("speed")

        return position

    def __get_music_line_pos(self) -> float:
        music_pos: float = 0
        music_time: float = 1
        self.__music_speed = 4.25

        while music_time < MusicManager.position:
            music_time += Window.DELTA
            music_pos = self.__update_music_line_pos(music_pos)

        return music_pos

    def __update_tile_panel_surface(self) -> None:
        self.__tile_panel_surface.fill("#7A7A7A7f")
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

    def update(self, *args, **kwargs) -> None:
        keys_pressed = pygame.key.get_pressed()
        keys_just_pressed = pygame.key.get_just_pressed()
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

        if keys_just_pressed[pygame.K_ESCAPE]:
            if self.__cursor_mode != CursorMode.SELECT:
                self.__cursor_mode = CursorMode.SELECT
                return

            self._game_state_manager.change_state_to_previous()

        # level saving
        if (keys_pressed[pygame.K_LCTRL] or keys_pressed[pygame.K_RCTRL]) and keys_just_pressed[pygame.K_s]:
            Level.save_tiles(self.level_path, self.__tiles)
            if self.__was_redacted:
                Level.save_data(self.level_path, max_progress=0, editor_scroll=self.__camera_scroll)
                self.__was_redacted = False
            else:
                Level.save_data(self.level_path, editor_scroll=self.__camera_scroll)
            self.__x_scroll_slider.max_value = Level.get_finish_pos(self.__tiles).x + 1000
            self.__x_scroll_slider.set_value(self.__camera_scroll.x)
            return

        # camera movement
        if keys_pressed[pygame.K_d]:
            self.__camera_scroll.x += 8
            self.__x_scroll_slider.set_value(self.__camera_scroll.x)
        elif keys_pressed[pygame.K_a]:
            self.__camera_scroll.x -= 8
            self.__x_scroll_slider.set_value(self.__camera_scroll.x)
        if keys_pressed[pygame.K_s]:
            self.__camera_scroll.y += 8
        elif keys_pressed[pygame.K_w]:
            self.__camera_scroll.y -= 8

        # tile movement
        step: int = 2
        if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]:
            step = Tile.SIZE
        if keys_just_pressed[pygame.K_LEFT]:
            for tile in self.__selected_tiles:
                tile.rect.x -= step
        elif keys_just_pressed[pygame.K_RIGHT]:
            for tile in self.__selected_tiles:
                tile.rect.x += step
        elif keys_just_pressed[pygame.K_UP]:
            for tile in self.__selected_tiles:
                tile.rect.y -= step
        elif keys_just_pressed[pygame.K_DOWN]:
            for tile in self.__selected_tiles:
                tile.rect.y += step

        # cursor mode
        if keys_just_pressed[pygame.K_m]:
            if self.__cursor_mode == CursorMode.BUILD:
                self.__cursor_mode = CursorMode.SELECT
            else:
                self.__cursor_mode = CursorMode.BUILD
                self.__was_redacted = True

        # tile rotation mode
        elif keys_just_pressed[pygame.K_r]:
            if self.__cursor_mode == CursorMode.ROTATE:
                self.__cursor_mode = CursorMode.SELECT

            elif self.__selected_tiles:
                self.__cursor_mode = CursorMode.ROTATE
                self.__tile_rotation_slider.set_value(list(self.__selected_tiles)[0].rotation)

        # tile scaling mode
        elif keys_just_pressed[pygame.K_t]:
            if self.__cursor_mode == CursorMode.SCALE:
                self.__cursor_mode = CursorMode.SELECT

            elif self.__selected_tiles:
                self.__cursor_mode = CursorMode.SCALE
                self.__tile_scale_x_slider.set_value(list(self.__selected_tiles)[0].scale_x)
                self.__tile_scale_y_slider.set_value(list(self.__selected_tiles)[0].scale_y)

        elif keys_just_pressed[pygame.K_h]:
            self.__draw_hitboxes = not self.__draw_hitboxes

        # tile flip
        elif keys_just_pressed[pygame.K_x]:
            for tile in self.__selected_tiles:
                tile.flip_by(not tile.flip_x, tile.flip_y)
        elif keys_just_pressed[pygame.K_y]:
            for tile in self.__selected_tiles:
                tile.flip_by(tile.flip_x, not tile.flip_y)

        # tile deleting
        elif keys_just_pressed[pygame.K_BACKSPACE] or keys_just_pressed[pygame.K_DELETE]:
            for tile in self.__selected_tiles:
                self.__tiles.remove(tile)

            self.__selected_tiles.clear()

        # x scroll slider
        self.__x_scroll_slider.update()
        if self.__x_scroll_slider.value != self.__camera_scroll.x:
            self.__camera_scroll.x = int(self.__x_scroll_slider.value)
        if self.__x_scroll_slider.is_collided:
            self.__mouse_pressed_pos = None
            self.__selection_rect = None
            return

        # music control buttons
        if self.__play_music_btn.is_just_pressed():
            if not MusicManager.playing:
                MusicManager.play(start=Level.levels.get(self.level_path).get("music_start_pos"))
            elif MusicManager.paused:
                MusicManager.unpause()
            else:
                MusicManager.pause()

        elif self.__stop_music_btn.is_pressed() and MusicManager.playing:
            self.__music_pos = 0
            self.__music_speed = 4.25
            MusicManager.stop()

        elif self.__remote_music_btn.is_just_pressed() and MusicManager.playing:
            self.__music_pos = self.__get_music_line_pos()
            MusicManager.rewind_by(1)

        # music line update
        if MusicManager.playing and not MusicManager.paused:
            self.__music_pos = self.__update_music_line_pos(self.__music_pos)

        if not mouse_pressed[0]:
            self.__mouse_pressed_pos = None
            self.__selection_rect = None
            return
        if self.__mouse_pressed_pos is None:
            self.__mouse_pressed_pos = mouse_pos.copy() + self.__camera_scroll

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

        # tile rotation
        if self.__cursor_mode == CursorMode.ROTATE:
            first_selected: Tile = list(self.__selected_tiles)[0]

            self.__tile_rotation_slider.update()
            if first_selected.rotation != self.__tile_rotation_slider.value:
                for tile in self.__selected_tiles:
                    TileManager.set_tile_rotation(tile, self.__tile_rotation_slider.value)

        # tile scaling
        if self.__cursor_mode == CursorMode.SCALE:
            first_selected: Tile = list(self.__selected_tiles)[0]
            self.__tile_scale_x_slider.update()
            self.__tile_scale_y_slider.update()
            if first_selected.scale_x != self.__tile_scale_x_slider.value:
                for tile in self.__selected_tiles:
                    tile.set_x_scale(round(self.__tile_scale_x_slider.value, 2))

            if first_selected.scale_y != self.__tile_scale_y_slider.value:
                for tile in self.__selected_tiles:
                    tile.set_y_scale(round(self.__tile_scale_y_slider.value, 2))

        # is any tile pressed
        pressed_tile: Tile | None = None
        pressed_tile_hit_box: bool = False
        for tile in self.__tiles:
            if tile.rect.collidepoint(mouse_pos + self.__camera_scroll):
                pressed_tile = tile
                tile_hitbox_rect = pygame.FRect(
                    tile.rect.x + tile.hitbox.x, tile.rect.y + tile.hitbox.y,
                    tile.hitbox.width, tile.hitbox.height
                )
                if tile_hitbox_rect.collidepoint(mouse_pos + self.__camera_scroll):
                    pressed_tile_hit_box = True
                break

        # is it possible to place new tile
        if self.__cursor_mode == CursorMode.BUILD and self.__placeable_tile and pressed_tile is None:
            placeable_tile_pos = (mouse_pos + self.__camera_scroll) // Tile.SIZE * Tile.SIZE
            new_tile: Tile = TileManager.create_tile(self.__placeable_tile, placeable_tile_pos)
            self.__tiles.append(new_tile)

        if self.__cursor_mode == CursorMode.SELECT:
            # creates selection rectangle
            self.__selection_rect = pygame.Rect(
                self.__mouse_pressed_pos,
                [mouse_pos.x + self.__camera_scroll.x - self.__mouse_pressed_pos.x,
                 mouse_pos.y + self.__camera_scroll.y - self.__mouse_pressed_pos.y]
            )
            # flips rectangle
            if self.__selection_rect.width < 0:
                self.__selection_rect.width = abs(self.__selection_rect.width)
                self.__selection_rect.x -= self.__selection_rect.width
            if self.__selection_rect.height < 0:
                self.__selection_rect.height = abs(self.__selection_rect.height)
                self.__selection_rect.y -= self.__selection_rect.height
            # check if tiles in this rectangle
            for tile in self.__tiles:
                tile_hitbox_rect = pygame.FRect(
                    tile.rect.x + tile.hitbox.x, tile.rect.y + tile.hitbox.y,
                    tile.hitbox.width, tile.hitbox.height
                )
                if self.__selection_rect.colliderect(tile_hitbox_rect):
                    self.__selected_tiles.add(tile)
                elif tile in self.__selected_tiles and not keys_pressed[pygame.K_LCTRL]:
                    self.__selected_tiles.remove(tile)

            if pressed_tile and pressed_tile_hit_box:
                self.__selected_tiles.add(pressed_tile)

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        surface.fill(self.__bg_color)
        # tile grid
        surface.blit(self.__grid_surface, [-self.__camera_scroll.x % Tile.SIZE - Tile.SIZE, -self.__camera_scroll.y % Tile.SIZE - Tile.SIZE])
        # X axis line
        pygame.draw.line(
            surface, "#0000ff",
            [0, -self.__camera_scroll.y + Tile.SIZE], [surface.get_width(), -self.__camera_scroll.y + Tile.SIZE],
            width=3
        )
        # Y axis line
        pygame.draw.line(
            surface, "#00ff00",
            [-self.__camera_scroll.x - Tile.SIZE, 0], [-self.__camera_scroll.x - Tile.SIZE, surface.get_height()],
            width=3
        )
        # music position line
        pygame.draw.line(
            surface, "#003fa3",
            [self.__music_pos - self.__camera_scroll.x, 0], [self.__music_pos - self.__camera_scroll.x, surface.get_height()]
        )
        # tiles
        for tile in self.__tiles:
            if TileManager.draw_tile(tile, surface, self.__camera_scroll):
                # if tile is a game mode portal
                if tile.id in [Tile.SHIP_PORTAL, Tile.BALL_PORTAL, Tile.WAVE_PORTAL]:
                    # ceil level line
                    pygame.draw.line(
                        surface, pygame.Color("#ffffff") - pygame.Color(self.__bg_color),
                                 tile.rect.center - self.__camera_scroll - pygame.Vector2(0, tile.ceil_level * Tile.SIZE),
                        [surface.get_width(), tile.rect.centery - self.__camera_scroll.y - tile.ceil_level * Tile.SIZE],
                        width=3
                    )
                    # ground level line
                    pygame.draw.line(
                        surface, pygame.Color("#ffffff") - pygame.Color(self.__bg_color),
                                 tile.rect.center - self.__camera_scroll + pygame.Vector2(0, tile.ground_level * Tile.SIZE),
                        [surface.get_width(), tile.rect.centery - self.__camera_scroll.y + tile.ground_level * Tile.SIZE],
                        width=3
                    )

                if self.__draw_hitboxes:
                    TileManager.draw_tile_hitbox(tile, surface, self.__camera_scroll)

                if tile in self.__selected_tiles:
                    selection_surface = pygame.Surface(tile.hitbox.size, flags=pygame.SRCALPHA)
                    selection_surface.fill((0, 255, 0, 127))
                    surface.blit(selection_surface, tile.rect.topleft - self.__camera_scroll + tile.hitbox.topleft)

        # selection rect
        if self.__selection_rect is not None:
            selection_surface = pygame.Surface(self.__selection_rect.size, flags=pygame.SRCALPHA)
            selection_surface.fill((0, 255, 0, 127))
            surface.blit(selection_surface, self.__selection_rect.topleft - self.__camera_scroll)

        # hammer icon
        if self.__cursor_mode == CursorMode.BUILD:
            surface.blit(self.__hammer_icon, pygame.Vector2(pygame.mouse.get_pos()) - pygame.Vector2(12, -6))

        elif self.__cursor_mode == CursorMode.ROTATE:
            self.__tile_rotation_slider.draw(surface)

        elif self.__cursor_mode == CursorMode.SCALE:
            self.__tile_scale_x_slider.draw(surface)
            self.__tile_scale_y_slider.draw(surface)

        self.__x_scroll_slider.draw(surface)

        # music control buttons
        self.__play_music_btn.draw(surface)
        if MusicManager.playing:
            self.__stop_music_btn.draw(surface)
            self.__remote_music_btn.draw(surface)

        # tile panel
        surface.blit(self.__tile_panel_surface, (0, Window.SIZE[1] - self.__tile_panel_surface.get_height()))
