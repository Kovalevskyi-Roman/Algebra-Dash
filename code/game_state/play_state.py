import pygame

from level import Level
from tile import TileManager
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

        self.__draw_hitboxes: bool = True

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
        if pygame.key.get_just_released()[pygame.K_ESCAPE]:
            self._game_state_manager.change_state(self._game_state_manager.MENU_STATE)
            return

        self.__player.update()
        self.__camera.update()
        self.__level.update(self.__camera.offset)

        if not self.__player.alive:
            self.on_state_enter()

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        surface.fill(self.__level.bg_color)
        self.__player.draw(surface, self.__camera.offset)
        self.__level.draw(surface, self.__camera.offset)

        if self.__draw_hitboxes:
            for tile in self.__level.tiles:
                TileManager.draw_tile_hitbox(tile, surface, self.__camera.offset)
