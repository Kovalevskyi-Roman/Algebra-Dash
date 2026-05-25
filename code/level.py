import json
import pathlib
import shutil
import random
from pathlib import Path

import pygame

from ui import UIConfig
from collider import Collider
from player import Player
from tile import Tile, TileManager


class Level:
    levels: dict[str, dict[str, ...]] = {}  # all existing levels
    """
    Level file structure:

    level folder (random value):
        tiles.json
        level_data.json:
            level name           (string)
            level music name     (string)
            is level original    (boolean)
            max progress         (int)
            death count          (int)
            editor scroll        (tuple[int, int])
    """
    def __init__(self) -> None:
        self.name: str = ""
        self.path: str = ""
        self.tiles: list[Tile] = list()
        self.collider: Collider | None = None
        self.__player: Player | None = None
        self.bg_color: str = ""
        self.ground_tile: Tile | None = None
        self.ceil_tile: Tile | None = None
        self.__finish_x_pos: float = 0
        self.max_progress: float = 0
        self.current_progress: float = 0
        self.death_count: int = 0

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
            for i in range(compressed_tile_row.get("count", 1)):
                tile_row.append(
                    TileManager.from_json(compressed_tile_row.get("tile"))
                )
                compressed_tile_row.get("tile").get("position")[0] += Tile.SIZE

            tiles.extend(tile_row)

        return tiles

    @classmethod
    def get_tiles(cls, path: str) -> list[Tile]:
        try:
            with open(path + "/tiles.json", "r") as tiles_file:
                compressed_tiles: list[dict[str, int | dict[str, ...]]] = json.load(tiles_file)

            return cls.__decompress_tiles(compressed_tiles)
        except FileNotFoundError:
            return list()

    def set_player(self, player: Player) -> None:
        self.__player = player
        self.collider.player = self.__player
        self.ground_tile.rect.y = Tile.SIZE
        self.ceil_tile.rect.y = -Tile.SIZE * 32

    def load(self, path: str, player: Player) -> None:
        self.tiles.clear()
        self.name = ""
        self.path = path
        self.collider = None
        self.__player = None
        self.bg_color = "#0000ff"
        try:
            with open(self.path + "/level_data.json", "r") as level_data_file:
                content: dict[str, ...] = json.load(level_data_file)
                self.name = content.get("name")
                self.max_progress = content.get("max_progress", 0)
                self.death_count = content.get("death_count", 0)

        except FileNotFoundError:
            print(f"Could not find file '{self.path}/level_data.json'.")

        self.tiles.extend(self.get_tiles(self.path))
        self.ground_tile = TileManager.create_tile(Tile.FOLLOW_TILE, [0, Tile.SIZE])
        self.ceil_tile = TileManager.create_tile(Tile.FOLLOW_TILE, [0, -Tile.SIZE * 32])
        self.tiles.append(self.ground_tile)
        self.tiles.append(self.ceil_tile)
        self.__finish_x_pos = max(self.tiles, key=lambda tile: tile.rect.x).rect.x + Tile.SIZE * 8

        self.__player = player
        self.collider = Collider(self.__player, self)

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
            return [{"tile": TileManager.to_json(sorted_tiles[0])}]

        compressed_tiles: list[dict[str, int | dict[str, ...]]] = list()
        count = 1  # how many tiles in a row
        first_tile: Tile | None = None  # first tile in a row
        last_tile: Tile | None = None  # last tile in level
        for i in range(len(sorted_tiles) - 1):
            tile = sorted_tiles[i]
            next_tile = sorted_tiles[i + 1]

            if i + 1 == len(sorted_tiles) - 1:
                last_tile = next_tile

            # if tile in a row has next neighbor
            if tile.rect.y == next_tile.rect.y and tile.rect.x + Tile.SIZE == next_tile.rect.x and \
                    tile.id == next_tile.id and tile.flip_x == next_tile.flip_x and tile.flip_y == next_tile.flip_y and \
                    tile.scale == next_tile.scale:
                count += 1
                if first_tile is None:
                    first_tile = tile
                continue

            # if tile has no neighbors
            if first_tile is None:
                json_tile = {"tile": TileManager.to_json(tile)}
                if count > 1:
                    json_tile.setdefault("count", count)
                compressed_tiles.append(json_tile)
                continue

            # if tile last in a row
            json_tile = {"tile": TileManager.to_json(first_tile)}
            if count > 1:
                json_tile.setdefault("count", count)
            compressed_tiles.append(json_tile)
            count = 1
            first_tile = None

        # if level ends with tiles in a row
        if first_tile is not None:
            json_tile = {"tile": TileManager.to_json(first_tile)}
            if count > 1:
                json_tile.setdefault("count", count)
            compressed_tiles.append(json_tile)
        else:
            compressed_tiles.append({"tile": TileManager.to_json(last_tile)})

        return compressed_tiles

    @classmethod
    def save_tiles(cls, path: str, tiles: list[Tile]) -> None:
        sorted_tiles = cls.get_sorted_tiles(tiles)
        compressed_tiles = cls.__compress_tiles(sorted_tiles)

        with open(f"{path}/tiles.json", "w") as file:
            json.dump(compressed_tiles, file)

    @classmethod
    def save_data(cls, path: str, level_name: str = None, is_original: bool = None,
                  max_progress: float = None, death_count: int = None, editor_scroll: pygame.Vector2 = None) -> None:

        level = list(filter(lambda l: l[0] == path, cls.levels.items()))
        if not level:
            raise ValueError(f"Level with path '{path}' does not exist.")

        if level_name is None:
            level_name = level[0][1].get("level_name")
        else:
            level[0][1]["level_name"] = level_name
        if is_original is None:
            is_original = level[0][1].get("is_original")
        if max_progress is None:
            max_progress = level[0][1].get("max_progress", 0)
        else:
            level[0][1]["max_progress"] = max_progress
        if death_count is None:
            death_count = level[0][1].get("death_count", 0)
        else:
            level[0][1]["death_count"] = death_count
        if editor_scroll is None:
            editor_scroll = level[0][1].get("editor_scroll", [0, 0])
        else:
            editor_scroll = [editor_scroll.x, editor_scroll.y]
            level[0][1]["editor_scroll"] = editor_scroll

        with open(path + "/level_data.json", "w") as level_data_file:
            content: dict[str, ...] = {
                "level_name": level_name,
                "is_original": is_original,
                "max_progress": max_progress,
                "death_count": death_count,
                "editor_scroll": editor_scroll
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
                "is_original": False,
                "max_progress": 0,
                "death_count": 0,
                "editor_scroll": [0, 0]
            }
            json.dump(level_data, level_data_file, indent=4)

        cls.load_levels()

        return str(path), level_data

    @classmethod
    def delete(cls, path: str) -> None:
        shutil.rmtree(path)
        cls.load_levels()

    def update(self, camera_offset: pygame.Vector2) -> None:
        self.__player.update()

        for tile in self.tiles:
            tile.update(player=self.__player, level=self)

        self.collider.update_collision(camera_offset)

        self.current_progress = round((self.__player.rect.x / self.__finish_x_pos) * 100, 1)

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
            pygame.draw.rect(surface, "#000000", [[0, self.ground_tile.rect.y - camera_offset.y], surface.size])
        # draw ceiling
        if self.ceil_tile.rect.bottom - camera_offset.y > 0:
            pygame.draw.rect(surface, "#000000", [0, 0, surface.width, self.ceil_tile.rect.bottom - camera_offset.y])

        # draw current progress
        render: pygame.Surface = UIConfig.fonts.get("jetbrains_16l").render(f"{self.current_progress}%", True, "#ffffff")
        surface.blit(render, [surface.width / 2 - render.width / 2, 0])
