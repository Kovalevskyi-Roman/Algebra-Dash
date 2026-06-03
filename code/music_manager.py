import pathlib
import pygame


class MusicManager:
    music: tuple[str, ...] | None = None
    loaded_music: str = ""
    playing: bool = False
    paused: bool = False

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
        pygame.mixer.music.set_volume(0.2)

    @classmethod
    def load(cls, music_name: str) -> None:
        if music_name not in cls.music:
            raise ValueError(f"Music '{music_name}' not found")

        cls.unload()

        pygame.mixer.music.load(f"../resources/music/{music_name}")
        cls.loaded_music = music_name
        cls.playing = False
        cls.paused = False

    @classmethod
    def unload(cls) -> None:
        pygame.mixer.music.unload()
        cls.loaded_music = ""
        cls.playing = False
        cls.paused = False

    @classmethod
    def play(cls, music_name: str = "", loops: int = 0, start: float = 0, fade_ms: int = 0) -> None:
        """Loads and plays music, if music_name is empty plays loaded music"""
        if music_name:
            cls.load(music_name)

        pygame.mixer.music.play(loops, start, fade_ms)
        cls.playing = True

    @classmethod
    def stop(cls) -> None:
        pygame.mixer.music.stop()
        cls.playing = False
        cls.paused = False

    @classmethod
    def pause(cls) -> None:
        pygame.mixer.music.pause()
        cls.paused = True

    @classmethod
    def unpause(cls) -> None:
        pygame.mixer.music.unpause()
        cls.paused = False
