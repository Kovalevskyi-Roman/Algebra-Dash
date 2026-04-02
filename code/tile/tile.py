import pygame

from common import TILE_SIZE


class Tile:
    def __init__(self, id_: str, position: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        self.id = id_
        self.rect = pygame.Rect(position, [TILE_SIZE, TILE_SIZE])

    def update(self, *args, **kwargs) -> None:
        ...

    def on_player_collide(self, player, *args, **kwargs) -> None:
        ...
