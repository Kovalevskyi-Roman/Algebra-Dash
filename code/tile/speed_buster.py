import pygame

from .tile import Tile


class X1SpeedBuster(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.X1_SPEED_BUSTER, position, size, hitbox, *args, **kwargs)
        self.speed: float = 3

    def on_player_collide(self, *args, **kwargs) -> None:
        kwargs.get("player").move_speed = self.speed


class X2SpeedBuster(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.X2_SPEED_BUSTER, position, size, hitbox, *args, **kwargs)
        self.speed = 4.25

    def on_player_collide(self, *args, **kwargs) -> None:
        kwargs.get("player").move_speed = self.speed


class X3SpeedBuster(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.X3_SPEED_BUSTER, position, size, hitbox, *args, **kwargs)
        self.speed: float = 5.5

    def on_player_collide(self, *args, **kwargs) -> None:
        kwargs.get("player").move_speed = self.speed


class X4SpeedBuster(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.X4_SPEED_BUSTER, position, size, hitbox, *args, **kwargs)
        self.speed: float = 6.71

    def on_player_collide(self, *args, **kwargs) -> None:
        kwargs.get("player").move_speed = self.speed
