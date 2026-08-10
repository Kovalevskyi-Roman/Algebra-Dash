import pygame

from window import Window
from tile.tile import Tile


class Trigger:
    def __init__(self, json_trigger: dict[str, ...]) -> None:
        self.__id: str = ""
        self.position: pygame.Vector2 | None = None
        self.group_id: int = -1
        self.work_time: float = 0
        self.data: dict[str, ...] | None = None

        self.from_json(json_trigger)

        self.remaining_time: float = self.work_time

    def from_json(self, json_trigger: dict[str, ...]) -> None:
        self.__id = json_trigger.get("id")
        self.position = pygame.Vector2(json_trigger.get("xy"))
        self.group_id = json_trigger.get("gId")
        self.work_time = json_trigger.get("wT")
        self.data = json_trigger.get("data")

    def to_json(self) -> dict[str, ...]:
        return {
            "id": self.__id,
            "xy": [self.position.x, self.position.y],
            "gId": self.group_id,
            "wT": self.work_time,
            "data": self.data,
        }

    def update(self, *args, **kwargs) -> None:
        ...

    def reset(self) -> None:
        self.remaining_time = self.work_time
