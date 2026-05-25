import pygame


class Tile:
    SIZE: int = 32

    TILE: str = "tile"
    FOLLOW_TILE: str = "follow_tile"
    SPIKE: str = "spike"

    YELLOW_ORB: str = "yellow_orb"
    PURPLE_ORB: str = "purple_orb"
    ORANGE_ORB: str = "orange_orb"
    BLACK_ORB: str = "black_orb"
    BLUE_ORB: str = "blue_orb"
    GREEN_ORB: str = "green_orb"

    YELLOW_TRAMPOLINE: str = "yellow_trampoline"
    PURPLE_TRAMPOLINE: str = "purple_trampoline"
    ORANGE_TRAMPOLINE: str = "orange_trampoline"
    BLUE_TRAMPOLINE: str = "blue_trampoline"

    BLUE_PORTAL: str = "blue_portal"
    YELLOW_PORTAL: str = "yellow_portal"
    CUBE_PORTAL: str = "cube_portal"
    SHIP_PORTAL: str = "ship_portal"
    BALL_PORTAL: str = "ball_portal"
    WAVE_PORTAL: str = "wave_portal"

    X1_SPEED_BUSTER: str = "x1_speed_buster"
    X2_SPEED_BUSTER: str = "x2_speed_buster"
    X3_SPEED_BUSTER: str = "x3_speed_buster"
    X4_SPEED_BUSTER: str = "x4_speed_buster"

    def __init__(self, id_: str, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        self.id = id_
        self.rect: pygame.FRect = pygame.FRect(position, size)
        self.hitbox: pygame.FRect = pygame.FRect(*hitbox)
        self.scale: float = 1.0
        self.flip_x: bool = False
        self.flip_y: bool = False
        self.rotation: int = 0

    def scale_to_factor(self, scale: float) -> None:
        # resets scale
        self.rect = self.rect.scale_by(1 / self.scale, 1 / self.scale)
        self.hitbox.x /= self.scale
        self.hitbox.y /= self.scale
        self.hitbox.width /= self.scale
        self.hitbox.height /= self.scale
        # sets new scale
        self.scale = round(scale, 2)
        self.rect = self.rect.scale_by(self.scale, self.scale)
        self.hitbox.x *= self.scale
        self.hitbox.y *= self.scale
        self.hitbox.width *= self.scale
        self.hitbox.height *= self.scale

    def flip_by(self, flip_x: bool, flip_y: bool) -> None:
        if self.flip_x != flip_x:
            self.hitbox.x = self.rect.width - self.hitbox.width - self.hitbox.x

        if self.flip_y != flip_y:
            self.hitbox.y = self.rect.height - self.hitbox.height - self.hitbox.y

        self.flip_x = flip_x
        self.flip_y = flip_y

    def rotate(self, angle: int) -> None:
        """Rotates rect only by 90 degrees"""
        self.rotation += angle
        if abs(self.rotation) == 360:
            self.rotation = 0

        if not angle:
            return

        self.rect.width, self.rect.height = self.rect.height, self.rect.width
        self.hitbox.width, self.hitbox.height = self.hitbox.height, self.hitbox.width
        self.hitbox.x, self.hitbox.y = self.hitbox.y, self.hitbox.x

    def update(self, *args, **kwargs) -> None:
        if self.id == self.FOLLOW_TILE:
            self.rect.x = kwargs.get("player").rect.x

    def on_player_collide(self, *args, **kwargs) -> None:
        ...
