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
                    cls.levels.setdefault(str(obj), json.load(file))

        except FileNotFoundError:
            print(f"File 'level_data.json' not found.'")

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

        try:
            with open(path + "/tiles.json", "r") as tiles_file:
                json_tiles: list[dict[str, ...]] = json.load(tiles_file)
                for json_tile in json_tiles:
                    self.tiles.append(TileManager.from_json(json_tile))

        except FileNotFoundError:
            pass

        self.tiles.append(Tile(Tile.FOLLOW_TILE, [0, 32]))

        self.__player = player
        self.collider = Collider(self.__player, self)

    def save_tiles(self, path: str) -> None:
        with open(path + "/tiles.json", "w") as tiles_file:
            json_tiles: list[dict[str, ...]] = list()
            for tile in self.tiles:
                json_tiles.append(TileManager.to_json(tile))

            json.dump(json_tiles, tiles_file, indent=2)

    def save_data(self, path: str) -> None:
        with open(path + "/level_data.json", "w") as level_data_file:
            content: dict[str, ...] = {
                "name": self.name,
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
