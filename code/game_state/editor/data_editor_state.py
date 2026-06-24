import pygame

from game_state.game_state import GameState
from level import Level
from music_manager import MusicManager
from ui import Entry, Button, UIConfig
from window import Window


class DataEditorState(GameState):
    def __init__(self, game_state_manager, *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)

        self.level: tuple[str, dict[str, ...]] | None = None  # (path, level_data)

        self.__x_offset = 100
        self.__level_name_entry: Entry = Entry(
            pygame.Rect(Window.SIZE[0] / 2 - 290 + self.__x_offset, 80, 580, 90),
            pygame.Surface((580, 90)),
            UIConfig.fonts.get("jetbrains_26m"),
            "#000000",
            max_text_length=28
        )
        self.__level_name_entry.texture.fill("#7A7A7A")

        self.__editor_btn_size: pygame.Vector2 = pygame.Vector2(140, 140)
        self.__editor_btn: Button = Button(
            pygame.Rect(
                (Window.SIZE[0] / 2 - self.__editor_btn_size.x / 2 + self.__x_offset, 320 - self.__editor_btn_size.y / 2),
                self.__editor_btn_size
            ),
            pygame.image.load("../resources/textures/ui/edit_button_round.png").convert_alpha()
        )
        self.__editor_btn.scale_texture_to_rect()

        self.__play_btn_size: pygame.Vector2 = pygame.Vector2(110, 110)
        self.__play_btn: Button = Button(
            pygame.Rect(
                (Window.SIZE[0] / 3 - self.__play_btn_size.x / 2 + self.__x_offset, 320 - self.__play_btn_size.y / 2),
                self.__play_btn_size
            ),
            pygame.image.load("../resources/textures/ui/play_button_round.png").convert_alpha()
        )
        self.__play_btn.scale_texture_to_rect()

        self.__back_btn_size: pygame.Vector2 = pygame.Vector2(110, 110)
        self.__back_btn: Button = Button(
            pygame.Rect(
                (Window.SIZE[0] * (2 / 3) - self.__back_btn_size.x / 2 + self.__x_offset, 320 - self.__back_btn_size.y / 2),
                self.__back_btn_size
            ),
            pygame.image.load("../resources/textures/ui/back_button.png").convert_alpha()
        )
        self.__back_btn.scale_texture_to_rect()

        self.__level_was_deleted: bool = False
        self.__delete_level_btn: Button = Button(
            pygame.Rect(Window.SIZE[0] - 70, Window.SIZE[1] - 70, 60, 60),
            pygame.Surface((60, 60))
        )
        self.__delete_level_btn.texture.fill("#7A7A7A")
        self.__delete_level_btn.texture.blit(
            pygame.image.load("../resources/textures/ui/trash_icon.png").convert_alpha(),
            [5, 5]
        )

        self.__current_music: int = 0
        self.__music_label = UIConfig.fonts.get("jetbrains_20l").render("Music name and offset", True, "#ffffff")
        self.__previous_music_btn: Button = Button(
            pygame.Rect(10, 32, 24, 24),
            pygame.Surface((24, 24))
        )
        self.__previous_music_btn.texture.fill("#7A7A7A")
        self.__next_music_btn: Button = Button(
            pygame.Rect(10 + 24 + 220, 32, 24, 24),
            pygame.Surface((24, 24))
        )
        self.__next_music_btn.texture.fill("#7A7A7A")
        self.__music_start_pos_entry: Entry = Entry(
            pygame.Rect(34, 64, 220, 32),
            pygame.Surface((220, 32)),
            UIConfig.fonts.get("jetbrains_16l"),
            "#000000",
            type_="int",
            max_text_length=8
        )
        self.__music_start_pos_entry.texture.fill("#646464")

        self.__bg_color_label = UIConfig.fonts.get("jetbrains_20l").render("BG Color", True, "#ffffff")
        self.__bg_color_entry: Entry = Entry(
            pygame.Rect(34, 136, 220, 32),
            pygame.Surface((220, 32)),
            UIConfig.fonts.get("jetbrains_16l"),
            "#000000",
            max_text_length=7
        )
        self.__bg_color_entry.texture.fill("#646464")

        self.__ground_color_label = UIConfig.fonts.get("jetbrains_20l").render("Ground Color", True, "#ffffff")
        self.__ground_color_entry: Entry = Entry(
            pygame.Rect(34, 206, 220, 32),
            pygame.Surface((220, 32)),
            UIConfig.fonts.get("jetbrains_16l"),
            "#000000",
            max_text_length=7
        )
        self.__ground_color_entry.texture.fill("#646464")

    def on_state_enter(self, *args, **kwargs) -> None:
        self.level = (self.level[0], Level.levels.get(self.level[0]))
        self.__level_name_entry.set_text(self.level[1].get("level_name"))
        self.__current_music = MusicManager.music.index(self.level[1].get("music_name"))
        self.__music_start_pos_entry.set_text(str(self.level[1].get("music_start_pos", 0)))
        self.__bg_color_entry.set_text(self.level[1].get("bg_color", "#0000ff"))
        self.__ground_color_entry.set_text(self.level[1].get("ground_color", "#000000"))

    def on_state_exit(self, *args, **kwargs) -> None:
        if not self.__level_was_deleted:
            Level.save_data(
                self.level[0], level_name=self.__level_name_entry.get_text(), music_name=self.level[1].get("music_name"),
                music_start_pos=self.level[1].get("music_start_pos"), bg_color=self.level[1].get("bg_color"),
                ground_color=self.level[1].get("ground_color")
            )
        self.__level_name_entry.active = False
        self.__music_start_pos_entry.active = False
        self.__level_was_deleted = False
        pygame.key.stop_text_input()

    def update(self, *args, **kwargs) -> None:
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            if self.__level_name_entry.active or self.__music_start_pos_entry.active or \
                    self.__bg_color_entry.active or self.__ground_color_entry.active:
                self.__level_name_entry.active = False
                self.__music_start_pos_entry.active = False
                self.__bg_color_entry.active = False
                self.__ground_color_entry.active = False
            else:
                self._game_state_manager.change_state(self._game_state_manager.CUSTOM_LEVELS_STATE)
                return

        self.__level_name_entry.update()
        if self.__level_name_entry.active:
            self.level[1]["level_name"] = self.__level_name_entry.get_text()

        self.__music_start_pos_entry.update()
        if self.__music_start_pos_entry.active:
            self.level[1]["music_start_pos"] = 0
            text = self.__music_start_pos_entry.get_text()
            if text and text.strip("."):
                self.level[1]["music_start_pos"] = float(text)

        self.__bg_color_entry.update()
        if not self.__bg_color_entry.active and self.__bg_color_entry.get_text() != self.level[1].get("bg_color", ""):
            self.__bg_color_entry.set_text(UIConfig.fix_hex_color(self.__bg_color_entry.get_text()))
            self.level[1]["bg_color"] = self.__bg_color_entry.get_text()

        self.__ground_color_entry.update()
        if not self.__ground_color_entry.active and self.__ground_color_entry.get_text() != self.level[1].get("ground_color", ""):
            self.__ground_color_entry.set_text(UIConfig.fix_hex_color(self.__ground_color_entry.get_text()))
            self.level[1]["ground_color"] = self.__ground_color_entry.get_text()

        if self.__back_btn.is_just_pressed():
            self._game_state_manager.change_state(self._game_state_manager.CUSTOM_LEVELS_STATE)

        elif self.__editor_btn.is_just_pressed():
            tile_editor_state = self._game_state_manager.game_states.get(self._game_state_manager.TILE_EDITOR_STATE, None)
            if tile_editor_state is None:
                raise AttributeError("State 'TILE_EDITOR_STATE' not found.")

            tile_editor_state.level_path = self.level[0]
            self._game_state_manager.change_state(self._game_state_manager.TILE_EDITOR_STATE)

        elif self.__play_btn.is_just_pressed():
            play_state = self._game_state_manager.game_states.get(self._game_state_manager.PLAY_STATE, None)
            if play_state is None:
                raise AttributeError("State 'PLAY_STATE' not found.")

            play_state.level_path = self.level[0]
            self._game_state_manager.change_state(self._game_state_manager.PLAY_STATE)

        elif self.__delete_level_btn.is_just_pressed():
            self.__level_was_deleted = True
            Level.delete(self.level[0])
            self._game_state_manager.change_state(self._game_state_manager.CUSTOM_LEVELS_STATE)

        elif self.__previous_music_btn.is_just_pressed():
            self.__current_music -= 1
            if self.__current_music < 0:
                self.__current_music = len(MusicManager.music) - 1

        elif self.__next_music_btn.is_just_pressed():
            self.__current_music += 1
            if self.__current_music >= len(MusicManager.music):
                self.__current_music = 0

        self.level[1]["music_name"] = MusicManager.music[self.__current_music]

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.__level_name_entry.draw(surface)

        self.__editor_btn.draw(surface)
        self.__play_btn.draw(surface)
        self.__back_btn.draw(surface)
        self.__delete_level_btn.draw(surface)

        # music name and start position
        surface.blit(self.__music_label, [self.__previous_music_btn.rect.right + 110 - self.__music_label.width / 2, 0])

        self.__previous_music_btn.draw(surface)
        self.__previous_music_btn.draw_text(surface, "<", UIConfig.fonts.get("jetbrains_16l"), "#000000")
        self.__next_music_btn.draw(surface)
        self.__next_music_btn.draw_text(surface, ">", UIConfig.fonts.get("jetbrains_16l"), "#000000")

        music_name = UIConfig.fonts.get("jetbrains_16l").render(self.level[1].get("music_name"), True, "#ffffff", wraplength=220)
        surface.blit(music_name, [self.__previous_music_btn.rect.right + 110 - music_name.width / 2, 32])

        self.__music_start_pos_entry.draw(surface)

        # bg color
        surface.blit(self.__bg_color_label, [self.__previous_music_btn.rect.right + 110 - self.__bg_color_label.width / 2, 104])
        self.__bg_color_entry.draw(surface)

        # ground color
        surface.blit(self.__ground_color_label, [self.__previous_music_btn.rect.right + 110 - self.__ground_color_label.width / 2, 176])
        self.__ground_color_entry.draw(surface)
