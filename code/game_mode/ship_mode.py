import pygame

from tile import Tile
from .game_mode import GameMode
from game_state.settings_state import SettingsState


class ShipMode(GameMode):
    def __init__(self, player: "Player", texture_path: str, texture_size: tuple[int, int] | None = None) -> None:
        super().__init__(player, texture_path, texture_size)
        self.hitbox = pygame.Rect(2, 10, Tile.SIZE - 2, Tile.SIZE - 10)
        self.jump_height: float = -SettingsState.GRAVITY * 1.8

    def update(self):
        self._player.velocity.y += SettingsState.GRAVITY * self._player.gravity_multiplier
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self._player.velocity.y += self.jump_height * self._player.gravity_multiplier
