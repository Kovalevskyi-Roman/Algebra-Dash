import pygame

from .game_state import GameState
from ui import Button, UIConfig
from window import Window
from level import Level
from tile import Tile
from music_manager import MusicManager
from sfx_manager import SFXManager
from camera import Camera
from player import Player
from timer import Timer


class PlayState(GameState):
    def __init__(self, game_state_manager, *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)

        self.__player: Player | None = None
        self.__level: Level | None = None
        self.__camera: Camera | None = None
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

        self.__death_timer: Timer = Timer(SFXManager.get_length("death_sound") / 1800)
        self.__level_complete_timer: Timer = Timer(SFXManager.get_length("level_complete") / 1800)

        self.__player_offset: pygame.Vector2 = pygame.Vector2(100, 0)
        self.__finish_direction: pygame.Vector2 = pygame.Vector2(0, 0)
        self.__animation_velocity: pygame.Vector2 = pygame.Vector2(0, 0)

    def on_state_enter(self, *args, **kwargs) -> None:
        self.__settings_state = self._game_state_manager.game_states.get(self._game_state_manager.SETTINGS_STATE)
        self.__player = Player(self.__settings_state.player_first_color,
                               self.__settings_state.player_second_color, self.__settings_state.player_icons)
        self.__level = Level()
        self.__level.load(self.level_path, self.__player)
        self.__level.set_player(self.__player)
        self.__camera = Camera(self.__player.rect.center + self.__player_offset)
        self.__is_paused = False
        pygame.mouse.set_visible(False)

    def on_state_exit(self, *args, **kwargs) -> None:
        Level.save_data(self.level_path, death_count=self.__level.death_count)
        self.__player = None
        self.__level = None
        self.__camera = None
        self.level_path = ""
        self.__is_paused = False
        self.__finish_direction = pygame.Vector2(0, 0)
        self.__animation_velocity = pygame.Vector2(0, 0)
        self.__player_offset = pygame.Vector2(100, 0)
        pygame.mouse.set_visible(True)
        MusicManager.stop()
        MusicManager.unload()

    def retry(self) -> None:
        self.__player = Player(self.__settings_state.player_first_color,
                               self.__settings_state.player_second_color, self.__settings_state.player_icons)
        self.__level.reset()
        self.__level.set_player(self.__player)
        self.__camera = Camera(self.__player.rect.center + self.__player_offset)
        pygame.mouse.set_visible(False)
        MusicManager.stop()

    def play_finish_animation(self) -> None:
        if round(self.__player.velocity):  # slows player down
            self.__player.velocity = self.__player.velocity.lerp(pygame.Vector2(0, 0), 0.05)
            self.__player.rect.topleft += self.__player.velocity
        else:  # if player has stopped, plays animation
            self.__player.velocity = pygame.Vector2(0, 0)

            self.__animation_velocity += self.__finish_direction * 0.1
            self.__player.rect.topleft += self.__animation_velocity
            self.__player.game_modes.get(self.__player.current_game_mode).rotation -= self.__animation_velocity.x * 2

        self.__player_offset = self.__player_offset.lerp(pygame.Vector2(-50, Tile.SIZE), self.__animation_velocity.x / 90)
        self.__camera.update(self.__player.rect.center + self.__player_offset)

    def update(self, *args, **kwargs) -> None:
        self.__death_timer.update(self.retry)
        self.__level_complete_timer.update(self._game_state_manager.change_state_to_previous)
        if self.__death_timer.started or self.__level is None:
            return

        if self.__level_complete_timer.started:
            self.play_finish_animation()
            return

        if not MusicManager.playing:
            MusicManager.play(start=self.__level.music_start_pos)

        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self.__is_paused = not self.__is_paused
            pygame.mouse.set_visible(self.__is_paused)

        if self.__is_paused and not MusicManager.paused:
            MusicManager.pause()
        elif not self.__is_paused and MusicManager.paused:
            MusicManager.unpause()

        if self.__is_paused:
            if self.__play_btn.is_just_pressed():
                self.__is_paused = False
                pygame.time.delay(100)

            elif self.__retry_btn.is_just_pressed():
                self.retry()
                self.__is_paused = False
                pygame.time.delay(100)

            elif self.__back_btn.is_just_pressed():
                self._game_state_manager.change_state_to_previous()
                self.__is_paused = True

            pygame.mouse.set_visible(self.__is_paused)
            return

        self.__player.platformer_mode = self.__settings_state.platformer_mode

        self.__camera.update(self.__player.rect.center + self.__player_offset)
        self.__level.update(self.__camera.offset)

        if self.__level.current_progress >= 100:
            MusicManager.fade_out(1000)
            SFXManager.play("level_complete")
            self.__level_complete_timer.start()
            # find's finish direction for animation
            finish_screen_pos = pygame.Vector2(
                self.__level.get_finish_screen_x(Window.SIZE[0], self.__camera.offset),
                (self.__level.ground_tile.rect.y - Tile.SIZE * 6.5 - self.__camera.offset.y)
            )
            self.__finish_direction = finish_screen_pos - (self.__player.rect.center - self.__camera.offset)
            self.__finish_direction = self.__finish_direction.normalize()

            Level.save_data(self.level_path, max_progress=100, death_count=self.__level.death_count)
            return

        if self.__settings_state.is_player_immortal:
            self.__player.alive = True

        if not self.__player.alive:
            MusicManager.fade_out(100)
            SFXManager.play("death_sound")
            self.__death_timer.start()

            self.__level.death_count += 1
            if self.__level.current_progress > self.__level.max_progress:

                self.__level.max_progress = self.__level.current_progress
                self.__level.save_data(
                    self.level_path,
                    max_progress=self.__level.current_progress,
                    death_count=self.__level.death_count
                )

            if self.__settings_state.pause_after_death:
                self.__is_paused = True

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.__level.draw(surface, self.__camera.offset, self.__settings_state.show_triggers, self.__settings_state.show_hitboxes)

        if self.__settings_state.show_hitboxes and not self.__level_complete_timer.started:
            self.__player.draw_hitbox(surface, self.__camera.offset)

        self.__camera.draw(surface)

        if self.__is_paused and not self.__death_timer.started:
            surface.blit(self.__pause_surface, [0, 0])

        # current progress
        render: pygame.Surface = UIConfig.create_label("jetbrains_16l", f"{self.__level.current_progress}%")
        surface.blit(render, [surface.width / 2 - render.width / 2, 0])
