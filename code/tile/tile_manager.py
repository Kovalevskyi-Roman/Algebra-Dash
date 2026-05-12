import json
import pygame

from .tile import Tile
from .spike import Spike
from .orb import YellowOrb, BlueOrb
from .portal import BluePortal, YellowPortal, CubePortal, ShipPortal, BallPortal
from .speed_buster import X1SpeedBuster, X2SpeedBuster, X3SpeedBuster, X4SpeedBuster


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

        return texture

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
                        "is_solid": tile.get("is_solid", True),
                        "size": size,
                        "hitbox": hitbox
                    }
                )

            # print(*cls.TILE_DATA.items(), sep="\n")

    @classmethod
    def create_tile(cls, tile_id: str, position: pygame.typing.SequenceLike[int] | pygame.Vector2, *args, **kwargs) -> Tile | None:
        size = cls.TILE_DATA.get(tile_id, {}).get("size", (Tile.SIZE, Tile.SIZE))
        hitbox = cls.TILE_DATA.get(tile_id, {}).get("hitbox", (0, 0, Tile.SIZE, Tile.SIZE))

        tile: Tile
        match tile_id:
            case Tile.TILE:
                tile = Tile(Tile.TILE, position, size, hitbox, *args, **kwargs)

            case Tile.SPIKE:
                tile = Spike(position, size, hitbox, *args, **kwargs)

            case Tile.YELLOW_ORB:
                tile = YellowOrb(position, size, hitbox, *args, **kwargs)

            case Tile.BLUE_ORB:
                tile = BlueOrb(position, size, hitbox, *args, **kwargs)

            case Tile.BLUE_PORTAL:
                tile = BluePortal(position, size, hitbox, *args, **kwargs)

            case Tile.YELLOW_PORTAL:
                tile = YellowPortal(position, size, hitbox, *args, **kwargs)

            case Tile.CUBE_PORTAL:
                tile = CubePortal(position, size, hitbox, *args, **kwargs)

            case Tile.SHIP_PORTAL:
                tile = ShipPortal(position, size, hitbox, *args, **kwargs)

            case Tile.BALL_PORTAL:
                tile = BallPortal(position, size, hitbox, *args, **kwargs)

            case Tile.X1_SPEED_BUSTER:
                tile = X1SpeedBuster(position, size, hitbox, *args, **kwargs)

            case Tile.X2_SPEED_BUSTER:
                tile = X2SpeedBuster(position, size, hitbox, *args, **kwargs)

            case Tile.X3_SPEED_BUSTER:
                tile = X3SpeedBuster(position, size, hitbox, *args, **kwargs)

            case Tile.X4_SPEED_BUSTER:
                tile = X4SpeedBuster(position, size, hitbox, *args, **kwargs)

            case _:
                tile = Tile(tile_id, position, size, hitbox, *args, **kwargs)

        tile.scale_to_factor(kwargs.get("scale", 1))
        tile.flip_by(kwargs.get("flip_x", False), kwargs.get("flip_y", False))
        return tile

    @classmethod
    def from_json(cls, json_tile: dict[str, ...]) -> Tile:
        if json_tile is None:
            raise ValueError("Could not create Tile from JSON because JSON is None.")

        tile_id: str = json_tile.get("id")
        tile_position: list | tuple = json_tile.get("position")
        scale: float = json_tile.get("scale", 1.0)
        flip_x: bool = json_tile.get("flip_x", False)
        flip_y: bool = json_tile.get("flip_y", False)

        return cls.create_tile(tile_id, tile_position, scale=scale, flip_x=flip_x, flip_y=flip_y)

    @classmethod
    def to_json(cls, tile: Tile) -> dict:
        if tile is None:
            raise ValueError("Could not convert tile to JSON because tile is None.")

        # if you're not scaling tiles back to 1 their position corrupts
        tile_scale = tile.scale
        tile.scale_to_factor(1)

        return {
            "id": tile.id,
            "position": [tile.rect.x, tile.rect.y],
            "flip_x": tile.flip_x,
            "flip_y": tile.flip_y,
            "scale": tile_scale
        }

    @classmethod
    def draw_tile_hitbox(cls, tile: Tile, surface: pygame.Surface, camera_offset: pygame.Vector2) -> None:
        hitbox_rect = pygame.FRect(tile.rect.topleft + (tile.hitbox.topleft - camera_offset), tile.hitbox.size)

        if hitbox_rect.right < 0 or hitbox_rect.x > surface.get_width() or \
                hitbox_rect.bottom < 0 or hitbox_rect.y > surface.get_height():
            return

        pygame.draw.rect(surface, "#ff0000", hitbox_rect, width=1)

    @classmethod
    def draw_tile(cls, tile: Tile, surface: pygame.Surface, camera_offset: pygame.Vector2) -> bool:
        """return True if the tile was drawn"""
        tile_texture: pygame.Surface | None = cls.TILE_DATA.get(tile.id, {}).get("texture", None)
        tile_pos: pygame.Vector2 = pygame.Vector2(tile.rect.topleft - camera_offset)
        if tile_texture is None:
            return False

        if tile_pos.x + tile.rect.width < 0 or tile_pos.x > surface.get_width() or \
                tile_pos.y + tile.rect.height < 0 or tile_pos.y > surface.get_height():
            return False

        if tile.flip_x or tile.flip_y:
            tile_texture = pygame.transform.flip(tile_texture, tile.flip_x, tile.flip_y)
        if tile.scale != 1:
            tile_texture = pygame.transform.scale_by(tile_texture, tile.scale)
        surface.blit(tile_texture, tile_pos)
        return True
