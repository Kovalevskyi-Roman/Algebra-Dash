import pygame

from camera import Camera
from collider import Collider
from window import Window
from player import Player
from tile import Tile, TileManager


class GameLoop:
    def __init__(self, window: Window) -> None:
        self.__window = window
        self.player: Player = Player()
        self.tiles: list[Tile] = list()
        self.tiles.append(TileManager.create_tile(TileManager.TILE, [32, 0]))
        self.tiles.append(TileManager.create_tile(TileManager.TILE, [0, 32]))
        self.tiles.append(TileManager.create_tile(TileManager.TILE, [0, -64]))
        self.camera: Camera = Camera(self.player)
        self.collider: Collider = Collider(self.player, self.tiles)

    def __update(self) -> None:
        self.__window.tick()
        self.player.update()
        self.camera.update()
        for tile in self.tiles:
            tile.update()

        self.collider.update_collision(self.camera.offset)

    def __draw(self) -> None:
        self.__window.fill((0, 0, 0))
        self.player.draw(self.__window.surface, self.camera.offset)
        for tile in self.tiles:
            TileManager.draw_tile(tile, self.__window.surface, self.camera.offset)

        self.__window.update()

    def run(self) -> None:
        while Window.running:
            Window.update_events()
            self.__update()
            self.__draw()

        pygame.quit()
