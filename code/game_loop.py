import pygame

from window import Window
from player import Player
from tile import Tile, TileManager


class GameLoop:
    def __init__(self, window: Window) -> None:
        self.__window = window
        self.player: Player = Player()
        self.tiles: list[Tile] = list()
        self.tiles.append(TileManager.create_tile(TileManager.TILE, [0, 0]))
        self.tiles.append(TileManager.create_tile(TileManager.TILE, [32, 64]))

    def __update(self) -> None:
        self.__window.tick()
        self.player.update()
        for tile in self.tiles:
            tile.update()

    def __draw(self) -> None:
        self.__window.fill((0, 0, 0))
        self.player.draw(self.__window.surface)
        for tile in self.tiles:
            TileManager.draw_tile(tile, self.__window.surface)

        self.__window.update()

    def run(self) -> None:
        while Window.running:
            Window.update_events()
            self.__update()
            self.__draw()

        pygame.quit()
