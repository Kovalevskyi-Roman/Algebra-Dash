import pygame

from tile import Tile
from game_state.icon_editor_state import IconEditorState

class GameMode:
    def __init__(self, player: "Player") -> None:
        self._player = player
        self.hitbox: pygame.Rect = pygame.Rect(0, 0, Tile.SIZE, Tile.SIZE)
        self.texture: pygame.Surface | None = None

    def load_texture(self, game_mode: str) -> None:
        self.texture = IconEditorState.icons.get(game_mode)[self._player.icons.get(game_mode, 0)]
        self.texture = IconEditorState.get_colored_icon(self.texture, self._player.first_color, self._player.second_color)

    def update(self):
        ...

    def draw(self, surface: pygame.Surface, camera_offset: pygame.math.Vector2) -> None:
        if self._player.gravity_multiplier < 0:
            surface.blit(
                pygame.transform.flip(self.texture, False, True),
                self._player.rect.topleft - camera_offset + self.hitbox.topleft
            )
            return

        surface.blit(self.texture, self._player.rect.topleft - camera_offset)
