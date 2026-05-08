import json
import pathlib
import shutil
import random
import pygame

from collider import Collider
from player import Player
from tile import Tile, TileManager


class Level:
    levels: dict[str, dict[str, ...]] = {}  # all existing levels
    """
    Level file structure:

    level folder (random hash value):
        tiles.json
        level_data.json:
            level display name   (string)
            level music name     (string)
            is level original    (boolean)
            max progress         (int)
            death count          (int)
    """
    def __init__(self) -> None:
        self.name: str = ""
        self.tiles: list[Tile] = list()
        self.collider: Collider | None = None
        self.__player: Player | None = None
        self.bg_color: str = ""
        self.ground_tile: Tile | None = None
        self.ceil_tile: Tile | None = None

    @classmethod
    def load_levels(cls) -> None:
        cls.levels.clear()
        path: pathlib.Path = pathlib.Path("../resources/data/levels/")
        try:
            for obj in path.iterdir():
                if not obj.is_dir():
                    continue

                with open(f"{str(obj)}/level_data.json", "r") as file:
                    cls.levels.setdefault(str(obj), json.load(file))  # path, data

        except FileNotFoundError:
            print(f"File 'level_data.json' not found.'")

    @classmethod
    def __decompress_tiles(cls, compressed_tiles: list[dict[str, int | dict[str, ...]]]) -> list[Tile]:
        tiles: list[Tile] = list()
        for compressed_tile_row in compressed_tiles:
            tile_row: list[Tile] = list()
            for i in range(compressed_tile_row.get("count")):
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

    def load(self, path: str, player: Player) -> None:
        self.tiles.clear()
        self.name = ""
        self.collider = None
        self.__player = None
        self.bg_color = "#272727"
        try:
            with open(path + "/level_data.json", "r") as level_data_file:
                content: dict[str, ...] = json.load(level_data_file)
                self.name = content.get("name")

        except FileNotFoundError:
            print(f"Could not find file '{path}/level_data.json'.")

        self.tiles.extend(self.get_tiles(path))
        self.ground_tile = TileManager.create_tile(Tile.FOLLOW_TILE, [0, Tile.SIZE])
        self.ceil_tile = TileManager.create_tile(Tile.FOLLOW_TILE, [0, -Tile.SIZE * 32])
        self.tiles.append(self.ground_tile)
        self.tiles.append(self.ceil_tile)

        self.__player = player
        self.collider = Collider(self.__player, self)

    @classmethod
    def __sort_tiles(cls, tiles: list[Tile]) -> list[Tile]:
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
            return [{"count": 1, "tile": TileManager.to_json(sorted_tiles[0])}]

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
                compressed_tiles.append({"count": count, "tile": TileManager.to_json(tile)})
                continue

            # if tile last in a row
            compressed_tiles.append({"count": count, "tile": TileManager.to_json(first_tile)})
            count = 1
            first_tile = None

        # if level ends with tiles in a row
        if first_tile is not None:
            compressed_tiles.append({"count": count, "tile": TileManager.to_json(first_tile)})
        else:
            compressed_tiles.append({"count": 1, "tile": TileManager.to_json(last_tile)})

        return compressed_tiles

    @classmethod
    def save_tiles(cls, path: str, tiles: list[Tile]) -> None:
        sorted_tiles = cls.__sort_tiles(tiles)
        compressed_tiles = cls.__compress_tiles(sorted_tiles)

        with open(f"{path}/tiles.json", "w") as file:
            json.dump(compressed_tiles, file)

    @classmethod
    def save_data(cls, path: str, level_name: str, is_original: bool) -> None:
        with open(path + "/level_data.json", "w") as level_data_file:
            content: dict[str, ...] = {
                "level_name": level_name,
                "is_original": is_original
            }
            json.dump(content, level_data_file, indent=4)

    @classmethod
    def get_path_from_level_name(cls, level_name: str) -> str:
        path = pathlib.Path("../resources/data/levels")
        for obj in path.iterdir():
            if not obj.is_dir():
                continue

            with open(str(obj) + "/level_data.json", "r") as file:
                if json.load(file).get("level_name") == level_name:
                    return str(obj)

        return ""

    @classmethod
    def create(cls) -> None:
        characters = "qwertyuiopasdfghjkllzxcvbnm1234567890="
        folder_name = "".join([random.choice(characters) for _ in range(18)])
        path = pathlib.Path(f"../resources/data/levels/{folder_name}")
        while path.exists():
            folder_name = "".join([random.choice(characters) for _ in range(18)])
            path = pathlib.Path(f"../resources/data/levels/{folder_name}")

        path.mkdir()
        with open(path / "level_data.json", "w") as level_data_file:
            json.dump(
                {"level_name": "New level", "is_original": True},
                level_data_file, indent=4)

        cls.load_levels()

    @classmethod
    def delete(cls, path: str) -> None:
        shutil.rmtree(path)
        cls.load_levels()

    def update(self, camera_offset: pygame.Vector2) -> None:
        for tile in self.tiles:
            tile.update(player=self.__player, level=self)

        self.collider.update_collision(camera_offset)

        if self.ground_tile.rect.y >= Tile.SIZE:
            self.ceil_tile.rect.y -= self.ground_tile.rect.y - Tile.SIZE
            self.ground_tile.rect.y = Tile.SIZE

    def draw(self, surface: pygame.Surface, camera_offset: pygame.Vector2) -> None:
        for tile in self.tiles:
            TileManager.draw_tile(tile, surface, camera_offset)

        # draw ground
        if self.ground_tile.rect.y - camera_offset.y < surface.height:
            pygame.draw.rect(surface, "#000000", [[0, self.ground_tile.rect.y - camera_offset.y], surface.size])

        # draw ceiling
        if self.ceil_tile.rect.bottom - camera_offset.y > 0:
            pygame.draw.rect(surface, "#000000", [0, 0, surface.width, self.ceil_tile.rect.bottom - camera_offset.y])
