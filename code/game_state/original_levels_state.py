import pygame

from ui import Button, UIConfig
from window import Window
from .game_state import GameState
from level import Level


class OriginalLevelsState(GameState):
    def __init__(self, game_state_manager, *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)

        self.levels: tuple[tuple[str, dict[str, ...]], ...] = tuple(
            filter(lambda level: level[1].get("is_original", False), Level.levels.items())
        )
        self.selected_level: int = 0
        self.__level_btn: Button = Button(
            pygame.Rect(Window.SIZE[0] / 2 - 200, Window.SIZE[1] / 2 - 120, 400, 240),
            pygame.Surface((400, 240))
        )
        self.__level_btn.texture.fill("#ffffff")

    def update(self, *args, **kwargs) -> None:
        keys_just_pressed = pygame.key.get_just_pressed()

        if keys_just_pressed[pygame.K_ESCAPE]:
            self._game_state_manager.change_state(self._game_state_manager.MENU_STATE)
            return

        if keys_just_pressed[pygame.K_LEFT]:
            self.selected_level -= 1
            if self.selected_level < 0:
                self.selected_level = len(self.levels) - 1

        elif keys_just_pressed[pygame.K_RIGHT]:
            self.selected_level += 1
            if self.selected_level >= len(self.levels):
                self.selected_level = 0

        if self.__level_btn.is_just_pressed():
            play_state = self._game_state_manager.game_states.get(self._game_state_manager.PLAY_STATE, None)
            if play_state is None:
                print("State 'PLAY_STATE' not found. Unable to play level.")
                return

            play_state.level_name = self.levels[self.selected_level][1].get("level_name")
            self._game_state_manager.change_state(self._game_state_manager.PLAY_STATE)

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.__level_btn.draw(surface)
        self.__level_btn.draw_text(
            surface,
            self.levels[self.selected_level][1].get("level_name"),
            UIConfig.fonts.get("tahoma_20"),
            "#000000"
        )
