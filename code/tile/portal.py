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
        kwargs.get("level").ground_tile.rect.y = Tile.SIZE
        kwargs.get("level").ceil_tile.rect.y = -Tile.SIZE * 64


class ShipPortal(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.SHIP_PORTAL, position, size, hitbox, *args, **kwargs)
        self.ground_level = 5
        self.ceil_level = 6

    def on_player_collide(self, *args, **kwargs) -> None:
        kwargs.get("player").current_game_mode = kwargs.get("player").SHIP_MODE

        level = kwargs.get("level")
        level.ground_tile.rect.y = self.rect.centery // Tile.SIZE * Tile.SIZE + Tile.SIZE * self.ground_level
        level.ceil_tile.rect.y = self.rect.centery // Tile.SIZE * Tile.SIZE - Tile.SIZE * (self.ceil_level + 1)


class UfoPortal(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.UFO_PORTAL, position, size, hitbox, *args, **kwargs)
        self.ground_level = 5
        self.ceil_level = 6

    def on_player_collide(self, *args, **kwargs) -> None:
        kwargs.get("player").current_game_mode = kwargs.get("player").UFO_MODE

        level = kwargs.get("level")
        level.ground_tile.rect.y = self.rect.centery // Tile.SIZE * Tile.SIZE + Tile.SIZE * self.ground_level
        level.ceil_tile.rect.y = self.rect.centery // Tile.SIZE * Tile.SIZE - Tile.SIZE * (self.ceil_level + 1)


class BallPortal(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.BALL_PORTAL, position, size, hitbox, *args, **kwargs)
        self.ground_level = 5
        self.ceil_level = 6

    def on_player_collide(self, *args, **kwargs) -> None:
        kwargs.get("player").current_game_mode = kwargs.get("player").BALL_MODE

        level = kwargs.get("level")
        level.ground_tile.rect.y = self.rect.centery // Tile.SIZE * Tile.SIZE + Tile.SIZE * self.ground_level
        level.ceil_tile.rect.y = self.rect.centery // Tile.SIZE * Tile.SIZE - Tile.SIZE * (self.ceil_level + 1)


class WavePortal(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.WAVE_PORTAL, position, size, hitbox, *args, **kwargs)
        self.ground_level = 5
        self.ceil_level = 6

    def on_player_collide(self, *args, **kwargs) -> None:
        kwargs.get("player").current_game_mode = kwargs.get("player").WAVE_MODE

        level = kwargs.get("level")
        level.ground_tile.rect.y = self.rect.centery // Tile.SIZE * Tile.SIZE + Tile.SIZE * self.ground_level
        level.ceil_tile.rect.y = self.rect.centery // Tile.SIZE * Tile.SIZE - Tile.SIZE * (self.ceil_level + 1)
