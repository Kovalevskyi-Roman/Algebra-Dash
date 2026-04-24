import pygame

from .game_mode import GameMode
from game_state.settings_state import SettingsState


class CubeMode(GameMode):
    def __init__(self, player: "Player", texture_path: str, texture_size: tuple[int, int] | None = None) -> None:
        super().__init__(player, texture_path, texture_size)
        self.jump_height: float = -9

    def update(self):
        if self._player.collision["bottom"] and pygame.key.get_pressed()[pygame.K_SPACE]:
            self._player.velocity.y = self.jump_height
        else:
            self._player.velocity.y += SettingsState.GRAVITY * self._player.gravity_multiplier
