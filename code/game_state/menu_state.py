import pygame

from random import choice, randint
from window import Window
from .game_state import GameState
from ui import Button, UIConfig


class MenuState(GameState):
    __LABELS: tuple[str, ...] = (
        "2+2=4",
        "y=kx+b",
        "a(x+y)=ax+ay",
        "1000-7=993",
        "g(x)=f(x)",
        "3x>10",
        "(fg)'=f'g+fg'",
        "(f+g)'=f'+g'"
    )

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

        self.__labels: list[dict[str, pygame.Surface | pygame.Vector2 | int]] = list()
        for _ in range(24):
            self.__labels.append(self.__create_label())

    def __create_label(self) -> dict[str, pygame.Surface | pygame.Vector2 | int]:
        label = UIConfig.create_label(
            choice(list(UIConfig.fonts.keys())), choice(self.__LABELS), f_color="#" + choice(("6a", "9a", "b1")) * 3
        )
        label = pygame.transform.rotate(label, randint(-45, 45))

        position = pygame.Vector2(randint(-50, Window.SIZE[0]), randint(0, Window.SIZE[1] - 60))
        speed = randint(4, 8) / 10

        return {
            "label": label,
            "position": position,
            "speed": speed
        }

    def update(self, *args, **kwargs) -> None:
        if self.__play_btn.is_just_pressed():
            self._game_state_manager.change_state(self._game_state_manager.ORIGINAL_LEVELS_STATE)

        elif self.__editor_btn.is_just_pressed():
            self._game_state_manager.change_state(self._game_state_manager.CUSTOM_LEVELS_STATE)

        elif self.__icon_editor_btn.is_just_pressed():
            self._game_state_manager.change_state(self._game_state_manager.ICON_EDITOR_STATE)

        elif self.__settings_btn.is_just_pressed():
            self._game_state_manager.change_state(self._game_state_manager.SETTINGS_STATE)

        active_labels = list()
        for label in self.__labels:
            label.get("position").y += label.get("speed")
            if label.get("position").y < Window.SIZE[1]:
                active_labels.append(label)
            else:
                active_labels.append(self.__create_label())
                active_labels[-1].get("position").y = -active_labels[-1].get("label").height

        self.__labels = active_labels

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:

        for label in self.__labels:
            surface.blit(label.get("label"), label.get("position"))

        surface.blit(self.__title, [surface.width / 2 - self.__title.width / 2, -30])
        self.__play_btn.draw(surface)
        self.__editor_btn.draw(surface)
        self.__icon_editor_btn.draw(surface)
        self.__settings_btn.draw(surface)
