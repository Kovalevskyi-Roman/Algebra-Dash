import pygame

from .game_state import GameState


class SettingsState(GameState):
    GRAVITY: float = 0.55

    def __init__(self, game_state_manager, *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)
        self.show_hitboxes: bool = True
