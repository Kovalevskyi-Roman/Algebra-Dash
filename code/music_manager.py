import pathlib
import pygame

from window import Window


class MusicManager:
    music: tuple[str, ...] | None = None
    loaded_music: str = ""
    playing: bool = False
    paused: bool = False
    position: float = 0  # in seconds

    @classmethod
    def init(cls) -> None:
        music: list[str] = list()

        path: pathlib.Path = pathlib.Path("../resources/music/")
        for obj in path.iterdir():
            if not obj.is_file():
                continue

            if obj.suffix == ".ogg":
                music.append(obj.name)

        cls.music = tuple(music)

    @classmethod
    def update(cls) -> None:
        if cls.playing and not cls.paused:
            cls.position += Window.DELTA

    @classmethod
    def load(cls, music_name: str) -> None:
        if music_name not in cls.music:
            raise ValueError(f"Music '{music_name}' not found")

        cls.unload()

        pygame.mixer.music.load(f"../resources/music/{music_name}")
        cls.loaded_music = music_name
        cls.playing = False
        cls.paused = False
        cls.position = 0

    @classmethod
    def unload(cls) -> None:
        pygame.mixer.music.unload()
        cls.loaded_music = ""
        cls.playing = False
        cls.paused = False
        cls.position = 0

    @classmethod
    def play(cls, music_name: str = "", loops: int = 0, start: float = 0, fade_ms: int = 0) -> None:
        """Loads and plays music, if music_name is empty plays loaded music"""
        if music_name:
            cls.load(music_name)

        pygame.mixer.music.play(loops, start, fade_ms)
        cls.playing = True
        cls.paused = False
        cls.position = start

    @classmethod
    def stop(cls) -> None:
        pygame.mixer.music.stop()
        cls.playing = False
        cls.paused = False
        cls.position = 0

    @classmethod
    def pause(cls) -> None:
        pygame.mixer.music.pause()
        cls.paused = True

    @classmethod
    def unpause(cls) -> None:
        pygame.mixer.music.unpause()
        cls.paused = False

    @classmethod
    def rewind_by(cls, time: float) -> None:
        cls.position -= time
        if cls.position < 0:
            cls.position = 0

        was_paused: bool = cls.paused
        cls.play(start=cls.position)
        if was_paused:
            cls.pause()
