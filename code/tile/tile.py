import pygame


class Tile:
    TILE_MANAGER: "TileManager" = None
    SIZE: int = 32

    FOLLOW_TILE: str = "follow_tile"
    TILE: str = "tile"
    HAZARD: str = "hazard"
    ORB: str = "orb"
    TRAMPOLINE: str = "trampoline"
    PORTAL: str = "portal"
    SPEED_BUSTER: str = "speed_buster"

    def __init__(self, id_: str, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        self.id = id_
        self.rect: pygame.FRect = pygame.FRect(position, size)
        self.hitbox: pygame.FRect = pygame.FRect(*hitbox)
        self.scale_x: float = 1.0
        self.scale_y: float = 1.0
        self.flip_x: bool = False
        self.flip_y: bool = False
        self.rotation: float = 0
        self.color: str = "#ffffff"

    def set_x_scale(self, scale: float) -> None:
        self.rect = self.rect.scale_by(1 / self.scale_x, 1)
        self.hitbox.x /= self.scale_x
        self.hitbox.width /= self.scale_x

        self.scale_x = round(scale, 2)
        self.rect = self.rect.scale_by(self.scale_x, 1)
        self.hitbox.x *= self.scale_x
        self.hitbox.width *= self.scale_x

    def set_y_scale(self, scale: float) -> None:
        self.rect = self.rect.scale_by(1, 1 / self.scale_y)
        self.hitbox.y /= self.scale_y
        self.hitbox.height /= self.scale_y

        self.scale_y = round(scale, 2)
        self.rect = self.rect.scale_by(1, self.scale_y)
        self.hitbox.y *= self.scale_y
        self.hitbox.height *= self.scale_y

    def flip_by(self, flip_x: bool, flip_y: bool) -> None:
        if self.flip_x != flip_x:
            if abs(self.rotation) == 90:
                self.hitbox.y = self.rect.height - self.hitbox.height - self.hitbox.y
            else:
                self.hitbox.x = self.rect.width - self.hitbox.width - self.hitbox.x

        if self.flip_y != flip_y:
            if abs(self.rotation) == 90:
                self.hitbox.x = self.rect.width - self.hitbox.width - self.hitbox.x
            else:
                self.hitbox.y = self.rect.height - self.hitbox.height - self.hitbox.y

        self.flip_x = flip_x
        self.flip_y = flip_y

    def rotate_by_90_degrees(self, direction: int) -> None:
        self.rotation += direction
        if abs(self.rotation) == 360:
            self.rotation = 0

        if not direction:
            return

        # counterclockwise
        if direction > 0:
            self.hitbox.x, self.hitbox.y = self.hitbox.y, self.rect.width - self.hitbox.x - self.hitbox.width
        # clockwise
        elif direction < 0:
            self.hitbox.x, self.hitbox.y = self.rect.height - self.hitbox.y - self.hitbox.height, self.hitbox.x

        self.rect.width, self.rect.height = self.rect.height, self.rect.width
        self.hitbox.width, self.hitbox.height = self.hitbox.height, self.hitbox.width

    def is_equal_to(self, other_tile: "Tile") -> bool:
        if self.id != other_tile.id:
            return False

        if self.flip_x != other_tile.flip_x or self.flip_y != other_tile.flip_y:
            return False

        if self.scale_x != other_tile.scale_x or self.scale_y != other_tile.scale_y:
            return False

        if self.rotation != other_tile.rotation:
            return False

        if self.color != other_tile.color:
            return False

        return True

    def update(self, *args, **kwargs) -> None:
        if self.id == self.FOLLOW_TILE:
            self.rect.x = kwargs.get("player").rect.x

    def on_player_collide(self, *args, **kwargs) -> None:
        ...

    def reset(self) -> None:
        ...
