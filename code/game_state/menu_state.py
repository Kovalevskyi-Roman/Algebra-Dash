import pygame

from window import Window
from .game_state import GameState
from ui import Button


class MenuState(GameState):
    def __init__(self, game_state_manager, *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)

        self.__play_btn_size: pygame.Vector2 = pygame.Vector2(120, 120)
        self.__play_btn: Button = Button(
            pygame.Rect(
                (Window.SIZE[0] / 2 - self.__play_btn_size.x / 2, Window.SIZE[1] / 2 - self.__play_btn_size.y / 2),
                self.__play_btn_size
            ),
            pygame.Surface(self.__play_btn_size)
        )
        self.__play_btn.texture.fill("#ffffff")

        self.__editor_btn_size: pygame.Vector2 = pygame.Vector2(90, 90)
        self.__editor_btn: Button = Button(
            pygame.Rect(
                (Window.SIZE[0] / 2 + self.__editor_btn_size.x * 2.4, Window.SIZE[1] / 2 - self.__editor_btn_size.y / 2),
                self.__editor_btn_size
            ),
            pygame.Surface(self.__editor_btn_size)
        )
        self.__editor_btn.texture.fill("#ffffff")

        self.__btn_size: pygame.Vector2 = pygame.Vector2(90, 90)
        self.__btn: Button = Button(
            pygame.Rect(
                (Window.SIZE[0] / 2 - self.__btn_size.x * 3.4, Window.SIZE[1] / 2 - self.__btn_size.y / 2),
                self.__btn_size
            ),
            pygame.Surface(self.__btn_size)
        )
        self.__btn.texture.fill("#ffffff")

    def update(self, *args, **kwargs) -> None:
        if self.__play_btn.is_pressed():
            self._game_state_manager.change_state(self._game_state_manager.ORIGINAL_LEVELS_STATE)

        elif self.__editor_btn.is_pressed():
            self._game_state_manager.change_state(self._game_state_manager.CUSTOM_LEVELS_STATE)

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.__play_btn.draw(surface)
        self.__editor_btn.draw(surface)
        self.__btn.draw(surface)
