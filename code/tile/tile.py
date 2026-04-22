import pygame


class Tile:
    SIZE: int = 32
    TILE: str = "tile"
    FOLLOW_TILE: str = "follow_tile"
    SPIKE: str = "spike"

    def __init__(self, id_: str, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        self.id = id_
        self.rect: pygame.FRect = pygame.FRect(position, size)
        self.hitbox: pygame.FRect = pygame.FRect(*hitbox)
        self.flip_x: bool = False
        self.flip_y: bool = False
        self.scale: float = 1.0

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

    def update(self, *args, **kwargs) -> None:
        if self.id == self.FOLLOW_TILE:
            self.rect.x = kwargs.get("player").rect.x

    def on_player_collide(self, *args, **kwargs) -> None:
        ...
