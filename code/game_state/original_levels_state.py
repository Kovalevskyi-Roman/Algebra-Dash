import pygame

from ui import Button, UIConfig, ProgressBar
from window import Window
from .game_state import GameState
from level import Level


class OriginalLevelsState(GameState):
    def __init__(self, game_state_manager, *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)

        self.__levels: tuple[tuple[str, dict[str, ...]], ...] = tuple()
        self.__selected_level: int = 0
        self.__level_btn: Button = Button(
            pygame.Rect(Window.SIZE[0] / 2 - 340, 100, 680, 140),
            pygame.Surface((680, 140)),
            font=UIConfig.fonts.get("jetbrains_40m"), f_color="#ffffff"
        )
        self.__level_btn.texture.fill("#6a6a6a")

        self.__progress: ProgressBar = ProgressBar(pygame.Rect(0, 300, 650, 25), 0, 100, border_radius=8)

    def __update_ui(self) -> None:
        self.__level_btn.text = self.__levels[self.__selected_level][1].get("level_name")
        self.__level_btn.render_text()
        self.__progress.set_progress(self.__levels[self.__selected_level][1].get("max_progress", 0))

    def on_state_enter(self, *args, **kwargs) -> None:
        self.__levels: tuple[tuple[str, dict[str, ...]], ...] = tuple(
            filter(lambda level: level[1].get("is_original", False), Level.levels.items())
        )
        if self.__selected_level >= len(self.__levels):
            self.__selected_level = 0

        self.__update_ui()

    def update(self, *args, **kwargs) -> None:
        keys_just_pressed = pygame.key.get_just_pressed()

        if keys_just_pressed[pygame.K_ESCAPE]:
            self._game_state_manager.change_state(self._game_state_manager.MENU_STATE)
            return

        if keys_just_pressed[pygame.K_LEFT]:
            self.__selected_level -= 1
            if self.__selected_level < 0:
                self.__selected_level = len(self.__levels) - 1

            self.__update_ui()

        elif keys_just_pressed[pygame.K_RIGHT]:
            self.__selected_level += 1
            if self.__selected_level >= len(self.__levels):
                self.__selected_level = 0

            self.__update_ui()

        if self.__level_btn.is_just_pressed() and self.__levels:
            play_state = self._game_state_manager.game_states.get(self._game_state_manager.PLAY_STATE, None)
            if play_state is None:
                raise AttributeError("State 'PLAY_STATE' not found")

            play_state.level_path = self.__levels[self.__selected_level][0]
            self._game_state_manager.change_state(self._game_state_manager.PLAY_STATE)

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        if not self.__levels:
            return

        selected_level_data = self.__levels[self.__selected_level][1]
        self.__level_btn.draw(surface)
        self.__level_btn.draw_text(surface)
        self.__progress.draw_centered(surface, True, False)
        self.__progress.draw_text(surface, f"{selected_level_data.get("max_progress", 0)}%",
                                  UIConfig.fonts.get("jetbrains_20l"), "#ffffff", centered_x=True)
