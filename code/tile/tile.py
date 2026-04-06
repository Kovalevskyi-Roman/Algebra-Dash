import pygame


class Tile:
    SIZE: int = 32
    TILE: str = "tile"
    FOLLOW_TILE: str = "follow_tile"

    def __init__(self, id_: str, position: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        self.id = id_
        self.rect = pygame.Rect(position, [self.SIZE, self.SIZE])

    def update(self, *args, **kwargs) -> None:
        if self.id == self.FOLLOW_TILE:
            self.rect.x = kwargs.get("player").rect.x

    def on_player_collide(self, *args, **kwargs) -> None:
        ...
