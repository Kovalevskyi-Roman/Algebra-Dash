import pygame

from window import Window
from .game_state import GameState
from ui import Button


class MenuState(GameState):
    def __init__(self, game_state_manager, *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)

        self.__title: pygame.Surface = pygame.image.load("../resources/textures/ui/title.png").convert_alpha()
        self.__title = pygame.transform.scale(self.__title, (self.__title.width * 2, self.__title.height * 1.6))

        self.__play_btn_size: pygame.Vector2 = pygame.Vector2(140, 140)
        self.__play_btn: Button = Button(
            pygame.Rect(
                (Window.SIZE[0] / 2 - self.__play_btn_size.x / 2, Window.SIZE[1] / 2 - self.__play_btn_size.y / 2),
                self.__play_btn_size
            ),
            pygame.image.load("../resources/textures/ui/play_button.png").convert_alpha()
        )
        self.__play_btn.scale_texture_to_rect()

        self.__editor_btn_size: pygame.Vector2 = pygame.Vector2(110, 110)
        self.__editor_btn: Button = Button(
            pygame.Rect(
                (Window.SIZE[0] * (2.25 / 3.25) - self.__editor_btn_size.x / 2, Window.SIZE[1] / 2 - self.__editor_btn_size.y / 2),
                self.__editor_btn_size
            ),
            pygame.image.load("../resources/textures/ui/edit_button.png").convert_alpha()
        )
        self.__editor_btn.scale_texture_to_rect()

        self.__icon_editor_btn_size: pygame.Vector2 = pygame.Vector2(110, 110)
        self.__icon_editor_btn: Button = Button(
            pygame.Rect(
                (Window.SIZE[0] / 3.25 - self.__icon_editor_btn_size.x / 2, Window.SIZE[1] / 2 - self.__icon_editor_btn_size.y / 2),
                self.__icon_editor_btn_size
            ),
            pygame.image.load("../resources/textures/ui/skin_shop_button.png").convert_alpha()
        )
        self.__icon_editor_btn.scale_texture_to_rect()

        self.__settings_btn: Button = Button(
            pygame.Rect(Window.SIZE[0] - 43, Window.SIZE[1] - 43, 35, 35),
            pygame.Surface((35, 35))
        )
        self.__settings_btn.texture.fill("#646464")
        self.__settings_btn.texture.blit(
            pygame.transform.scale(
                pygame.image.load("../resources/textures/ui/settings_icon.png").convert_alpha(), (35, 35)
            ),
            [0, 0]
        )

    def update(self, *args, **kwargs) -> None:
        if self.__play_btn.is_just_pressed():
            self._game_state_manager.change_state(self._game_state_manager.ORIGINAL_LEVELS_STATE)

        elif self.__editor_btn.is_just_pressed():
            self._game_state_manager.change_state(self._game_state_manager.CUSTOM_LEVELS_STATE)

        elif self.__icon_editor_btn.is_just_pressed():
            self._game_state_manager.change_state(self._game_state_manager.ICON_EDITOR_STATE)

        elif self.__settings_btn.is_just_pressed():
            self._game_state_manager.change_state(self._game_state_manager.SETTINGS_STATE)

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        surface.blit(self.__title, [surface.width / 2 - self.__title.width / 2, -30])
        self.__play_btn.draw(surface)
        self.__editor_btn.draw(surface)
        self.__icon_editor_btn.draw(surface)
        self.__settings_btn.draw(surface)
