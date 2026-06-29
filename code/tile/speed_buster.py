import pygame

from .tile import Tile


class SpeedBuster(Tile):
    def __init__(self, id_: str, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(id_, position, size, hitbox, *args, **kwargs)
        self.speed: float = Tile.TILE_MANAGER.TILE_DATA.get(self.id, {}).get("properties", {}).get("speed", 0)

    def on_player_collide(self, *args, **kwargs) -> None:
        kwargs.get("player").move_speed = self.speed
