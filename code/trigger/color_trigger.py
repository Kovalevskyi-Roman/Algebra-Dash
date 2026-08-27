import pygame

from math import ceil
from .trigger import Trigger
from window import Window


class ColorTrigger(Trigger):
    def __init__(self, json_trigger: dict[str, ...]) -> None:
        super().__init__(json_trigger)
        self.__iterations: int = round(self.work_time / Window.DELTA)
        if self.__iterations <= 0:
            self.__iterations = 1

        self.__color = pygame.Color(self.data.get("color", "#000000"))

    def update(self, *args, **kwargs) -> None:
        level = kwargs.get("level", None)
        if level is None:
            raise AttributeError("Cannot update color trigger because level is None")

        if self.group_id == -2:
            level.bg_color = pygame.Color(level.bg_color).lerp(self.__color, 1 / self.__iterations).hex

        elif self.group_id == -1:
            level.ground_color = pygame.Color(level.ground_color).lerp(self.__color, 1 / self.__iterations).hex

        else:
            tile = kwargs.get("tile", None)
            if tile is None:
                return

            tile.color = pygame.Color(tile.color).lerp(self.__color, 1 / self.__iterations).hex

        self.__iterations: int = round(self.remaining_time / Window.DELTA)
        if self.__iterations <= 0:
            self.__iterations = 1
