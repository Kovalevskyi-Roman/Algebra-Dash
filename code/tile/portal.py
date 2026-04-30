import pygame

from .tile import Tile


class BluePortal(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.BLUE_PORTAL, position, size, hitbox, *args, **kwargs)

    def on_player_collide(self, *args, **kwargs) -> None:
        kwargs.get("player").gravity_multiplier = abs(kwargs.get("player").gravity_multiplier)


class YellowPortal(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.YELLOW_PORTAL, position, size, hitbox, *args, **kwargs)

    def on_player_collide(self, *args, **kwargs) -> None:
        kwargs.get("player").gravity_multiplier = -abs(kwargs.get("player").gravity_multiplier)


class CubePortal(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.CUBE_PORTAL, position, size, hitbox, *args, **kwargs)

    def on_player_collide(self, *args, **kwargs) -> None:
        kwargs.get("player").current_game_mode = kwargs.get("player").CUBE_MODE


class ShipPortal(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.SHIP_PORTAL, position, size, hitbox, *args, **kwargs)

    def on_player_collide(self, *args, **kwargs) -> None:
        kwargs.get("player").current_game_mode = kwargs.get("player").SHIP_MODE
