import pygame

from tile import Tile
from .game_mode import GameMode


class WaveMode(GameMode):
    def __init__(self, player: "Player", texture_path: str, texture_size: tuple[int, int] | None = None) -> None:
        super().__init__(player, texture_path, texture_size)
        self.hitbox = pygame.Rect(10, 10, Tile.SIZE - 18, Tile.SIZE - 18)
        self.__rotation: float = 0
        self.__old_velocity: pygame.Vector2 = pygame.Vector2(0, 0)
        self.__trail_points: list[pygame.Vector2] = list()

    def update(self):
        self._player.velocity.y = self._player.move_speed * self._player.gravity_multiplier

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self._player.velocity.y *= -1

        if self.__old_velocity != self._player.velocity:
            self.__trail_points.append(pygame.Vector2(self._player.rect.center))
            self.__old_velocity = self._player.velocity.copy()

        if any(self._player.collision.values()):
            self._player.alive = False

    def draw(self, surface: pygame.Surface, camera_offset: pygame.math.Vector2) -> None:
        texture = pygame.transform.rotate(self.texture, self.__rotation)
        if self._player.velocity.y >= 0:
            texture = pygame.transform.flip(texture, False, True)

        if len(self.__trail_points) == 0:
            self.__trail_points.append(pygame.Vector2(self._player.rect.center))
            self.__trail_points.append(pygame.Vector2(self._player.rect.center))

        need_to_remove: list[pygame.Vector2] = list()
        next_point = pygame.Vector2(0, 0)
        for i in range(len(self.__trail_points) - 1):
            point = self.__trail_points[i]
            next_point = self.__trail_points[i + 1]

            if next_point.x - camera_offset.x < 0:
                need_to_remove.append(point)

            pygame.draw.line(surface, "#ff0000", point - camera_offset, next_point - camera_offset, width=5)

        pygame.draw.line(surface, "#ff0000", next_point - camera_offset, self._player.rect.center - camera_offset, width=5)
        for point in need_to_remove:
            self.__trail_points.remove(point)

        surface.blit(
            texture,
            self._player.rect.center - camera_offset - texture.get_rect().center
        )
