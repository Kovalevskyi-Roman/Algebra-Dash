import pygame

from ui import Button
from window import Window
from tile import TileManager
from trigger import TriggerManager


class BottomPanel:
    TILE_MODE: int = 0
    TRIGGER_MODE: int = 1

    def __init__(self) -> None:
        self.__surface: pygame.Surface = pygame.Surface((Window.SIZE[0], Window.SIZE[1] / 5), flags=pygame.SRCALPHA)
        self.__icon_size: tuple[int, int] = (24, 24)
        self.__icon_padding: int = 8
        self.selected_tile: str = ""
        self.selected_trigger: str = ""
        self.mode: int = self.TILE_MODE

        self.__change_mode_btn: Button = Button(
            pygame.Rect(
                (Window.SIZE[0] - self.__icon_size[0] - self.__icon_padding, Window.SIZE[1] - self.__icon_size[1] - self.__icon_padding),
                self.__icon_size
            )
        )
        self.__change_mode_btn.texture.fill("#9b9b9b")

        self.__update_surface()

    def get_surface_size(self) -> tuple[int, int]:
        return self.__surface.get_size()

    def __update_surface(self) -> None:
        self.__surface.fill("#7a7a7a7f")
        x = self.__icon_padding
        y = self.__icon_padding

        if self.mode == self.TILE_MODE:
            for tile in TileManager.TILE_DATA.items():
                if tile[1].get("texture", None) is None:
                    continue

                texture = pygame.transform.scale(tile[1].get("texture"), self.__icon_size)
                if self.selected_tile == tile[0]:
                    pygame.draw.rect(
                        self.__surface,
                        "#17ff17",
                        [
                            x - self.__icon_padding / 4,
                            y - self.__icon_padding / 4,
                            self.__icon_size[0] + self.__icon_padding / 2,
                            self.__icon_size[1] + self.__icon_padding / 2
                        ],
                    )
                self.__surface.blit(texture, (x, y))

                x += self.__icon_size[0] + self.__icon_padding
                if x >= self.__change_mode_btn.rect.x:
                    x = self.__icon_padding
                    y += self.__icon_size[1] + self.__icon_padding

        elif self.mode == self.TRIGGER_MODE:
            for trigger in TriggerManager.textures.items():
                if trigger[1] is None:
                    continue

                texture = pygame.transform.scale(trigger[1], self.__icon_size)
                if self.selected_trigger == trigger[0]:
                    pygame.draw.rect(
                        self.__surface,
                        "#17ff17",
                        [
                            x - self.__icon_padding / 4,
                            y - self.__icon_padding / 4,
                            self.__icon_size[0] + self.__icon_padding / 2,
                            self.__icon_size[1] + self.__icon_padding / 2
                        ],
                    )
                self.__surface.blit(texture, (x, y))

                x += self.__icon_size[0] + self.__icon_padding
                if x >= self.__change_mode_btn.rect.x:
                    x = self.__icon_padding
                    y += self.__icon_size[1] + self.__icon_padding

    def reset(self) -> None:
        self.selected_tile = ""
        self.selected_trigger = ""
        self.mode = self.TILE_MODE
        self.__update_surface()

    def update(self, mouse_pos: pygame.Vector2) -> None:
        if self.__change_mode_btn.is_just_pressed():
            self.selected_tile = ""
            self.selected_trigger = ""
            match self.mode:
                case self.TILE_MODE:
                    self.mode = self.TRIGGER_MODE

                case self.TRIGGER_MODE:
                    self.mode = self.TILE_MODE

            self.__update_surface()

        x = self.__icon_padding
        y = Window.SIZE[1] - self.__surface.height + self.__icon_padding

        if self.mode == self.TILE_MODE:
            self.selected_tile = ""
            for tile in TileManager.TILE_DATA.items():
                if tile[1].get("texture", None) is None:
                    continue

                if pygame.Rect((x, y), self.__icon_size).collidepoint(mouse_pos):
                    self.selected_tile = tile[0]
                    self.__update_surface()
                    return

                x += self.__icon_size[0] + self.__icon_padding
                if x >= self.__change_mode_btn.rect.x:
                    x = self.__icon_padding
                    y += self.__icon_size[1] + self.__icon_padding

        elif self.mode == self.TRIGGER_MODE:
            self.selected_trigger = ""
            for trigger in TriggerManager.textures.items():
                if trigger[1] is None:
                    continue

                if pygame.Rect((x, y), self.__icon_size).collidepoint(mouse_pos):
                    self.selected_trigger = trigger[0]
                    self.__update_surface()
                    return

                x += self.__icon_size[0] + self.__icon_padding
                if x >= self.__change_mode_btn.rect.x:
                    x = self.__icon_padding
                    y += self.__icon_size[1] + self.__icon_padding

        self.__update_surface()

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.__surface, (0, Window.SIZE[1] - self.__surface.height))
        self.__change_mode_btn.draw(surface)
