import pygame

from .tile import Tile


class YellowOrb(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.YELLOW_ORB, position, size, hitbox, *args, **kwargs)
        self.__jump_high: float = -10

    def on_player_collide(self, *args, **kwargs) -> None:
        player = kwargs.get("player")

        if pygame.key.get_just_pressed()[pygame.K_SPACE]:
            player.velocity.y = self.__jump_high * player.gravity_multiplier

class BlueOrb(Tile):
    def __init__(self, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(Tile.BLUE_ORB, position, size, hitbox, *args, **kwargs)

    def on_player_collide(self, *args, **kwargs) -> None:
        player = kwargs.get("player")

        if pygame.key.get_just_pressed()[pygame.K_SPACE]:
            player.gravity_multiplier *= -1
            player.velocity.y = 0
