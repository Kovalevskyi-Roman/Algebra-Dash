import json
import pygame

from .tile import Tile


class TileManager:
    TILE_DATA: dict[str, dict[str, ...]] = {
        Tile.FOLLOW_TILE: {
            "is_solid": True,
            "hit_box": (0, 0, Tile.SIZE, Tile.SIZE)
        }
    }

    @classmethod
    def __load_tile_texture(cls, texture_name: str, texture_size: pygame.typing.SequenceLike[int] | None) -> pygame.Surface | None:
        if not texture_name:
            return None

        texture: pygame.Surface = pygame.image.load("../resources/textures/tiles/" + texture_name).convert_alpha()
        if texture_size is None:
            texture = pygame.transform.scale_by(texture, Tile.SIZE / texture.get_width())
        else:
            texture = pygame.transform.scale(texture, texture_size)

        return texture

    @classmethod
    def __load_tile_hit_box(cls, tile: dict[str, ...]) -> tuple[int, ...]:
        hit_box: list[int] | None = tile.get("hit_box", None)
        if hit_box is None:
            hit_box = [0, 0, 1, 1]

        return tuple(map(lambda x: int(x * Tile.SIZE), hit_box))

    @classmethod
    def load_tile_data(cls) -> None:
        with open("../resources/data/tiles.json") as file:
            content: list[dict[str, ...]] = json.load(file)

            for tile in content:
                cls.TILE_DATA.setdefault(
                    tile.get("id"),
                    {
                        "texture": cls.__load_tile_texture(tile.get("texture", ""), tile.get("texture_size", None)),
                        "is_solid": tile.get("is_solid", False),
                        "hit_box": cls.__load_tile_hit_box(tile)
                    }
                )

    @classmethod
    def create_tile(cls, tile_id: str, position: pygame.typing.SequenceLike[int], *args, **kwargs) -> Tile | None:
        match tile_id:
            case Tile.TILE:
                return Tile(Tile.TILE, position, *args, **kwargs)

            case _:
                return Tile(tile_id, position, *args, **kwargs)

    @classmethod
    def draw_tile(cls, tile: Tile, surface: pygame.Surface, camera_offset: pygame.Vector2) -> None:
        tile_texture: pygame.Surface | None = cls.TILE_DATA.get(tile.id, {}).get("texture", None)
        if tile_texture is None:
            return

        surface.blit(tile_texture, tile.rect.topleft - camera_offset)
