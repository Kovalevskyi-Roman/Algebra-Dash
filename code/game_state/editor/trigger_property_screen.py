import pygame

from ui import UIConfig, Entry
from trigger import Trigger, MoveTrigger, ColorTrigger


class TriggerPropertyScreen:
    def __init__(self) -> None:
        self.active: bool = False
        self.__selected_trigger: Trigger | None = None

        self.__group_id_lbl: pygame.Surface = UIConfig.create_label("jetbrains_20m", "Group ID:  Work time:")
        self.__group_id_entry: Entry = Entry(
            pygame.Rect(8, 40, 140, 40),
            UIConfig.fonts.get("jetbrains_20l"),
            "#ffffff",
            type_=Entry.INT
        )
        self.__group_id_entry.texture.fill("#646464")

        self.__work_time_entry: Entry = Entry(
            pygame.Rect(self.__group_id_entry.rect.right + 8, 40, 140, 40),
            UIConfig.fonts.get("jetbrains_20l"),
            "#ffffff",
            type_=Entry.FLOAT
        )
        self.__work_time_entry.texture.fill("#646464")

        # move trigger ----------------------------------
        self.__move_by_lbl: pygame.Surface = UIConfig.create_label("jetbrains_20m", "Move by XY:")
        self.__move_by_x_entry: Entry = Entry(
            pygame.Rect(8, self.__group_id_entry.rect.bottom + 40, 140, 40),
            UIConfig.fonts.get("jetbrains_20l"),
            "#ffffff",
            type_=Entry.INT
        )
        self.__move_by_x_entry.texture.fill("#646464")
        self.__move_by_y_entry: Entry = Entry(
            pygame.Rect(self.__move_by_x_entry.rect.right + 8, self.__move_by_x_entry.rect.y, 140, 40),
            UIConfig.fonts.get("jetbrains_20l"),
            "#ffffff",
            type_=Entry.INT
        )
        self.__move_by_y_entry.texture.fill("#646464")

        # color trigger ---------------------------------
        self.__color_lbl: pygame.Surface = UIConfig.create_label("jetbrains_20m", "Color:")
        self.__color_entry: Entry = Entry(
            pygame.Rect(8, self.__group_id_entry.rect.bottom + 40, 140, 40),
            UIConfig.fonts.get("jetbrains_20l"),
            "#ffffff",
            max_text_length=7
        )
        self.__color_entry.texture.fill("#646464")

    def on_enter(self, selected_trigger: Trigger):
        self.__selected_trigger = selected_trigger

        self.__group_id_entry.set_text(str(selected_trigger.group_id))
        self.__work_time_entry.set_text(str(selected_trigger.work_time))

        # move trigger ----------------------------------
        if isinstance(self.__selected_trigger, MoveTrigger):
            if self.__selected_trigger.data.get("move_by", None) is None:
                self.__selected_trigger.data["move_by"] = [0, 0]
            self.__move_by_x_entry.set_text(str(self.__selected_trigger.data.get("move_by")[0]))
            self.__move_by_y_entry.set_text(str(self.__selected_trigger.data.get("move_by")[1]))

        # color trigger ---------------------------------
        elif isinstance(self.__selected_trigger, ColorTrigger):
            if self.__selected_trigger.data.get("color", None) is None:
                self.__selected_trigger.data["color"] = "#000000"
            self.__color_entry.set_text(self.__selected_trigger.data.get("color"))

    def on_escape_pressed(self) -> None:
        if self.__group_id_entry.active or self.__work_time_entry.active or \
                self.__move_by_x_entry.active or self.__move_by_y_entry.active or self.__color_entry.active:
            self.__group_id_entry.update()
            self.__work_time_entry.update()

            # move trigger ----------------------------------
            if isinstance(self.__selected_trigger, MoveTrigger):
                self.__move_by_x_entry.update()
                self.__move_by_y_entry.update()

            # color trigger ---------------------------------
            elif isinstance(self.__selected_trigger, ColorTrigger):
                self.__color_entry.update()

            return

        self.__selected_trigger.group_id = int(self.__group_id_entry.get_text())
        self.__selected_trigger.work_time = float(self.__work_time_entry.get_text())
        # move trigger ----------------------------------
        if isinstance(self.__selected_trigger, MoveTrigger):
            self.__selected_trigger.data["move_by"][0] = int(self.__move_by_x_entry.get_text())
            self.__selected_trigger.data["move_by"][1] = int(self.__move_by_y_entry.get_text())

        # color trigger ---------------------------------
        elif isinstance(self.__selected_trigger, ColorTrigger):
            self.__selected_trigger.data["color"] = UIConfig.fix_hex_color(self.__color_entry.get_text())

        self.active = False

    def update(self) -> None:
        self.__group_id_entry.update()
        self.__work_time_entry.update()

        # move trigger ----------------------------------
        if isinstance(self.__selected_trigger, MoveTrigger):
            self.__move_by_x_entry.update()
            self.__move_by_y_entry.update()

        # color trigger ---------------------------------
        elif isinstance(self.__selected_trigger, ColorTrigger):
            self.__color_entry.update()

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.__group_id_lbl, [8, self.__group_id_entry.rect.y - self.__group_id_lbl.height])
        self.__group_id_entry.draw(surface)
        self.__work_time_entry.draw(surface)

        # move trigger ----------------------------------
        if isinstance(self.__selected_trigger, MoveTrigger):
            surface.blit(self.__move_by_lbl, [8, self.__move_by_x_entry.rect.y - self.__move_by_lbl.height])
            self.__move_by_x_entry.draw(surface)
            self.__move_by_y_entry.draw(surface)

        # color trigger ---------------------------------
        elif isinstance(self.__selected_trigger, ColorTrigger):
            surface.blit(self.__color_lbl, [8, self.__color_entry.rect.y - self.__color_lbl.height])
            self.__color_entry.draw(surface)
