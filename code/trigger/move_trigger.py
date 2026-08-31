import pygame

from tile import Tile
from window import Window
from .trigger import Trigger


class MoveTrigger(Trigger):
    def __init__(self, json_trigger: dict[str, ...]) -> None:
        super().__init__(json_trigger)

        self.__move_by: pygame.Vector2 = pygame.Vector2(self.data.get("move_by", 0)) / self.iterations

    def update(self, *args, **kwargs) -> None:
        tile: Tile | None = kwargs.get("tile", None)
        if tile is None:
            raise AttributeError("Cannot update move trigger because tile is None")
        
        tile.rect.topleft += self.__move_by
