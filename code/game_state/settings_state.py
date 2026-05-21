import json
import pygame

from ui import UIConfig, Button
from .game_state import GameState


class SettingsState(GameState):
    GRAVITY: float = 0.55

    def __init__(self, game_state_manager, *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)
        self.show_hitboxes: bool = False
        self.pause_after_death: bool = False

        self.__show_hitboxes_btn: Button = Button(
            pygame.Rect((8, 8), UIConfig.CHECKBOX_SIZE),
            UIConfig.CHECKBOX_TEXTURE
        )

        self.__pause_on_death_btn: Button = Button(
            pygame.Rect((8, 8 + 8 + UIConfig.CHECKBOX_SIZE[1]), UIConfig.CHECKBOX_SIZE),
            UIConfig.CHECKBOX_TEXTURE
        )

        self.__load_settings()

    def on_state_exit(self, *args, **kwargs) -> None:
        self.__save_settings()

    def __load_settings(self) -> None:
        with open("../resources/data/settings.json", "r") as file:
            content: dict[str, bool] = json.load(file)
            self.show_hitboxes = content.get("show_hitboxes", False)
            self.pause_after_death = content.get("pause_after_death", False)

    def __save_settings(self) -> None:
        with open("../resources/data/settings.json", "w") as file:
            content: dict[str, bool] = {
                "show_hitboxes": self.show_hitboxes,
                "pause_after_death": self.pause_after_death
            }
            json.dump(content, file, indent=4)

    def update(self, *args, **kwargs) -> None:
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self._game_state_manager.change_state_to_previous()
            return

        if self.__show_hitboxes_btn.is_just_pressed():
            self.show_hitboxes = not self.show_hitboxes

        elif self.__pause_on_death_btn.is_just_pressed():
            self.pause_after_death = not self.pause_after_death

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.__show_hitboxes_btn.draw(surface)
        self.__show_hitboxes_btn.draw_text(surface, "Show hitboxes", UIConfig.fonts.get("jetbrains_20l"), "#ffffff",
                                           offset=[UIConfig.CHECKBOX_SIZE[0] + 8, -1])
        if self.show_hitboxes:
            surface.blit(UIConfig.CHECKBOX_ACTIVE_TEXTURE, self.__show_hitboxes_btn.rect.topleft)

        self.__pause_on_death_btn.draw(surface)
        self.__pause_on_death_btn.draw_text(surface, "Pause after death", UIConfig.fonts.get("jetbrains_20l"), "#ffffff",
                                            offset=[UIConfig.CHECKBOX_SIZE[0] + 8, -1])

        if self.pause_after_death:
            surface.blit(UIConfig.CHECKBOX_ACTIVE_TEXTURE, self.__pause_on_death_btn.rect.topleft)
