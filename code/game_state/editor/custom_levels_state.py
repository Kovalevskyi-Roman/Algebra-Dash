import pygame

from game_state.game_state import GameState


class CustomLevelsState(GameState):
    def __init__(self, game_state_manager, *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)
