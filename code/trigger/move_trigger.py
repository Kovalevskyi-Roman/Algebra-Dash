import pygame

from tile import Tile
from window import Window
from .trigger import Trigger


class MoveTrigger(Trigger):
    def __init__(self, json_trigger: dict[str, ...]) -> None:
        super().__init__(json_trigger)
        self.__iterations: int = round(self.work_time / Window.DELTA)
        if self.__iterations <= 0:
            self.__iterations = 1

        self.__move_by: pygame.Vector2 = pygame.Vector2(self.data.get("move_by", 0)) / self.__iterations

    def update(self, *args, **kwargs) -> None:
        tile: Tile | None = kwargs.get("tile", None)
        if tile is None:
            return
        
        tile.rect.topleft += self.__move_by
