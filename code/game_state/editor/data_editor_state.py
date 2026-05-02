import pygame

from game_state.game_state import GameState
from level import Level
from ui import Entry, UIConfig
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
        self.entry.texture.fill("#9c9c9c")

    def on_state_enter(self, *args, **kwargs) -> None:
        self.entry.set_text(self.level[1].get("level_name"))

    def on_state_exit(self, *args, **kwargs) -> None:
        Level.save_data(self.level[0], self.entry.get_text(), True)
        self.level = None
        self.entry.set_text("")
        self.entry.active = False
        pygame.key.stop_text_input()

        Level.load_levels()

    def update(self, *args, **kwargs) -> None:
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            if self.entry.active:
                self.entry.active = False
                pygame.key.stop_text_input()
            else:
                self._game_state_manager.change_state_to_previous()
                return

        self.entry.update()

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.entry.draw(surface)
