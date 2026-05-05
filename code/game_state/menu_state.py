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
            pygame.image.load("../resources/textures/ui/play_button.png").convert_alpha()
        )
        self.__play_btn.scale_texture_to_rect()

        self.__editor_btn_size: pygame.Vector2 = pygame.Vector2(90, 90)
        self.__editor_btn: Button = Button(
            pygame.Rect(
                (Window.SIZE[0] * (2 / 3) - self.__editor_btn_size.x / 2, Window.SIZE[1] / 2 - self.__editor_btn_size.y / 2),
                self.__editor_btn_size
            ),
            pygame.image.load("../resources/textures/ui/edit_button.png").convert_alpha()
        )
        self.__editor_btn.scale_texture_to_rect()

        self.__skin_shop_btn_size: pygame.Vector2 = pygame.Vector2(90, 90)
        self.__skin_shop_btn: Button = Button(
            pygame.Rect(
                (Window.SIZE[0] / 3 - self.__skin_shop_btn_size.x / 2, Window.SIZE[1] / 2 - self.__skin_shop_btn_size.y / 2),
                self.__skin_shop_btn_size
            ),
            pygame.image.load("../resources/textures/ui/skin_shop_button.png").convert_alpha()
        )
        self.__skin_shop_btn.scale_texture_to_rect()

    def update(self, *args, **kwargs) -> None:
        if self.__play_btn.is_pressed():
            self._game_state_manager.change_state(self._game_state_manager.ORIGINAL_LEVELS_STATE)

        elif self.__editor_btn.is_pressed():
            self._game_state_manager.change_state(self._game_state_manager.CUSTOM_LEVELS_STATE)

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.__play_btn.draw(surface)
        self.__editor_btn.draw(surface)
        self.__skin_shop_btn.draw(surface)
