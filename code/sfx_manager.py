import pathlib
import pygame


class SFXManager:
    sounds: dict[str, pygame.mixer.Sound] = dict()
    volume: float = 1

    @classmethod
    def init(cls) -> None:
        path = pathlib.Path("../resources/sfx/")
        for obj in path.iterdir():
            if not obj.is_file():
                continue

            if obj.suffix == ".wav":
                cls.sounds[obj.stem] = pygame.mixer.Sound(obj)

        cls.set_volume(0.25)
        cls.set_local_volume("death_sound", 1)

    @classmethod
    def set_volume(cls, volume: float) -> None:
        cls.volume = volume

        for sound in cls.sounds.values():
            sound.set_volume(cls.volume)

    @classmethod
    def set_local_volume(cls, sound_name: str, volume: float) -> None:
        sound = cls.sounds.get(sound_name, None)
        if sound is None:
            return

        sound.set_volume(volume)

    @classmethod
    def get_length(cls, sound_name: str) -> int:
        sound = cls.sounds.get(sound_name, None)
        if sound is None:
            return 0

        return int(sound.get_length() * 1000)

    @classmethod
    def play(cls, sound_name: str, loops: int = 0, max_time: int = 0, fade_ms: int = 0) -> None:
        sound = cls.sounds.get(sound_name, None)
        if sound is None:
            return

        sound.play(loops, max_time, fade_ms)

    @classmethod
    def stop(cls, sound_name: str) -> None:
        sound = cls.sounds.get(sound_name, None)
        if sound is None:
            return

        sound.stop()
