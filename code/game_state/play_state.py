import pygame

from level import Level
from .game_state import GameState
from camera import Camera
from player import Player


class PlayState(GameState):
    def __init__(self, game_state_manager, *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)

        self.__player: Player | None = None
        self.__camera: Camera | None = None
        self.__level: Level | None = None
        self.level_path: str = ""

    def on_state_enter(self, *args, **kwargs) -> None:
        self.__player = Player()
        self.__camera = Camera(self.__player)
        self.__level = Level()
        self.__level.load(self.level_path, self.__player)

    def on_state_exit(self, *args, **kwargs) -> None:
        self.__player = None
        self.__camera = None
        self.__level = None
        self.level_path = ""

    def update(self, *args, **kwargs) -> None:
        self.__player.update()
        self.__camera.update()
        self.__level.update(self.__camera.offset)

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.__player.draw(surface, self.__camera.offset)
        self.__level.draw(surface, self.__camera.offset)
