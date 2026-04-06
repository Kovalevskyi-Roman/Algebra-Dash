import pygame

from level import Level
from .game_state import GameState
from camera import Camera
from player import Player


class PlayState(GameState):
    def __init__(self, game_state_manager, *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)

        self.player: Player | None = None
        self.camera: Camera | None = None
        self.level_name: str = ""
        self.level: Level | None = None

    def on_state_enter(self, *args, **kwargs) -> None:
        self.player = Player()
        self.camera = Camera(self.player)
        self.level = Level()
        self.level.load(Level.get_path_from_name(self.level_name), self.player)

    def update(self, *args, **kwargs) -> None:
        self.player.update()
        self.camera.update()
        self.level.update(self.camera.offset)

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.player.draw(surface, self.camera.offset)
        self.level.draw(surface, self.camera.offset)
