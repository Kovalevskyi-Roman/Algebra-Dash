import pygame

from .game_mode import GameMode
from game_state.settings_state import SettingsState


class CubeMode(GameMode):
    def __init__(self, player: "Player", texture_path: str, texture_size: tuple[int, int] | None = None) -> None:
        super().__init__(player, texture_path, texture_size)
        self.jump_height: float = -9
        self.__rotation: float = 0

    def update(self):
        bottom = self._player.collision["bottom"]
        if self._player.gravity_multiplier < 0:
            bottom = self._player.collision["top"]

        if self._player.jump_action and bottom:
            self._player.velocity.y += self.jump_height * self._player.gravity_multiplier
        else:
            self._player.velocity.y += SettingsState.GRAVITY * self._player.gravity_multiplier

        if not bottom:
            self.__rotation -= 3.5 * (1 if self._player.velocity.x > 0 else -1)
        else:
            self.__rotation = round(self.__rotation / 90) * 90

    def draw(self, surface: pygame.Surface, camera_offset: pygame.math.Vector2) -> None:
        if abs(self.__rotation) >= 360:
            self.__rotation = 0

        texture = pygame.transform.rotate(self.texture, self.__rotation)
        if self._player.gravity_multiplier < 0:
            texture = pygame.transform.flip(texture, False, True)

        surface.blit(
            texture,
            self._player.rect.center - camera_offset - texture.get_rect().center
        )
