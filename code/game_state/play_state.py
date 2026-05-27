import pygame

from level import Level
from music_manager import MusicManager
from tile import TileManager
from ui import Button
from window import Window
from .game_state import GameState
from camera import Camera
from player import Player


class PlayState(GameState):
    def __init__(self, game_state_manager, *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)

        self.__player: Player | None = None
        self.__camera: Camera | None = None
        self.__level: Level | None = None
        self.level_path: str = ""
        self.__is_paused: bool = False
        self.__pause_surface: pygame.Surface = pygame.Surface(Window.SIZE, flags=pygame.SRCALPHA)
        self.__pause_surface.fill("#1111117f")

        self.__play_btn_size: pygame.Vector2 = pygame.Vector2(140, 140)
        self.__play_btn: Button = Button(
            pygame.Rect(
                (Window.SIZE[0] / 2 - self.__play_btn_size.x / 2, 320 - self.__play_btn_size.y / 2),
                self.__play_btn_size
            ),
            pygame.image.load("../resources/textures/ui/play_button_round.png").convert_alpha()
        )
        self.__play_btn.scale_texture_to_rect()

        self.__retry_btn_size: pygame.Vector2 = pygame.Vector2(110, 110)
        self.__retry_btn: Button = Button(
            pygame.Rect(
                (Window.SIZE[0] / 3 - self.__retry_btn_size.x / 2, 320 - self.__retry_btn_size.y / 2),
                self.__retry_btn_size
            ),
            pygame.image.load("../resources/textures/ui/retry_button.png").convert_alpha()
        )
        self.__retry_btn.scale_texture_to_rect()

        self.__back_btn_size: pygame.Vector2 = pygame.Vector2(110, 110)
        self.__back_btn: Button = Button(
            pygame.Rect(
                (Window.SIZE[0] * (2 / 3) - self.__back_btn_size.x / 2, 320 - self.__back_btn_size.y / 2),
                self.__back_btn_size
            ),
            pygame.image.load("../resources/textures/ui/back_button.png").convert_alpha()
        )
        self.__back_btn.scale_texture_to_rect()

        self.__play_btn.draw(self.__pause_surface)
        self.__retry_btn.draw(self.__pause_surface)
        self.__back_btn.draw(self.__pause_surface)

        self.__settings_state: GameState | None = None

    def on_state_enter(self, *args, **kwargs) -> None:
        self.__player = Player()
        self.__camera = Camera(self.__player.rect.center)
        self.__level = Level()
        self.__level.load(self.level_path, self.__player)
        self.__is_paused = False
        self.__settings_state = self._game_state_manager.game_states.get(self._game_state_manager.SETTINGS_STATE)
        MusicManager.play(start=self.__level.music_start_pos)

    def on_state_exit(self, *args, **kwargs) -> None:
        Level.save_data(self.level_path, death_count=self.__level.death_count)
        self.__player = None
        self.__camera = None
        self.__level = None
        self.level_path = ""
        self.__is_paused = False
        MusicManager.stop()
        MusicManager.unload()

    def retry(self) -> None:
        self.__player = Player()
        self.__camera = Camera(self.__player.rect.center)
        self.__level.set_player(self.__player)
        MusicManager.stop()
        MusicManager.play(start=self.__level.music_start_pos)

    def update(self, *args, **kwargs) -> None:
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self.__is_paused = not self.__is_paused

            if self.__is_paused:
                MusicManager.pause()
            else:
                MusicManager.unpause()

        if self.__is_paused:
            if self.__play_btn.is_pressed():
                self.__is_paused = False
            elif self.__retry_btn.is_pressed():
                self.retry()
                self.__is_paused = False
            elif self.__back_btn.is_pressed():
                self._game_state_manager.change_state_to_previous()
            return
        self.__player.platformer_mode = self.__settings_state.platformer_mode

        self.__camera.update(self.__player.rect.center)
        self.__level.update(self.__camera.offset)

        if self.__level.current_progress >= 100:
            Level.save_data(self.level_path, max_progress=100, death_count=self.__level.death_count)
            self._game_state_manager.change_state_to_previous()
            return

        if self.__settings_state.is_player_immortal:
            self.__player.alive = True

        if not self.__player.alive:
            self.__level.death_count += 1
            if self.__level.current_progress > self.__level.max_progress:
                self.__level.save_data(self.level_path,
                                       max_progress=self.__level.current_progress,
                                       death_count=self.__level.death_count
                                       )

            if self.__settings_state.pause_after_death:
                self.__is_paused = True

            self.retry()

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.__level.draw(surface, self.__camera.offset)

        if self.__settings_state.show_hitboxes:
            for tile in self.__level.tiles:
                TileManager.draw_tile_hitbox(tile, surface, self.__camera.offset)

            self.__player.draw_hitbox(surface, self.__camera.offset)

        if self.__is_paused:
            surface.blit(self.__pause_surface, [0, 0])
