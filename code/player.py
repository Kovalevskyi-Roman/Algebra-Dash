import pygame

from tile import Tile
from game_mode import GameMode, CubeMode, ShipMode


class Player:
    CUBE_MODE: type[GameMode] = CubeMode
    SHIP_MODE: type[ShipMode] = ShipMode

    def __init__(self) -> None:
        self.rect: pygame.FRect = pygame.FRect(0, 0, Tile.SIZE, Tile.SIZE)
        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)
        self.move_speed: float = 4
        self.jump_height: float = -9
        self.collision: dict[str, bool] = {
            "top": False, "left": False, "bottom": False, "right": False
        }
        self.alive = True
        self.gravity_multiplier: float = 1

        self.game_modes: dict[type[GameMode], GameMode] = {
            self.CUBE_MODE: CubeMode(self, "../resources/textures/game_modes/cube_mode.png"),
            self.SHIP_MODE: ShipMode(self, "../resources/textures/game_modes/ship_mode.png")
        }
        self.current_game_mode: type[GameMode] = self.SHIP_MODE

    def update(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.velocity.x = self.move_speed
        elif keys[pygame.K_a]:
            self.velocity.x = -self.move_speed
        else:
            self.velocity.x = 0

        self.game_modes.get(self.current_game_mode).update()

    def draw_hitbox(self, surface: pygame.Surface, camera_offset: pygame.Vector2) -> None:
        game_mode_hitbox = self.game_modes.get(self.current_game_mode).hitbox
        hitbox = pygame.FRect(self.rect.topleft + (game_mode_hitbox.topleft - camera_offset), game_mode_hitbox.size)
        pygame.draw.rect(surface, "#00ff00", hitbox, width=1)

    def draw(self, surface: pygame.Surface, camera_offset: pygame.Vector2) -> None:
        self.game_modes.get(self.current_game_mode).draw(surface, camera_offset)
