import pygame

from ui import UIConfig, Button, Entry
from tile import Tile


class TilePropertyScreen:
    def __init__(self) -> None:
        self.active: bool = False

        self.__color_lbl: pygame.Surface = UIConfig.create_label("jetbrains_20m", "Color")
        self.__color_entry: Entry = Entry(
            pygame.Rect(8, 40, 240, 32),
            UIConfig.fonts.get("jetbrains_20l"),
            "#ffffff",
            max_text_length=7
        )
        self.__color_entry.texture.fill("#646464")

        self.__group_ids_lbl: pygame.Surface = UIConfig.create_label("jetbrains_20m", "Group id's")
        self.__group_ids_entry: Entry = Entry(
            pygame.Rect(self.__color_entry.rect.right + 128, 40, 240, 32),
            UIConfig.fonts.get("jetbrains_20l"),
            "#ffffff",
            type_=Entry.INT
        )
        self.__group_ids_entry.texture.fill("#646464")
        self.__add_group_id_btn: Button = Button(
            pygame.Rect(self.__group_ids_entry.rect.right + 8, 40, 32, 32),
            text="+", font=UIConfig.fonts.get("jetbrains_16l")
        )
        self.__add_group_id_btn.texture.fill("#646464")
        self.__remove_group_id_btn: Button = Button(
            pygame.Rect(self.__add_group_id_btn.rect.right + 8, 40, 32, 32),
            text="-", font=UIConfig.fonts.get("jetbrains_16l")
        )
        self.__remove_group_id_btn.texture.fill("#646464")
        self.__tile_group_ids_lbl: pygame.Surface = UIConfig.create_label("jetbrains_20l", "")

    def on_enter(self, selected_tiles: list[Tile]) -> None:
        self.__color_entry.set_text(selected_tiles[0].color)
        group_ids: set[int] = set()
        for tile in selected_tiles:
            group_ids.update(tile.group_ids)

        self.__tile_group_ids_lbl = UIConfig.create_label("jetbrains_20l", str(group_ids))

    def on_escape_pressed(self) -> None:
        if self.__color_entry.active or self.__group_ids_entry.active:
            self.__color_entry.active = False
            self.__group_ids_entry.active = False

        elif self.active:
            self.active = False
            self.__group_ids_entry.set_text("")

    def update(self, selected_tiles: list[Tile]) -> None:
        self.__color_entry.update()
        self.__group_ids_entry.update()

        change_color = self.__color_entry.get_text() != selected_tiles[0].color
        if change_color and not self.__color_entry.active:
            self.__color_entry.set_text(UIConfig.fix_hex_color(self.__color_entry.get_text()))

            for tile in selected_tiles:
                if change_color:
                    tile.color = UIConfig.fix_hex_color(self.__color_entry.get_text())

        if not self.__group_ids_entry.get_text():
            return

        if self.__add_group_id_btn.is_just_pressed():
            new_id: int = int(self.__group_ids_entry.get_text())
            group_ids: set[int] = set()
            for tile in selected_tiles:
                tile.group_ids.add(new_id)
                group_ids.update(tile.group_ids)

            self.__tile_group_ids_lbl = UIConfig.create_label("jetbrains_20l", str(group_ids))
            self.__group_ids_entry.set_text("")

        elif self.__remove_group_id_btn.is_just_pressed():
            remove_id: int = int(self.__group_ids_entry.get_text())
            group_ids: set[int] = set()
            for tile in selected_tiles:
                if remove_id in tile.group_ids:
                    tile.group_ids.remove(remove_id)
                group_ids.update(tile.group_ids)

            self.__tile_group_ids_lbl = UIConfig.create_label("jetbrains_20l", str(group_ids))
            self.__group_ids_entry.set_text("")

    def draw(self, surface: pygame.Surface) -> None:
        # color settings
        surface.blit(self.__color_lbl, (self.__color_entry.rect.centerx - self.__color_lbl.width / 2, 8))
        self.__color_entry.draw(surface)
        pygame.draw.rect(
            surface,
            UIConfig.fix_hex_color(self.__color_entry.get_text()),
            [self.__color_entry.rect.right + 4, self.__color_entry.rect.y,
             self.__color_entry.rect.height, self.__color_entry.rect.height]
        )
        # group id settings
        surface.blit(
            self.__group_ids_lbl,
            (self.__group_ids_entry.rect.x + (self.__remove_group_id_btn.rect.right - self.__group_ids_entry.rect.x) / 2, 8)
        )
        surface.blit(self.__tile_group_ids_lbl, (self.__group_ids_entry.rect.x, self.__group_ids_entry.rect.bottom + 8))
        self.__group_ids_entry.draw(surface)
        self.__add_group_id_btn.draw(surface)
        self.__add_group_id_btn.draw_text(surface)
        self.__remove_group_id_btn.draw(surface)
        self.__remove_group_id_btn.draw_text(surface)
