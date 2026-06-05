import json
import pygame

from ui import UIConfig, Button, Slider
from window import Window
from .game_state import GameState


class SettingsState(GameState):
    GRAVITY: float = 0.55

    def __init__(self, game_state_manager, *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)
        self.show_hitboxes: bool = False
        self.pause_after_death: bool = False
        self.is_player_immortal: bool = False
        self.platformer_mode: bool = False

        self.player_first_color: str = ""
        self.player_second_color: str = ""
        self.player_icons: dict[str, int] = dict()

        self.__show_hitboxes_btn: Button = Button(
            pygame.Rect((8, 8), UIConfig.CHECKBOX_SIZE),
            UIConfig.CHECKBOX_TEXTURE
        )

        self.__pause_on_death_btn: Button = Button(
            pygame.Rect((8, 8 * 2 + UIConfig.CHECKBOX_SIZE[1]), UIConfig.CHECKBOX_SIZE),
            UIConfig.CHECKBOX_TEXTURE
        )

        self.__is_player_immortal_btn: Button = Button(
            pygame.Rect((8, 8 * 3 + UIConfig.CHECKBOX_SIZE[1] * 2), UIConfig.CHECKBOX_SIZE),
            UIConfig.CHECKBOX_TEXTURE
        )

        self.__platformer_mode_btn: Button = Button(
            pygame.Rect((8, 8 * 4 + UIConfig.CHECKBOX_SIZE[1] * 3), UIConfig.CHECKBOX_SIZE),
            UIConfig.CHECKBOX_TEXTURE
        )

        self.__music_volume_lbl = UIConfig.fonts.get("jetbrains_20l").render("Music volume", True, "#ffffff")
        self.music_volume_slider: Slider = Slider(
            pygame.Vector2(Window.SIZE[0] / 2, self.__music_volume_lbl.height + 8), Window.SIZE[0] // 2 - 50,
            0, 100.5
        )

        self.__load_settings()

    def on_state_exit(self, *args, **kwargs) -> None:
        pygame.mixer.music.set_volume(round(self.music_volume_slider.value) / 100)
        self.save_settings()

    def __load_settings(self) -> None:
        with open("../resources/data/settings.json", "r") as file:
            content: dict[str, bool | dict[str, int] | int] = json.load(file)

            self.show_hitboxes = content.get("show_hitboxes", False)
            self.pause_after_death = content.get("pause_after_death", False)
            self.is_player_immortal = content.get("is_player_immortal", False)
            self.platformer_mode = content.get("platformer_mode", False)

            self.player_first_color = content.get("player_first_color", "#ffdd00")
            self.player_second_color = content.get("player_second_color", "#0000ff")
            self.player_icons = content.get("player_icons", dict())
            self.music_volume_slider.set_value(content.get("music_volume", 25))

        pygame.mixer.music.set_volume(round(self.music_volume_slider.value) / 100)

    def save_settings(self) -> None:
        with open("../resources/data/settings.json", "w") as file:
            content: dict[str, bool | dict[str, int] | int] = {
                "show_hitboxes": self.show_hitboxes,
                "pause_after_death": self.pause_after_death,
                "is_player_immortal": self.is_player_immortal,
                "platformer_mode": self.platformer_mode,

                "player_first_color": self.player_first_color,
                "player_second_color": self.player_second_color,
                "player_icons": self.player_icons,
                "music_volume": round(self.music_volume_slider.value)
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

        elif self.__is_player_immortal_btn.is_just_pressed():
            self.is_player_immortal = not self.is_player_immortal

        elif self.__platformer_mode_btn.is_just_pressed():
            self.platformer_mode = not self.platformer_mode

        self.music_volume_slider.update()

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

        self.__is_player_immortal_btn.draw(surface)
        self.__is_player_immortal_btn.draw_text(surface, "Player immortality", UIConfig.fonts.get("jetbrains_20l"), "#ffffff",
                                                offset=[UIConfig.CHECKBOX_SIZE[0] + 8, -1])

        if self.is_player_immortal:
            surface.blit(UIConfig.CHECKBOX_ACTIVE_TEXTURE, self.__is_player_immortal_btn.rect.topleft)

        self.__platformer_mode_btn.draw(surface)
        self.__platformer_mode_btn.draw_text(surface, "Platformer mode", UIConfig.fonts.get("jetbrains_20l"), "#ffffff",
                                             offset=[UIConfig.CHECKBOX_SIZE[0] + 8, -1])

        if self.platformer_mode:
            surface.blit(UIConfig.CHECKBOX_ACTIVE_TEXTURE, self.__platformer_mode_btn.rect.topleft)

        surface.blit(self.__music_volume_lbl,
                     [self.music_volume_slider.rect.centerx - self.__music_volume_lbl.width / 2, 0])
        self.music_volume_slider.draw(surface)
