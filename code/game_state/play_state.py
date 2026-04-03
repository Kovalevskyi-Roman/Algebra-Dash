import pygame

from .game_state import GameState
from camera import Camera
from collider import Collider
from window import Window
from player import Player
from tile import Tile, TileManager


class PlayState(GameState):
    def __init__(self, game_state_manager, *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)

        self.player: Player = Player()
        self.tiles: list[Tile] = list()
        self.tiles.append(TileManager.create_tile(Tile.TILE, [32, 0]))
        self.tiles.append(TileManager.create_tile(Tile.FOLLOW_TILE, [0, 32]))
        self.tiles.append(TileManager.create_tile(Tile.TILE, [0, -64]))
        self.camera: Camera = Camera(self.player)
        self.collider: Collider = Collider(self.player, self.tiles)

    def update(self, *args, **kwargs) -> None:
        self.player.update()
        self.camera.update()
        for tile in self.tiles:
            tile.update(player=self.player)

        self.collider.update_collision(self.camera.offset)

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.player.draw(surface, self.camera.offset)
        for tile in self.tiles:
            TileManager.draw_tile(tile, surface, self.camera.offset)
