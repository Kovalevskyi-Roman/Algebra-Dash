import pygame

from .game_state import GameState


class OriginalLevelsState(GameState):
    def __init__(self, game_state_manager, *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)
