import pygame

from tile import Tile
from .game_mode import GameMode
from game_state.settings_state import SettingsState


class BallMode(GameMode):
    def __init__(self, player: "Player", texture_path: str, texture_size: tuple[int, int] | None = None) -> None:
        super().__init__(player, texture_path, texture_size)
        self.hitbox = pygame.Rect(2, 2, Tile.SIZE - 2, Tile.SIZE - 2)
        self.__rotation: float = 0

    def update(self):
        bottom = self._player.collision["bottom"]
        if self._player.gravity_multiplier < 0:
            bottom = self._player.collision["top"]

        if self._player.just_jump_action and bottom:
            self._player.gravity_multiplier = -self._player.gravity_multiplier

        self._player.velocity.y += SettingsState.GRAVITY * self._player.gravity_multiplier

    def draw(self, surface: pygame.Surface, camera_offset: pygame.math.Vector2) -> None:
        self.__rotation -= self._player.velocity.x * self._player.gravity_multiplier
        if abs(self.__rotation) >= 360:
            self.__rotation = 0

        texture = pygame.transform.rotate(self.texture, self.__rotation)
        surface.blit(texture, self._player.rect.center - camera_offset - texture.get_rect().center)
