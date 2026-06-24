import pygame

from .game_mode import GameMode
from game_state.settings_state import SettingsState
from tile.tile import Tile


class CubeMode(GameMode):
    def __init__(self, player: "Player") -> None:
        super().__init__(player)
        self.load_texture("cube")

        self.jump_height: float = -9

    def dash(self) -> None:
        self._player.velocity = self._player.dash_direction * self._player.move_speed
        self.rotation -= 3.5 * (1 if self._player.velocity.x >= 0 else -1)

    def update(self):
        if self._player.rect.y < -Tile.SIZE * 64:
            self._player.alive = False
            return

        bottom = self._player.collision["bottom"]
        if self._player.gravity_multiplier < 0:
            bottom = self._player.collision["top"]

        if self._player.jump_action and bottom:
            self._player.velocity.y += self.jump_height * self._player.gravity_multiplier
        else:
            self._player.velocity.y += SettingsState.GRAVITY * self._player.gravity_multiplier

        if not bottom:
            self.rotation -= 3.5 * (1 if self._player.velocity.x >= 0 else -1)
        else:
            self.rotation = round(self.rotation / 90) * 90

    def draw(self, surface: pygame.Surface, camera_offset: pygame.math.Vector2) -> None:
        if abs(self.rotation) >= 360:
            self.rotation = 0

        texture = pygame.transform.rotate(self.texture, self.rotation)
        if self._player.gravity_multiplier < 0:
            texture = pygame.transform.flip(texture, False, True)

        surface.blit(
            texture,
            self._player.rect.center - camera_offset - texture.get_rect().center
        )
