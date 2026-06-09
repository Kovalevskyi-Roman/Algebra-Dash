import pygame

from tile import Tile
from .game_mode import GameMode


class WaveMode(GameMode):
    def __init__(self, player: "Player") -> None:
        super().__init__(player)
        self.load_texture("wave")

        self.hitbox = pygame.Rect(11, 11, Tile.SIZE - 22, Tile.SIZE - 22)
        self.rotation: float = 0
        self.__old_velocity: pygame.Vector2 = pygame.Vector2(0, 0)
        self.__trail_points: list[pygame.Vector2] = list()

    def dash(self) -> None:
        self._player.velocity = self._player.dash_direction * self._player.move_speed
        if self._player.dash_direction.angle > 0:
            self.rotation = self._player.dash_direction.angle - 45
        else:
            self.rotation = -self._player.dash_direction.angle - 45

    def update(self):
        if self.rotation:
            self.rotation = 0

        self._player.velocity.y = self._player.move_speed * self._player.gravity_multiplier

        if self._player.jump_action:
            self._player.velocity.y *= -1

        if self.__old_velocity.x != self._player.velocity.x or self.__old_velocity.y != self._player.velocity.y:
            self.__trail_points.append(pygame.Vector2(self._player.rect.center))
            self.__old_velocity = self._player.velocity.copy()

        if any(self._player.collision.values()):
            self._player.alive = False

    def draw(self, surface: pygame.Surface, camera_offset: pygame.math.Vector2) -> None:
        texture = pygame.transform.rotate(self.texture, self.rotation)
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

            pygame.draw.line(surface, self._player.second_color, point - camera_offset, next_point - camera_offset, width=6)

        pygame.draw.line(surface, self._player.second_color, next_point - camera_offset, self._player.rect.center - camera_offset, width=6)
        for point in need_to_remove:
            self.__trail_points.remove(point)

        surface.blit(
            texture,
            self._player.rect.center - camera_offset - texture.get_rect().center
        )
