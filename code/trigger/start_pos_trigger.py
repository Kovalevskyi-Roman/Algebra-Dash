import pygame

from .trigger import Trigger


class StartPosTrigger(Trigger):
    def __init__(self, json_trigger: dict[str, ...]) -> None:
        super().__init__(json_trigger)

    # TODO: player speed selection
    # TODO: player game mode selection
    # TODO: player gravity selection
