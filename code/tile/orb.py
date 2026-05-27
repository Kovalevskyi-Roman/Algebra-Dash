import pygame

from .tile import Tile


class YellowOrb(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.YELLOW_ORB, position, size, hitbox, *args, **kwargs)
        self.__jump_high: float = -10

    def on_player_collide(self, *args, **kwargs) -> None:
        player = kwargs.get("player")

        if player.just_jump_action:
            player.velocity.y = self.__jump_high * player.gravity_multiplier


class PurpleOrb(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.PURPLE_ORB, position, size, hitbox, *args, **kwargs)
        self.__jump_high: float = -6.75

    def on_player_collide(self, *args, **kwargs) -> None:
        player = kwargs.get("player")

        if player.just_jump_action:
            player.velocity.y = self.__jump_high * player.gravity_multiplier


class OrangeOrb(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.ORANGE_ORB, position, size, hitbox, *args, **kwargs)
        self.__jump_high: float = -14

    def on_player_collide(self, *args, **kwargs) -> None:
        player = kwargs.get("player")

        if player.just_jump_action:
            player.velocity.y = self.__jump_high * player.gravity_multiplier


class BlackOrb(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.BLACK_ORB, position, size, hitbox, *args, **kwargs)
        self.__jump_high: float = 14

    def on_player_collide(self, *args, **kwargs) -> None:
        player = kwargs.get("player")

        if player.just_jump_action:
            player.velocity.y = self.__jump_high * player.gravity_multiplier


class BlueOrb(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.BLUE_ORB, position, size, hitbox, *args, **kwargs)
        self.one_off: bool = True
        self.__was_pressed: bool = False

    def on_player_collide(self, *args, **kwargs) -> None:
        if self.one_off and self.__was_pressed:
            return

        player = kwargs.get("player")

        if player.just_jump_action:
            player.gravity_multiplier *= -1
            player.velocity.y = 0
            self.__was_pressed = True

    def reset(self) -> None:
        self.__was_pressed = False


class GreenOrb(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.GREEN_ORB, position, size, hitbox, *args, **kwargs)
        self.__jump_high: float = -10

    def on_player_collide(self, *args, **kwargs) -> None:
        player = kwargs.get("player")

        if player.just_jump_action:
            player.gravity_multiplier *= -1
            player.velocity.y = self.__jump_high * player.gravity_multiplier
