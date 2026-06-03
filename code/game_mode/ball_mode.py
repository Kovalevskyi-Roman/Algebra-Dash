import pygame

from tile import Tile
from .game_mode import GameMode
from game_state.settings_state import SettingsState


class BallMode(GameMode):
    def __init__(self, player: "Player") -> None:
        super().__init__(player)
        self.load_texture("ball")

        self.hitbox = pygame.Rect(2, 2, Tile.SIZE - 4, Tile.SIZE - 4)
        self.__rotation: float = 0

    def update(self):
        bottom = self._player.collision["bottom"]
        if self._player.gravity_multiplier < 0:
            bottom = self._player.collision["top"]

        if self._player.just_jump_action and bottom:
            self._player.gravity_multiplier = -self._player.gravity_multiplier

        self._player.velocity.y += SettingsState.GRAVITY * self._player.gravity_multiplier

        self.__rotation -= self._player.velocity.x * self._player.gravity_multiplier
        if abs(self.__rotation) >= 360:
            self.__rotation = 0

    def draw(self, surface: pygame.Surface, camera_offset: pygame.math.Vector2) -> None:
        texture = pygame.transform.rotate(self.texture, self.__rotation)
        surface.blit(texture, self._player.rect.center - camera_offset - texture.get_rect().center)
