import json
import pygame

from .trigger import Trigger
from .move_trigger import MoveTrigger
from tile import Tile


class TriggerManager:
    TRIGGERS: dict[str, type[Trigger]] = {
        "trigger": Trigger,
        "move_trigger": MoveTrigger
    }
    textures: dict[str, pygame.Surface] = dict()

    __selection_surface: pygame.Surface | None = None

    @classmethod
    def get_id_from_type(cls, trigger: Trigger) -> str:
        for trigger_id, trigger_type in cls.TRIGGERS.items():
            if trigger_type == type(trigger):
                return trigger_id

        return ""

    @classmethod
    def load_textures(cls) -> None:
        with open("../resources/data/triggers.json", "r") as file:
            for json_trigger in json.load(file):
                if json_trigger.get("id") not in cls.TRIGGERS.keys():
                    continue

                cls.textures[json_trigger.get("id")] = pygame.image.load(
                    f"../resources/textures/triggers/{json_trigger.get("texture_path")}"
                ).convert_alpha()

        cls.__selection_surface = pygame.Surface((Tile.SIZE, Tile.SIZE), flags=pygame.SRCALPHA)
        cls.__selection_surface.fill((0, 255, 0, 127))

    @classmethod
    def create_trigger(cls, json_trigger: dict[str, ...]) -> Trigger:
        trigger_type = cls.TRIGGERS.get(json_trigger.get("id"), None)

        if trigger_type is None:
            raise ValueError(f"Trigger {json_trigger.get("id")} not found.")

        trigger = trigger_type(json_trigger)
        return trigger

    @classmethod
    def draw(cls, surface: pygame.Surface, trigger: Trigger, camera_offset: pygame.Vector2, selected: bool = False) -> None:
        if trigger.position.x < camera_offset.x or trigger.position.x > surface.get_width() + camera_offset.x or \
                trigger.position.y < camera_offset.y or trigger.position.y > surface.get_height() + camera_offset.y:
            return

        texture: pygame.Surface = cls.textures.get(cls.get_id_from_type(trigger))
        pygame.draw.line(surface, "#ffffff",
                         [trigger.position.x - camera_offset.x, 0],
                         [trigger.position.x - camera_offset.x, surface.get_height()]
                         )
        surface.blit(texture, trigger.position - camera_offset - pygame.Vector2(Tile.SIZE, Tile.SIZE) * 0.5)
        if selected:
            surface.blit(cls.__selection_surface, trigger.position - camera_offset - pygame.Vector2(Tile.SIZE, Tile.SIZE) * 0.5)
