import json
import pygame

from common import TILE_SIZE
from .tile import Tile


class TileManager:
    TILE: str = "tile"
    __TILE_DATA: dict[str, dict[str, ...]] = {}

    @classmethod
    def __load_tile_texture(cls, texture_name: str) -> pygame.Surface | None:
        if not texture_name:
            return None

        texture: pygame.Surface = pygame.image.load("../resources/textures/tiles/" + texture_name).convert_alpha()
        texture = pygame.transform.scale_by(texture, TILE_SIZE / texture.get_width())

        return texture

    @classmethod
    def __load_tile_hit_box(cls, tile: dict[str, ...]) -> tuple[int, ...]:
        hit_box: list[int] | None = tile.get("hit_box", None)
        if hit_box is None:
            hit_box = [0, 0, 1, 1]

        return tuple(map(lambda x: int(x * TILE_SIZE), hit_box))

    @classmethod
    def load_tile_data(cls) -> None:
        with open("../resources/data/tiles.json") as file:
            content: list[dict[str, ...]] = json.load(file)

            for tile in content:
                cls.__TILE_DATA.setdefault(
                    tile.get("id"),
                    {
                        "texture": cls.__load_tile_texture(tile.get("texture", "")),
                        "is_solid": tile.get("is_solid", False),
                        "hit_box": cls.__load_tile_hit_box(tile)
                    }
                )

    @classmethod
    def create_tile(cls, tile_id: str, position: pygame.typing.SequenceLike[int], *args, **kwargs) -> Tile | None:
        match tile_id:
            case cls.TILE:
                return Tile(cls.TILE, position, *args, **kwargs)

            case _:
                return None

    @classmethod
    def draw_tile(cls, tile: Tile, surface: pygame.Surface) -> None:
        tile_texture = cls.__TILE_DATA.get(tile.id).get("texture")
        if tile_texture is None:
            return

        surface.blit(tile_texture, tile.rect.topleft)
