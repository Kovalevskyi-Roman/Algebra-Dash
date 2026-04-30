import pygame

from game_state.game_state import GameState
from ui import UIConfig, Button
from level import Level
from window import Window


class CustomLevelsState(GameState):
    def __init__(self, game_state_manager, *args, **kwargs) -> None:
        super().__init__(game_state_manager, *args, **kwargs)

        # self.__levels: tuple[tuple[str, dict[str, ...]], ...] = tuple(
        #     filter(lambda level: not level[1].get("is_original", False), Level.levels.items())
        # )
        self.__levels: tuple[tuple[str, dict[str, ...]], ...] = tuple(
            filter(lambda level: True, Level.levels.items())
        )
        self.__selected_level: int = -1
        self.__level_surfaces: tuple[pygame.Surface, ...] = tuple()
        self.__level_surface_size: pygame.Vector2 = pygame.Vector2(600, 40)
        self.__level_surface_x: int = int(Window.SIZE[0] / 2 - self.__level_surface_size.x / 2)
        self.__level_surfaces_padding: int = 8
        self.__scroll: int = self.__level_surfaces_padding

        self.__edit_btn: Button = Button(
            pygame.Rect(4, Window.SIZE[1] - 50, Window.SIZE[0] / 3 - 16, 48),
            pygame.Surface((Window.SIZE[0] / 3 - 16, 48)),
        )
        self.__edit_btn.texture.fill("#ffffff")

        self.update_level_surfaces()

    def update_level_surfaces(self) -> None:
        level_surfaces: list[pygame.Surface] = list()
        for i, level in enumerate(self.__levels):
            surface = pygame.Surface(self.__level_surface_size)

            if self.__selected_level == i:
                surface.fill("#d0d0d0")
            else:
                surface.fill("#676767")

            level_name = UIConfig.fonts.get("tahoma_20").render(level[1].get("level_name"), True, "#000000")
            surface.blit(level_name, [6, self.__level_surface_size.y / 2 - level_name.height / 2])

            level_surfaces.append(surface)

        self.__level_surfaces = tuple(level_surfaces)

    def update(self, *args, **kwargs) -> None:

        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self._game_state_manager.change_state(self._game_state_manager.MENU_STATE)
            return

        mouse_press = pygame.mouse.get_just_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_scroll = tuple(filter(lambda e: e.type == pygame.MOUSEWHEEL, Window.events))
        if mouse_scroll:
            self.__scroll += mouse_scroll[0].y * 10
            if self.__scroll > self.__level_surfaces_padding:
                self.__scroll = self.__level_surfaces_padding

        if self.__edit_btn.is_pressed() and self.__selected_level != -1:
            editor_state = self._game_state_manager.game_states.get(self._game_state_manager.EDITOR_STATE, None)
            if editor_state is None:
                raise RuntimeError("Could not find editor state.")

            editor_state.level_path = self.__levels[self.__selected_level][0]
            self._game_state_manager.change_state(self._game_state_manager.EDITOR_STATE)

        if not mouse_press[0]:
            return

        # if any of level buttons pressed
        for i, level in enumerate(self.__levels):
            y = i * (self.__level_surface_size.y + self.__level_surfaces_padding) + self.__scroll
            if y > Window.SIZE[1]:
                break

            if y + self.__level_surface_size.y < 0:
                continue

            if pygame.Rect((self.__level_surface_x, y), self.__level_surface_size).collidepoint(mouse_pos):
                self.__selected_level = i
                break

            self.__selected_level = -1

        self.update_level_surfaces()

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        for i, level_surface in enumerate(self.__level_surfaces):
            y = i * (self.__level_surface_size.y + self.__level_surfaces_padding) + self.__scroll
            if y > Window.SIZE[1]:
                break

            if y + self.__level_surface_size.y < 0:
                continue

            surface.blit(level_surface, [self.__level_surface_x, y])

        self.__edit_btn.draw(surface)
        self.__edit_btn.draw_text(surface, "Edit", UIConfig.fonts.get("tahoma_20"), "#000000")
