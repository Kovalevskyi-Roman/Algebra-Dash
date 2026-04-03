import pygame


class GameState:
    def __init__(self, game_state_manager, *args, **kwargs) -> None:
        self.__game_state_manager = game_state_manager

    def update(self, *args, **kwargs) -> None:
        ...

    def on_state_enter(self, *args, **kwargs) -> None:
        ...

    def on_state_exit(self, *args, **kwargs) -> None:
        ...

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        ...
