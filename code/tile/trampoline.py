import pygame

from .tile import Tile


class Trampoline(Tile):
    def __init__(self, id_: str, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(id_, position, size, hitbox, *args, **kwargs)
        self.__jump_high: float = Tile.TILE_MANAGER.TILE_DATA.get(self.id, {}).get("properties", {}).get("jump_height", 0)
        self.__was_used: bool = False

    def on_player_collide(self, *args, **kwargs) -> None:
        if self.__was_used:
            return

        player = kwargs.get("player")
        player.velocity.y = self.__jump_high * player.gravity_multiplier

        if Tile.TILE_MANAGER.TILE_DATA.get(self.id, {}).get("properties", {}).get("flip_gravity", False):
            player.gravity_multiplier *= -1

        self.__was_used = True

    def reset(self) -> None:
        super().reset()
        self.__was_used = False
