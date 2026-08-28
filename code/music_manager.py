import pathlib
import pygame

from window import Window
from tile import TileManager


class MusicManager:
    music: tuple[str, ...] | None = None
    loaded_music: str = ""
    playing: bool = False
    paused: bool = False
    position: float = 0  # in seconds
    music_line_speed: float = 0.0  # pixels per frame

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
        cls.music_line_speed = TileManager.TILE_DATA.get("x2_speed_buster").get("properties").get("speed")

    @classmethod
    def update(cls) -> None:
        if cls.playing and not cls.paused:
            cls.position += Window.DELTA
            cls.position = round(cls.position, 3)

        if not pygame.mixer.music.get_busy() and not cls.paused and cls.playing:
            cls.stop()

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
    def fade_out(cls, time_ms: int) -> None:
        pygame.mixer.music.fadeout(time_ms)
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
        cls.position = round(cls.position, 3)
        if cls.position < 0:
            cls.position = 0

        was_paused: bool = cls.paused
        cls.play(start=cls.position)
        if was_paused:
            cls.pause()

    @classmethod
    def step_music_line(cls, position: float, tiles: list) -> float:
        position += cls.music_line_speed
        for tile in tiles:
            if not hasattr(tile, "speed"):
                continue

            if position > tile.rect.x:
                cls.music_line_speed = tile.speed

        return position

    @classmethod
    def get_position_from_time(cls, time: float, tiles: list) -> float:
        music_line_pos: float = 0

        while time > 0:
            time -= Window.DELTA
            time = round(time, 2)
            music_line_pos = cls.step_music_line(music_line_pos, tiles)

        return music_line_pos

    @classmethod
    def get_time_from_position(cls, position: float, tiles: list) -> float:
        time: float = 0
        current_position: float = 0
        while current_position < position:
            time += Window.DELTA
            current_position = cls.step_music_line(current_position, tiles)

        return round(time, 3)
