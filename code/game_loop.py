import pygame

from window import Window
from game_state import GameStateManager
from music_manager import MusicManager


class GameLoop:
    def __init__(self, window: Window, game_state_manager: GameStateManager) -> None:
        self.__window = window
        self.__game_state_manager = game_state_manager

    def __update(self) -> None:
        self.__window.tick()
        self.__game_state_manager.update()

    def __draw(self) -> None:
        self.__window.fill("#16191D")
        MusicManager.update()
        self.__game_state_manager.draw(self.__window.surface)
        self.__window.update()

    def run(self) -> None:
        while Window.running:
            Window.update_events()
            self.__update()
            self.__draw()

        self.__game_state_manager.game_states.get(GameStateManager.SETTINGS_STATE).save_settings()
        pygame.quit()
