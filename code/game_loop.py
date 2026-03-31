import pygame

from window import Window


class GameLoop:
    def __init__(self, window: Window) -> None:
        self.__window = window

    def __update(self) -> None:
        self.__window.tick()

    def __draw(self) -> None:
        self.__window.fill((0, 0, 0))
        self.__window.update()

    def run(self) -> None:
        while Window.running:
            Window.update_events()
            self.__update()
            self.__draw()

        pygame.quit()
