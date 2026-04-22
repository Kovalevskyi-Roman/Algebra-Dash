import pygame

from .tile import Tile


class Spike(Tile):
    def __init__(self, id_: str, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(id_, position, size, hitbox, *args, **kwargs)

    def on_player_collide(self, *args, **kwargs) -> None:
        player = kwargs.get("player", None)
        if player is None:
            raise AttributeError("Tile 'Spike' could not found player.")

        player.alive = False
