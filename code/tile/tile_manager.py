import json
import pygame

from .tile import Tile
from .hazard import Hazard
from .orb import Orb
from .trampoline import Trampoline
from .portal import Portal
from .speed_buster import SpeedBuster


class TileManager:
    TILE_DATA: dict[str, dict[str, ...]] = {
        Tile.FOLLOW_TILE: {
            "is_solid": True,
            "hitbox": (0, 0, Tile.SIZE, Tile.SIZE),
            "size": (Tile.SIZE, Tile.SIZE)
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

        return texture.convert_alpha()

    @classmethod
    def __load_tile_hitbox(cls, tile: dict[str, ...], size: tuple) -> tuple[int, ...]:
        hitbox: list[int] | None = tile.get("hitbox", None)
        if hitbox is None:
            hitbox = [0, 0, 1, 1]

        return hitbox[0] * size[0], hitbox[1] * size[1], hitbox[2] * size[0], hitbox[3] * size[1]

    @classmethod
    def load_tile_data(cls) -> None:
        with open("../resources/data/tiles.json") as file:
            content: list[dict[str, ...]] = json.load(file)

            for tile in content:
                size = tuple(map(lambda x: int(x * Tile.SIZE), tile.get("size", [1, 1])))
                texture = cls.__load_tile_texture(tile.get("texture", ""), size)
                hitbox = cls.__load_tile_hitbox(tile, size)

                cls.TILE_DATA.setdefault(
                    tile.get("id"),
                    {
                        "texture": texture,
                        "type": tile.get("type", Tile.TILE),
                        "size": size,
                        "hitbox": hitbox,
                        "is_solid": tile.get("is_solid", True),
                        "free_rotatable": tile.get("free_rotatable", False),
                        "properties": tile.get("properties", {})
                    }
                )

        Tile.TILE_MANAGER = cls

    @classmethod
    def create_tile(cls, tile_id: str, position: pygame.typing.SequenceLike[int] | pygame.Vector2, *args, **kwargs) -> Tile | None:
        size = cls.TILE_DATA.get(tile_id, {}).get("size", (Tile.SIZE, Tile.SIZE))
        hitbox = cls.TILE_DATA.get(tile_id, {}).get("hitbox", (0, 0, Tile.SIZE, Tile.SIZE))

        tile: Tile
        match cls.TILE_DATA.get(tile_id, {}).get("type"):
            case Tile.HAZARD:
                tile = Hazard(tile_id, position, size, hitbox, *args, **kwargs)

            case Tile.ORB:
                tile = Orb(tile_id, position, size, hitbox, *args, **kwargs)

            case Tile.TRAMPOLINE:
                tile = Trampoline(tile_id, position, size, hitbox, *args, **kwargs)

            case Tile.PORTAL:
                tile = Portal(tile_id, position, size, hitbox, *args, **kwargs)

            case Tile.SPEED_BUSTER:
                tile = SpeedBuster(tile_id, position, size, hitbox, *args, **kwargs)

            case _:
                tile = Tile(tile_id, position, size, hitbox, *args, **kwargs)

        tile.set_x_scale(kwargs.get("scale_x", 1))
        tile.set_y_scale(kwargs.get("scale_y", 1))
        tile.flip_by(kwargs.get("flip_x", False), kwargs.get("flip_y", False))
        cls.set_tile_rotation(tile, kwargs.get("rotation", 0))
        tile.color = kwargs.get("color", "#ffffff")
        tile.group_ids = kwargs.get("group_ids", None)

        return tile

    @classmethod
    def clone_tile(cls, tile: Tile) -> Tile:
        return cls.create_tile(
            tile.id,
            tile.rect.topleft,
            scale_x=tile.scale_x,
            scale_y=tile.scale_y,
            flip_x=tile.flip_x,
            flip_y=tile.flip_y,
            rotation=tile.rotation,
            group_ids=tile.group_ids
        )

    @classmethod
    def set_tile_rotation(cls, tile: Tile, rotation: float) -> None:
        if not cls.TILE_DATA.get(tile.id, {}).get("free_rotatable", False):
            while tile.rotation != 0:
                tile.rotate_by_90_degrees(-90 if tile.rotation > 0 else 90)

            while tile.rotation // 90 != rotation // 90:
                tile.rotate_by_90_degrees(90 if rotation > 0 else -90)

            return

        tile.rotation = rotation

    @classmethod
    def from_json(cls, json_tile: dict[str, ...]) -> Tile:
        if json_tile is None:
            raise ValueError("Could not create Tile from JSON because JSON is None.")

        tile_id: str = json_tile.get("id")
        tile_position: list | tuple = json_tile.get("xy", json_tile.get("position"))
        scale_x: float = json_tile.get("sx", json_tile.get("scale_x", 1))
        scale_y: float = json_tile.get("sy", json_tile.get("scale_y", 1))
        flip_x: bool = json_tile.get("fx", json_tile.get("flip_x", False))
        flip_y: bool = json_tile.get("fy", json_tile.get("flip_y", False))
        rotation: int = json_tile.get("rot", json_tile.get("rotation", 0))
        color: str = json_tile.get("c", "#ffffff")
        group_ids: list[int] | None = json_tile.get("gIds", None)

        return cls.create_tile(tile_id, tile_position, scale_x=scale_x, scale_y=scale_y,
                               flip_x=flip_x, flip_y=flip_y, rotation=rotation, color=color, group_ids=group_ids)

    @classmethod
    def to_json(cls, tile: Tile) -> dict:
        if tile is None:
            raise ValueError("Could not convert tile to JSON because tile is None.")

        # without scaling tiles back to 1 their position corrupts
        tile_scale_x = tile.scale_x
        tile_scale_y = tile.scale_y
        tile.set_x_scale(1)
        tile.set_y_scale(1)

        json_tile: dict[str, ...] = {
            "id": tile.id,
            "xy": [round(tile.rect.x, 2), round(tile.rect.y, 2)]
        }
        if tile_scale_x != 1:
            json_tile.setdefault("sx", tile_scale_x)
        if tile_scale_y != 1:
            json_tile.setdefault("sy", tile_scale_y)
        if tile.flip_x or tile.flip_y:
            json_tile.setdefault("fx", tile.flip_x)
        if tile.flip_y:
            json_tile.setdefault("fy", tile.flip_y)
        if tile.rotation:
            json_tile.setdefault("rot", tile.rotation)
        if tile.color != "#ffffff":
            json_tile.setdefault("c", tile.color)
        if tile.group_ids:
            json_tile.setdefault("gIds", tile.group_ids)

        return json_tile

    @classmethod
    def draw_tile_hitbox(cls, tile: Tile, surface: pygame.Surface, camera_offset: pygame.Vector2) -> None:
        # rect = pygame.Rect(tile.rect.topleft - camera_offset, tile.rect.size)
        hitbox_rect = pygame.FRect(tile.rect.topleft + (tile.hitbox.topleft - camera_offset), tile.hitbox.size)

        if hitbox_rect.right < 0 or hitbox_rect.x > surface.get_width() or \
                hitbox_rect.bottom < 0 or hitbox_rect.y > surface.get_height():
            return

        # pygame.draw.rect(surface, "#0000ff", rect, width=1)
        pygame.draw.rect(surface, "#ff0000", hitbox_rect, width=1)

    @classmethod
    def draw_tile(cls, tile: Tile, surface: pygame.Surface, camera_offset: pygame.Vector2) -> bool:
        """return True if the tile was drawn"""
        tile_texture: pygame.Surface | None = cls.TILE_DATA.get(tile.id, {}).get("texture", None)
        if tile_texture is None:
            return False

        tile_pos: pygame.Vector2 = pygame.Vector2(tile.rect.topleft - camera_offset)
        if tile_pos.x + tile.rect.width < 0 or tile_pos.x > surface.get_width() or \
                tile_pos.y + tile.rect.height < 0 or tile_pos.y > surface.get_height():
            return False

        if tile.color != "#ffffff":
            tile_texture = tile_texture.copy()
            tile_texture.fill(tile.color, special_flags=pygame.BLEND_MULT)

        if tile.flip_x or tile.flip_y:
            tile_texture = pygame.transform.flip(tile_texture, tile.flip_x, tile.flip_y)
        if tile.rotation:
            tile_texture = pygame.transform.rotate(tile_texture, tile.rotation)
        if tile.scale_x != 1 or tile.scale_y != 1:
            tile_texture = pygame.transform.scale(tile_texture, tile.rect.size)

        tile_texture_pos = tile.rect.center - pygame.Vector2(tile_texture.size) * 0.5
        surface.blit(tile_texture, tile_texture_pos - camera_offset)
        return True
