import pygame

from .game_state import GameState
from .menu_state import MenuState
from .play_state import PlayState
from .level_selection_state import LevelSelectionState


class GameStateManager:
    MENU_STATE: type[GameState] = MenuState
    PLAY_STATE: type[GameState] = PlayState
    LEVEL_SELECTION_STATE: type[GameState] = LevelSelectionState

    def __init__(self) -> None:
        self.game_states: dict[type[GameState], GameState] = {
            self.MENU_STATE: MenuState(self),
            self.PLAY_STATE: PlayState(self),
            self.LEVEL_SELECTION_STATE: LevelSelectionState(self)
        }

        self.current_state_type: type[GameState] = self.MENU_STATE
        self.__current_state: GameState | None = None

        self.change_state(self.MENU_STATE)

    def change_state(self, new_state: type[GameState]) -> None:
        if self.__current_state is not None:
            self.__current_state.on_state_exit()

        self.current_state_type = new_state
        self.__current_state = self.game_states.get(self.current_state_type, None)
        if self.__current_state is not None:
            self.__current_state.on_state_enter()

    def update_state(self) -> None:
        self.__current_state.update()

    def draw_state(self, surface: pygame.Surface) -> None:
        self.__current_state.draw(surface)
