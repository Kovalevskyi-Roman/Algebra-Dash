import json
import pathlib
import shutil
import random

import pygame

from music_manager import MusicManager
from trigger import Trigger, TriggerManager
from ui import UIConfig
from collider import Collider
from player import Player
from tile import Tile, TileManager
from window import Window


class Level:
    levels: dict[str, dict[str, ...]] = {}  # all existing levels
    """
    Level file structure:

    level folder (random value):
        tiles.json
        level_data.json:
            level name                (string)
            level music name          (string)
            level music start pos     (float)
            is level original         (boolean)
            max progress              (int)
            death count               (int)
            editor scroll             (tuple[int, int])
            bg color                  (string)
    """
    def __init__(self) -> None:
        self.path: str = ""
        self.name: str = ""
        self.music_name: str = ""
        self.music_start_pos: float = 0
        self.max_progress: float = 0
        self.death_count: int = 0
        self.bg_color: str = ""
        self.ground_color: str = ""

        self.tiles: list[Tile] = list()
        self.ground_tile: Tile | None = None
        self.ceil_tile: Tile | None = None
        self.__finish_x_pos: float = 0
        self.current_progress: float = 0

        self.triggers: list[Trigger] = list()
        self.__working_triggers: list[Trigger] = list()

        self.collider: Collider | None = None
        self.__player: Player | None = None

    @classmethod
    def load_levels(cls) -> None:
        """
        Loads level_data for every level that's in '../resources/data/level/' folder.
        return => {
            "level_path_1": {level_data.json},
            ...
            "level_path_N": {level_data.json},
        }
        """
        cls.levels.clear()
        path: pathlib.Path = pathlib.Path("../resources/data/levels/")
        obj: pathlib.Path | None = None
        try:
            for obj in path.iterdir():
                if not obj.is_dir():
                    continue

                with open(f"{str(obj)}/level_data.json", "r") as file:
                    cls.levels.setdefault(str(obj), json.load(file))  # path, data

        except FileNotFoundError:
            print(f"Level with path: '{str(obj)}' has no level_data file.")

    @classmethod
    def __decompress_tiles(cls, compressed_tiles: list[dict[str, int | dict[str, ...]]]) -> list[Tile]:
        tiles: list[Tile] = list()
        for compressed_tile_row in compressed_tiles:
            tile_row: list[Tile] = list()
            for i in range(compressed_tile_row.get("c", compressed_tile_row.get("count", 1))):
                json_tile = compressed_tile_row.get("t", compressed_tile_row.get("tile"))
                tile_row.append(TileManager.from_json(json_tile))
                json_tile.get("xy", json_tile.get("position"))[0] += Tile.SIZE

            tiles.extend(tile_row)

        return tiles

    @classmethod
    def get_objects(cls, path: pathlib.Path | str) -> dict[str, list]:
        try:
            with open(path + "/objects.json", "r") as file:
                return json.load(file)

        except FileNotFoundError:
            return dict()

    @classmethod
    def get_tiles(cls, path: pathlib.Path | str) -> list[Tile]:
        return cls.__decompress_tiles(cls.get_objects(path).get("tiles", list()))

    @classmethod
    def get_triggers(cls, path: pathlib.Path | str) -> list[Trigger]:
        triggers: list[Trigger] = list()

        # [TriggerManager.create_trigger(js_trigger) for js_trigger in cls.get_objects(path).get("triggers", [])]
        for json_trigger in cls.get_objects(path).get("triggers", []):
            triggers.append(TriggerManager.create_trigger(json_trigger))

        return triggers

    def set_player(self, player: Player) -> None:
        self.__player = player
        self.collider.player = self.__player
        self.ground_tile.rect.y = Tile.SIZE
        self.ceil_tile.rect.y = -Tile.SIZE * 64

    def load(self, path: str, player: Player) -> None:
        self.tiles.clear()
        self.triggers.clear()
        self.__working_triggers.clear()
        self.path = path
        try:
            with open(self.path + "/level_data.json", "r") as level_data_file:
                content: dict[str, ...] = json.load(level_data_file)
                self.name = content.get("name")
                self.music_name = content.get("music_name", "")
                self.music_start_pos = content.get("music_start_pos", 0)
                self.max_progress = content.get("max_progress", 0)
                self.death_count = content.get("death_count", 0)
                self.bg_color = content.get("bg_color", "#0000ff")
                self.ground_color = content.get("ground_color", "#000000")

        except FileNotFoundError:
            print(f"Could not find file '{self.path}/level_data.json'.")

        self.tiles = self.get_tiles(self.path)

        self.ground_tile = TileManager.create_tile(Tile.FOLLOW_TILE, [-Tile.SIZE, Tile.SIZE])
        self.ceil_tile = TileManager.create_tile(Tile.FOLLOW_TILE, [-Tile.SIZE, -Tile.SIZE * 64])
        self.tiles.append(self.ground_tile)
        self.tiles.append(self.ceil_tile)

        self.triggers = self.get_triggers(self.path)

        self.__finish_x_pos = self.get_finish_pos(self.tiles).x

        self.__player = player
        self.collider = Collider(self.__player, self)
        MusicManager.load(self.music_name)

    @classmethod
    def get_finish_pos(cls, tiles: list[Tile]) -> pygame.Vector2:
        if not tiles:
            return pygame.Vector2(Tile.SIZE * 8, 0)

        return pygame.Vector2(max(tiles, key=lambda tile: tile.rect.x).rect.topleft) + (Tile.SIZE * 8, 0)

    @classmethod
    def get_sorted_tiles(cls, tiles: list[Tile]) -> list[Tile]:
        # group tiles by Y coordinate
        tile_groups: dict[float, list[Tile]] = dict()
        for tile in tiles:
            if tile_groups.get(tile.rect.y, None) is None:
                tile_groups.setdefault(tile.rect.y, list())
            tile_groups.get(tile.rect.y).append(tile)

        # sorts tiles by X coordinate
        sorted_tiles: list[Tile] = list()
        for tile_group in tile_groups.values():
            sorted_tiles.extend(sorted(tile_group, key=lambda t: t.rect.x))

        return sorted_tiles

    @classmethod
    def __compress_tiles(cls, sorted_tiles: list[Tile]) -> list[dict[str, int | dict[str, ...]]]:
        if not sorted_tiles:
            return list()

        if len(sorted_tiles) == 1:
            return [{"t": TileManager.to_json(sorted_tiles[0])}]

        compressed_tiles: list[dict[str, int | dict[str, ...]]] = list()
        count = 1  # how many tiles in a row
        first_tile: Tile | None = None  # first tile in a row
        last_tile: Tile | None = None  # last tile in level
        for i in range(len(sorted_tiles) - 1):
            tile = sorted_tiles[i]
            next_tile = sorted_tiles[i + 1]

            if i + 1 == len(sorted_tiles) - 1:
                last_tile = next_tile

            # if tile in a row has next identical neighbor
            if tile.rect.y == next_tile.rect.y and tile.rect.right == next_tile.rect.x and tile.is_equal_to(next_tile):
                count += 1
                if first_tile is None:
                    first_tile = tile
                continue

            # if tile has no identical neighbors
            if first_tile is None:
                json_tile = {"t": TileManager.to_json(tile)}
                if count > 1:
                    json_tile.setdefault("c", count)
                compressed_tiles.append(json_tile)
                continue

            # if tile last in a row of identical neighbors
            json_tile = {"t": TileManager.to_json(first_tile)}
            if count > 1:
                json_tile.setdefault("c", count)
            compressed_tiles.append(json_tile)
            count = 1
            first_tile = None

        # if level ends with tiles in a row
        if first_tile is not None:
            json_tile = {"t": TileManager.to_json(first_tile)}
            if count > 1:
                json_tile.setdefault("c", count)
            compressed_tiles.append(json_tile)
        else:
            compressed_tiles.append({"t": TileManager.to_json(last_tile)})

        return compressed_tiles

    @classmethod
    def save_objects(cls, path: str, tiles: list[Tile], triggers: list[Trigger]) -> None:
        sorted_tiles = cls.get_sorted_tiles(tiles)
        compressed_tiles = cls.__compress_tiles(sorted_tiles)

        json_triggers = [trigger.to_json() for trigger in triggers]

        data = {
            "tiles": compressed_tiles,
            "triggers": json_triggers
        }

        with open(f"{path}/objects.json", "w") as file:
            json.dump(data, file)

    @classmethod
    def save_data(cls, path: str, level_name: str = None, is_original: bool = None,
                  max_progress: float = None, death_count: int = None, editor_scroll: pygame.Vector2 = None,
                  music_name: str = None, music_start_pos: float = None, bg_color: str = None,
                  ground_color: str = None) -> None:

        level = list(filter(lambda lvl: lvl[0] == path, cls.levels.items()))
        if not level:
            raise ValueError(f"Level with path '{path}' does not exist.")

        if level_name is None:
            level_name = level[0][1].get("level_name")
        level[0][1]["level_name"] = level_name

        if is_original is None:
            is_original = level[0][1].get("is_original")

        if max_progress is None:
            max_progress = level[0][1].get("max_progress", 0)
        level[0][1]["max_progress"] = max_progress

        if death_count is None:
            death_count = level[0][1].get("death_count", 0)
        level[0][1]["death_count"] = death_count

        if editor_scroll is None:
            editor_scroll = pygame.Vector2(level[0][1].get("editor_scroll", [0, 0]))
        editor_scroll = [editor_scroll.x, editor_scroll.y]
        level[0][1]["editor_scroll"] = editor_scroll

        if music_name is None:
            music_name = level[0][1].get("music_name", "")
        level[0][1]["music_name"] = music_name

        if music_start_pos is None:
            music_start_pos = level[0][1].get("music_start_pos", 0)
        level[0][1]["music_start_pos"] = music_start_pos

        if bg_color is None:
            bg_color = level[0][1].get("bg_color", "#0000ff")
        level[0][1]["bg_color"] = bg_color

        if ground_color is None:
            ground_color = level[0][1].get("ground_color", "#000000")
        level[0][1]["ground_color"] = ground_color

        with open(path + "/level_data.json", "w") as level_data_file:
            content: dict[str, ...] = {
                "level_name": level_name,
                "music_name": music_name,
                "music_start_pos": music_start_pos,
                "is_original": is_original,
                "max_progress": max_progress,
                "death_count": death_count,
                "editor_scroll": editor_scroll,
                "bg_color": bg_color,
                "ground_color": ground_color
            }
            json.dump(content, level_data_file, indent=4)

    @classmethod
    def create(cls) -> tuple[str, dict[str, str | bool | int]]:
        characters = "qwertyuiopasdfghjkllzxcvbnm1234567890="

        folder_name = "".join([random.choice(characters) for _ in range(18)])
        path = pathlib.Path(f"../resources/data/levels/{folder_name}")
        while path.exists():
            folder_name = "".join([random.choice(characters) for _ in range(18)])
            path = pathlib.Path(f"../resources/data/levels/{folder_name}")

        path.mkdir()
        with open(path / "level_data.json", "w") as level_data_file:
            level_data = {
                "level_name": "New Level",
                "music_name": MusicManager.music[0],
                "music_start_pos": 0,
                "is_original": False,
                "max_progress": 0,
                "death_count": 0,
                "editor_scroll": [0, 0],
                "bg_color": "#0000ff",
                "ground_color": "#000000"
            }
            json.dump(level_data, level_data_file, indent=4)

        cls.load_levels()

        return str(path), level_data

    @classmethod
    def delete(cls, path: str) -> None:
        shutil.rmtree(path)
        cls.load_levels()

    def reset_objects(self) -> None:
        for tile in self.tiles:
            tile.reset()

        self.__working_triggers.clear()
        for trigger in self.triggers:
            trigger.reset()

    def update(self, camera_offset: pygame.Vector2) -> None:
        self.__player.update()

        for tile in self.tiles:
            tile.update(player=self.__player, level=self)

        for trigger in self.triggers:
            if self.__player.rect.right >= trigger.position.x and trigger.remaining_time > 0 and trigger not in self.__working_triggers:
                self.__working_triggers.append(trigger)

        for trigger in self.__working_triggers:
            trigger.remaining_time -= Window.DELTA
            if trigger.group_id == -1:
                trigger.update(level=self)
                continue

            for tile in self.tiles:
                if not tile.group_ids:
                    continue

                if trigger.group_id in tile.group_ids:
                    trigger.update(tile=tile, level=self)
        self.__working_triggers = list(filter(lambda t: t.remaining_time > 0, self.__working_triggers))

        self.collider.update_collision(camera_offset)

        self.current_progress = round((self.__player.rect.x / self.__finish_x_pos) * 100, 1)
        if self.current_progress < 0:
            self.current_progress = 0

        if self.ground_tile.rect.y >= Tile.SIZE:
            self.ceil_tile.rect.y -= self.ground_tile.rect.y - Tile.SIZE
            self.ground_tile.rect.y = Tile.SIZE

    def draw(self, surface: pygame.Surface, camera_offset: pygame.Vector2) -> None:
        surface.fill(self.bg_color)
        self.__player.draw(surface, camera_offset)

        for tile in self.tiles:
            TileManager.draw_tile(tile, surface, camera_offset)
        # draw ground
        if self.ground_tile.rect.y - camera_offset.y < surface.height:
            pygame.draw.rect(surface, self.ground_color, [[0, self.ground_tile.rect.y - camera_offset.y], surface.size])
        # draw ceiling
        if self.ceil_tile.rect.bottom - camera_offset.y > 0:
            pygame.draw.rect(surface, self.ground_color, [0, 0, surface.width, self.ceil_tile.rect.bottom - camera_offset.y])

        # draw current progress
        render: pygame.Surface = UIConfig.fonts.get("jetbrains_16l").render(f"{self.current_progress}%", True, "#ffffff")
        surface.blit(render, [surface.width / 2 - render.width / 2, 0])
