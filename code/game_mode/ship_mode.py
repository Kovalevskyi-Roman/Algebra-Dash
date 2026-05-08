import pygame

from tile import Tile
from .game_mode import GameMode
from game_state.settings_state import SettingsState


class ShipMode(GameMode):
    def __init__(self, player: "Player", texture_path: str, texture_size: tuple[int, int] | None = None) -> None:
        super().__init__(player, texture_path, texture_size)
        self.hitbox = pygame.Rect(2, 10, Tile.SIZE - 2, Tile.SIZE - 10)
        self.jump_height: float = -SettingsState.GRAVITY * 1.8
        self.__rotation: float = 0

    def update(self):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self._player.velocity.y += self.jump_height * self._player.gravity_multiplier

        self._player.velocity.y += SettingsState.GRAVITY * self._player.gravity_multiplier

    def draw(self, surface: pygame.Surface, camera_offset: pygame.math.Vector2) -> None:
        self.__rotation = self._player.velocity.y * -self._player.gravity_multiplier * 3

        texture = pygame.transform.rotate(self.texture, self.__rotation)
        padding = pygame.Vector2(0, 0)
        if self._player.gravity_multiplier < 0:
            texture = pygame.transform.flip(texture, False, True)
            padding.y = self.hitbox.y

        surface.blit(
            texture,
            self._player.rect.center - camera_offset - texture.get_rect().center + padding
        )
