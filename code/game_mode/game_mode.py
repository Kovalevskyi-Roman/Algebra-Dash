import pygame

from tile import Tile


class GameMode:
    def __init__(self, player: "Player", texture_path: str, texture_size: tuple[int, int] | None = None) -> None:
        self._player = player
        self.hitbox: pygame.Rect = pygame.Rect(0, 0, Tile.SIZE, Tile.SIZE)
        self.texture: pygame.Surface | None = None

        self.load_texture(texture_path, texture_size)

    def load_texture(self, texture_path: str, texture_size: tuple[int, int] | None) -> None:
        if texture_size is None:
            texture_size = (Tile.SIZE, Tile.SIZE)

        self.texture = pygame.image.load(texture_path).convert_alpha()
        self.texture = pygame.transform.scale(self.texture, texture_size)

    def update(self):
        ...

    def draw(self, surface: pygame.Surface, camera_offset: pygame.math.Vector2) -> None:
        surface.blit(self.texture, self._player.rect.topleft - camera_offset)
