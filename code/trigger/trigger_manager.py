import pygame

from .trigger import Trigger
from .move_trigger import MoveTrigger


class TriggerManager:
    TRIGGERS: dict[str, type[Trigger]] = {
        "trigger": Trigger,
        "move_trigger": MoveTrigger
    }

    @classmethod
    def create_trigger(cls, json_trigger: dict[str, ...]) -> Trigger:
        trigger_type = cls.TRIGGERS.get(json_trigger.get("id"), None)

        if trigger_type is None:
            raise ValueError(f"Trigger {json_trigger.get("id")} not found.")

        trigger = trigger_type(json_trigger)
        return trigger
