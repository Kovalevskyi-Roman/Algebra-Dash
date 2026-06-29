import pygame

from window import Window
from ui import UIConfig, Button, Entry
from tile import Tile


class TilePropertyScreen:
    def __init__(self) -> None:
        self.active: bool = False

        self.__tile_color_lbl: pygame.Surface = UIConfig.fonts.get("jetbrains_20m").render("Color", True, "#ffffff")
        self.__tile_color_entry: Entry = Entry(
            pygame.Rect(8, 40, 240, 32),
            UIConfig.fonts.get("jetbrains_20l"),
            "#000000",
            max_text_length=7
        )
        self.__tile_color_entry.texture.fill("#646464")

    def on_enter(self, selected_tiles: list[Tile]) -> None:
        self.__tile_color_entry.set_text(selected_tiles[0].color)

    def on_escape_pressed(self) -> None:
        if self.__tile_color_entry.active:
            self.__tile_color_entry.active = False

        elif self.active:
            self.active = False

    def update(self, selected_tiles: list[Tile]) -> None:
        self.__tile_color_entry.update()

        change_color = self.__tile_color_entry.get_text() != selected_tiles[0].color
        if change_color and not self.__tile_color_entry.active:
            self.__tile_color_entry.set_text(UIConfig.fix_hex_color(self.__tile_color_entry.get_text()))

        for tile in selected_tiles:
            if change_color:
                tile.color = UIConfig.fix_hex_color(self.__tile_color_entry.get_text())

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.__tile_color_lbl, (self.__tile_color_entry.rect.centerx - self.__tile_color_lbl.width / 2, 8))
        self.__tile_color_entry.draw(surface)
        pygame.draw.rect(
            surface,
            UIConfig.fix_hex_color(self.__tile_color_entry.get_text()),
            [self.__tile_color_entry.rect.right + 4, self.__tile_color_entry.rect.y,
             self.__tile_color_entry.rect.height, self.__tile_color_entry.rect.height]
        )
