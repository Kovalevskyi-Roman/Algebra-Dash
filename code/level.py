import json
import pathlib
import pygame

from collider import Collider
from player import Player
from tile import Tile, TileManager


class Level:
    levels: dict[str, dict[str, ...]] = {}
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
    def get_tiles(cls, path: str) -> list[Tile]:
        try:
            with open(path + "/tiles.json", "r") as tiles_file:
                tiles: list[Tile] = list()
                for json_tile in json.load(tiles_file):
                    tiles.append(TileManager.from_json(json_tile))

            return tiles

        except FileNotFoundError:
            return list()

    def load(self, path: str, player: Player) -> None:
        self.tiles.clear()
        self.name = ""
        self.collider = None
        self.__player = None
        try:
            with open(path + "/level_data.json", "r") as level_data_file:
                content: dict[str, ...] = json.load(level_data_file)
                self.name = content.get("name")

        except FileNotFoundError:
            print(f"Could not find file '{path}/level_data.json'.")

        self.tiles.extend(self.get_tiles(path))
        self.tiles.append(Tile(Tile.FOLLOW_TILE, [0, 32]))

        self.__player = player
        self.collider = Collider(self.__player, self)

    @classmethod
    def __sort_tiles(cls, tiles: list[Tile]) -> list[Tile]:
        tile_groups: dict[int, list[Tile]] = dict()
        for tile in tiles:
            if tile_groups.get(tile.rect.y, None) is None:
                tile_groups.setdefault(tile.rect.y, list())
            tile_groups.get(tile.rect.y).append(tile)
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
        count = 1
        first_tile: Tile | None = None
        last_tile: Tile | None = None
        for i in range(len(sorted_tiles) - 1):
            tile = sorted_tiles[i]
            next_tile = sorted_tiles[i + 1]

            if i + 1 == len(sorted_tiles) - 1:
                last_tile = next_tile

            # if tile in a row has next neighbor
            if tile.rect.y == next_tile.rect.y and tile.rect.x + Tile.SIZE == next_tile.rect.x and \
                    tile.id == next_tile.id:
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
    def save_data(cls, path: str, level_name: str) -> None:
        with open(path + "/level_data.json", "w") as level_data_file:
            content: dict[str, ...] = {
                "name": level_name,
            }
            json.dump(content, level_data_file, indent=4)

    @classmethod
    def get_path_from_name(cls, level_name: str) -> str:
        path = pathlib.Path("../resources/data/levels")
        for obj in path.iterdir():
            if not obj.is_dir():
                continue

            with open(str(obj) + "/level_data.json", "r") as file:
                if json.load(file).get("level_name") == level_name:
                    return str(obj)

        return ""

    @classmethod
    def delete(cls, path: str) -> None:
        ...

    def update(self, camera_offset: pygame.Vector2) -> None:
        for tile in self.tiles:
            tile.update(player=self.__player)

        self.collider.update_collision(camera_offset)

    def draw(self, surface: pygame.Surface, camera_offset: pygame.Vector2) -> None:
        for tile in self.tiles:
            TileManager.draw_tile(tile, surface, camera_offset)
