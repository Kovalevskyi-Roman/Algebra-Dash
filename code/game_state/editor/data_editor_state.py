import pygame

from game_state.game_state import GameState
from level import Level
from ui import Entry, Button, UIConfig
from window import Window


class DataEditorState(GameState):
    def __init__(self, game_state_manager, *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)

        self.level: tuple[str, dict[str, ...]] | None = None

        self.entry: Entry = Entry(
            pygame.Rect(Window.SIZE[0] / 2 - 210, 80, 420, 45),
            pygame.Surface((420, 45)),
            UIConfig.fonts.get("tahoma_26"),
            "#000000",
            max_text_length=28
        )
        self.entry.texture.fill("#7A7A7A")

        self.__editor_btn_size: pygame.Vector2 = pygame.Vector2(120, 120)
        self.__editor_btn: Button = Button(
            pygame.Rect(
                (Window.SIZE[0] / 2 - self.__editor_btn_size.x / 2, 320 - self.__editor_btn_size.y / 2),
                self.__editor_btn_size
            ),
            pygame.image.load("../resources/textures/ui/edit_button_round.png").convert_alpha()
        )
        self.__editor_btn.scale_texture_to_rect()

        self.__play_btn_size: pygame.Vector2 = pygame.Vector2(90, 90)
        self.__play_btn: Button = Button(
            pygame.Rect(
                (Window.SIZE[0] / 3 - self.__play_btn_size.x / 2, 320 - self.__play_btn_size.y / 2),
                self.__play_btn_size
            ),
            pygame.image.load("../resources/textures/ui/play_button_round.png").convert_alpha()
        )
        self.__play_btn.scale_texture_to_rect()

        self.__back_btn_size: pygame.Vector2 = pygame.Vector2(90, 90)
        self.__back_btn: Button = Button(
            pygame.Rect(
                (Window.SIZE[0] * (2 / 3) - self.__back_btn_size.x / 2, 320 - self.__back_btn_size.y / 2),
                self.__back_btn_size
            ),
            pygame.image.load("../resources/textures/ui/back_button.png").convert_alpha()
        )
        self.__back_btn.scale_texture_to_rect()

    def on_state_enter(self, *args, **kwargs) -> None:
        self.entry.set_text(self.level[1].get("level_name"))

    def on_state_exit(self, *args, **kwargs) -> None:
        Level.save_data(self.level[0], self.entry.get_text(), True)
        self.entry.active = False
        pygame.key.stop_text_input()

    def update(self, *args, **kwargs) -> None:
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            if self.entry.active:
                self.entry.active = False
                pygame.key.stop_text_input()
            else:
                self._game_state_manager.change_state(self._game_state_manager.CUSTOM_LEVELS_STATE)
                return

        self.entry.update()
        if self.entry.active:
            self.level[1]["level_name"] = self.entry.get_text()

        if self.__back_btn.is_pressed():
            self._game_state_manager.change_state(self._game_state_manager.CUSTOM_LEVELS_STATE)

        elif self.__editor_btn.is_pressed():
            tile_editor_state = self._game_state_manager.game_states.get(self._game_state_manager.TILE_EDITOR_STATE, None)
            if tile_editor_state is None:
                raise AttributeError("State 'TILE_EDITOR_STATE' not found.")

            tile_editor_state.level_path = self.level[0]
            self._game_state_manager.change_state(self._game_state_manager.TILE_EDITOR_STATE)

        elif self.__play_btn.is_pressed():
            play_state = self._game_state_manager.game_states.get(self._game_state_manager.PLAY_STATE, None)
            if play_state is None:
                raise AttributeError("State 'PLAY_STATE' not found.")

            play_state.level_path = self.level[0]
            self._game_state_manager.change_state(self._game_state_manager.PLAY_STATE)

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.entry.draw(surface)

        self.__editor_btn.draw(surface)
        self.__play_btn.draw(surface)
        self.__back_btn.draw(surface)
