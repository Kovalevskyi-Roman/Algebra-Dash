import pygame

from tile import Tile
from game_mode import GameMode, CubeMode, ShipMode, BallMode, WaveMode


class Player:
    CUBE_MODE: type[GameMode] = CubeMode
    SHIP_MODE: type[ShipMode] = ShipMode
    BALL_MODE: type[BallMode] = BallMode
    WAVE_MODE: type[WaveMode] = WaveMode

    def __init__(self) -> None:
        self.rect: pygame.FRect = pygame.FRect(0, 0, Tile.SIZE, Tile.SIZE)
        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)
        self.move_speed: float = 4.25
        self.collision: dict[str, bool] = {
            "top": False, "left": False, "bottom": False, "right": False
        }
        self.alive: bool = True
        self.platformer_mode: bool = False
        self.gravity_multiplier: float = 1

        self.game_modes: dict[type[GameMode], GameMode] = {
            self.CUBE_MODE: CubeMode(self, "../resources/textures/game_modes/cube_mode.png"),
            self.SHIP_MODE: ShipMode(self, "../resources/textures/game_modes/ship_mode.png"),
            self.BALL_MODE: BallMode(self, "../resources/textures/game_modes/ball_mode.png"),
            self.WAVE_MODE: WaveMode(self, "../resources/textures/game_modes/wave_mode.png")
        }
        self.current_game_mode: type[GameMode] = self.CUBE_MODE

        self.jump_action: bool = False
        self.just_jump_action: bool = False

    def update(self) -> None:
        pressed_keys = pygame.key.get_pressed()
        just_pressed_keys = pygame.key.get_just_pressed()
        pressed_mouse = pygame.mouse.get_pressed()
        just_pressed_mouse = pygame.mouse.get_just_pressed()

        self.jump_action = pressed_keys[pygame.K_SPACE] or pressed_mouse[0]
        self.just_jump_action = just_pressed_keys[pygame.K_SPACE] or just_pressed_mouse[0]

        self.velocity.x = self.move_speed
        if self.platformer_mode:
            if pressed_keys[pygame.K_d]:
                self.velocity.x = self.move_speed
            elif pressed_keys[pygame.K_a]:
                self.velocity.x = -self.move_speed
            else:
                self.velocity.x = 0

        self.game_modes.get(self.current_game_mode).update()

        if self.collision["right"]:
            self.alive = False

    def draw_hitbox(self, surface: pygame.Surface, camera_offset: pygame.Vector2) -> None:
        game_mode_hitbox = self.game_modes.get(self.current_game_mode).hitbox
        hitbox = pygame.FRect(self.rect.topleft + (game_mode_hitbox.topleft - camera_offset), game_mode_hitbox.size)
        pygame.draw.rect(surface, "#00ff00", hitbox, width=1)

    def draw(self, surface: pygame.Surface, camera_offset: pygame.Vector2) -> None:
        self.game_modes.get(self.current_game_mode).draw(surface, camera_offset)
