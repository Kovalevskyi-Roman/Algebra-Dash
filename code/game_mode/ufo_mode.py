import pygame

from .game_mode import GameMode
from tile import Tile
from game_state.settings_state import SettingsState
from game_state.icon_editor_state import IconEditorState


class UfoMode(GameMode):
    def __init__(self, player: "Player") -> None:
        super().__init__(player)
        self.load_texture("ufo")

        self.jump_height: float = -9
        self.hitbox = pygame.Rect(2, 4, Tile.SIZE - 4, Tile.SIZE - 4)

        self.__cube_icon = IconEditorState.icons.get("cube")[self._player.icons.get("cube", 0)]
        self.__cube_icon = IconEditorState.get_colored_icon(self.__cube_icon, self._player.first_color, self._player.second_color)
        self.__cube_icon = pygame.transform.scale_by(self.__cube_icon, 0.45)

        self.texture.blit(
            self.__cube_icon,
            (Tile.SIZE / 2 - self.__cube_icon.width / 2, Tile.SIZE / 2 - self.__cube_icon.height / 2)
        )

    def update(self) -> None:
        self._player.velocity.y += SettingsState.GRAVITY * self._player.gravity_multiplier

        if self._player.just_jump_action:
            self._player.velocity.y = self.jump_height * self._player.gravity_multiplier

    def draw(self, surface: pygame.Surface, camera_offset: pygame.math.Vector2) -> None:
        self.rotation = self._player.velocity.y * -self._player.gravity_multiplier * 1.25

        texture = pygame.transform.rotate(self.texture, self.rotation)
        padding = pygame.Vector2(0, 0)
        if self._player.gravity_multiplier < 0:
            texture = pygame.transform.flip(texture, False, True)
            padding.y = self.hitbox.y

        surface.blit(
            texture,
            self._player.rect.center - camera_offset - texture.get_rect().center + padding
        )
