import pygame

from window import Window
from player import Player
from tile import Tile, TileManager


class Collider:
    def __init__(self, player: Player, tiles: list[Tile]) -> None:
        self.player = player
        self.tiles = tiles

    def __get_collided_tiles(self, camera_offset: pygame.Vector2) -> tuple[Tile, ...]:
        collided_tiles: list[Tile] = list()

        for tile in self.tiles:
            # checks if tile is on screen
            if tile.rect.right - camera_offset.x < 0 or tile.rect.left - camera_offset.x > Window.SIZE[0] or \
                    tile.rect.bottom - camera_offset.y < 0 or tile.rect.top - camera_offset.y > Window.SIZE[1]:
                continue

            if self.player.rect.colliderect(tile.rect):
                collided_tiles.append(tile)

        return tuple(collided_tiles)

    def update_collision(self, camera_offset: pygame.Vector2) -> None:
        self.player.collision = {
            "top": False, "left": False, "bottom": False, "right": False
        }

        self.player.rect.x += self.player.velocity.x
        for tile in self.__get_collided_tiles(camera_offset):
            if self.player.velocity.x > 0:
                self.player.rect.right = tile.rect.left
                self.player.collision["right"] = TileManager.TILE_DATA.get(tile.id, {}).get("is_solid", False)

            elif self.player.velocity.x < 0:
                self.player.rect.left = tile.rect.right
                self.player.collision["left"] = TileManager.TILE_DATA.get(tile.id, {}).get("is_solid", False)

            tile.on_player_collide(self.player)
            self.player.velocity.x = 0

        self.player.rect.y += self.player.velocity.y
        for tile in self.__get_collided_tiles(camera_offset):
            if self.player.velocity.y > 0:
                self.player.rect.bottom = tile.rect.top
                self.player.collision["bottom"] = TileManager.TILE_DATA.get(tile.id, {}).get("is_solid", False)

            elif self.player.velocity.y < 0:
                self.player.rect.top = tile.rect.bottom
                self.player.collision["top"] = TileManager.TILE_DATA.get(tile.id, {}).get("is_solid", False)

            tile.on_player_collide(self.player)
            self.player.velocity.y = 0
