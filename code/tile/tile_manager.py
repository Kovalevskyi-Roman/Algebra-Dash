import json
import pygame

from .tile import Tile
from .spike import Spike
from .orb import YellowOrb, PurpleOrb, OrangeOrb, BlackOrb, BlueOrb, GreenOrb, DashOrb, ReversedDashOrb
from .trampoline import YellowTrampoline, PurpleTrampoline, OrangeTrampoline, BlueTrampoline
from .portal import BluePortal, YellowPortal, CubePortal, ShipPortal, BallPortal, WavePortal
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
                        "size": size,
                        "hitbox": hitbox,
                        "is_solid": tile.get("is_solid", True),
                        "free_rotatable": tile.get("free_rotatable", False)
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

            case Tile.PURPLE_ORB:
                tile = PurpleOrb(position, size, hitbox, *args, **kwargs)

            case Tile.ORANGE_ORB:
                tile = OrangeOrb(position, size, hitbox, *args, **kwargs)

            case Tile.BLACK_ORB:
                tile = BlackOrb(position, size, hitbox, *args, **kwargs)

            case Tile.BLUE_ORB:
                tile = BlueOrb(position, size, hitbox, *args, **kwargs)

            case Tile.GREEN_ORB:
                tile = GreenOrb(position, size, hitbox, *args, **kwargs)

            case Tile.DASH_ORB:
                tile = DashOrb(position, size, hitbox, *args, **kwargs)

            case Tile.REVERSED_DASH_ORB:
                tile = ReversedDashOrb(position, size, hitbox, *args, **kwargs)

            case Tile.YELLOW_TRAMPOLINE:
                tile = YellowTrampoline(position, size, hitbox, *args, **kwargs)

            case Tile.PURPLE_TRAMPOLINE:
                tile = PurpleTrampoline(position, size, hitbox, *args, **kwargs)

            case Tile.ORANGE_TRAMPOLINE:
                tile = OrangeTrampoline(position, size, hitbox, *args, **kwargs)

            case Tile.BLUE_TRAMPOLINE:
                tile = BlueTrampoline(position, size, hitbox, *args, **kwargs)

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

            case Tile.WAVE_PORTAL:
                tile = WavePortal(position, size, hitbox, *args, **kwargs)

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

        rotation = kwargs.get("rotation", 0)
        if not cls.TILE_DATA.get(tile_id, {}).get("free_rotatable", False):
            while rotation != 0:
                tile.rotate_by_90_degrees(90 if rotation > 0 else -90)
                rotation -= 90 if rotation > 0 else -90
        else:
            tile.rotation = rotation

        return tile

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
        tile_position: list | tuple = json_tile.get("position")
        scale: float = json_tile.get("scale", 1.0)
        flip_x: bool = json_tile.get("flip_x", False)
        flip_y: bool = json_tile.get("flip_y", False)
        rotation: int = json_tile.get("rotation", 0)

        return cls.create_tile(tile_id, tile_position, scale=scale, flip_x=flip_x, flip_y=flip_y, rotation=rotation)

    @classmethod
    def to_json(cls, tile: Tile) -> dict:
        if tile is None:
            raise ValueError("Could not convert tile to JSON because tile is None.")

        # if you're not scaling tiles back to 1 their position corrupts
        tile_scale = tile.scale
        tile.scale_to_factor(1)
        json_tile: dict[str, ...] = {
            "id": tile.id,
            "position": [tile.rect.x, tile.rect.y]
        }
        if tile_scale != 1:
            json_tile.setdefault("scale", tile_scale)
        if tile.flip_x:
            json_tile.setdefault("flip_x", tile.flip_x)
        if tile.flip_y:
            json_tile.setdefault("flip_y", tile.flip_y)
        if tile.rotation:
            json_tile.setdefault("rotation", tile.rotation)

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

        if tile.flip_x or tile.flip_y:
            tile_texture = pygame.transform.flip(tile_texture, tile.flip_x, tile.flip_y)
        if tile.scale != 1:
            tile_texture = pygame.transform.scale_by(tile_texture, tile.scale)
        if tile.rotation:
            tile_texture = pygame.transform.rotate(tile_texture, tile.rotation)

        tile_texture_pos = tile.rect.center - pygame.Vector2(tile_texture.size) * 0.5
        surface.blit(tile_texture, tile_texture_pos - camera_offset)
        return True
