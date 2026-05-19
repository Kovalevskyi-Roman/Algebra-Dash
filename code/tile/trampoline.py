import pygame

from .tile import Tile


class YellowTrampoline(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.YELLOW_TRAMPOLINE, position, size, hitbox, *args, **kwargs)
        self.__jump_high: float = -9

    def on_player_collide(self, *args, **kwargs) -> None:
        kwargs.get("player").velocity.y = self.__jump_high * kwargs.get("player").gravity_multiplier


class PurpleTrampoline(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.PURPLE_TRAMPOLINE, position, size, hitbox, *args, **kwargs)
        self.__jump_high: float = -6.75

    def on_player_collide(self, *args, **kwargs) -> None:
        kwargs.get("player").velocity.y = self.__jump_high * kwargs.get("player").gravity_multiplier


class OrangeTrampoline(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.ORANGE_TRAMPOLINE, position, size, hitbox, *args, **kwargs)
        self.__jump_high: float = -13

    def on_player_collide(self, *args, **kwargs) -> None:
        kwargs.get("player").velocity.y = self.__jump_high * kwargs.get("player").gravity_multiplier


class BlueTrampoline(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.BLUE_TRAMPOLINE, position, size, hitbox, *args, **kwargs)
        self.__was_collide: bool = False

    def on_player_collide(self, *args, **kwargs) -> None:
        if self.__was_collide:
            return

        self.__was_collide = True
        kwargs.get("player").gravity_multiplier *= -1
