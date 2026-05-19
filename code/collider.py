import pygame

from window import Window
from player import Player
from tile import Tile, TileManager


class Collider:
    def __init__(self, player: Player, level: "Level") -> None:
        self.player = player
        self.level = level

    def __get_collided_tiles(self, camera_offset: pygame.Vector2, player_rect: pygame.FRect) -> tuple[Tile, ...]:
        collided_tiles: list[Tile] = list()

        for tile in self.level.tiles:
            # checks if tile is on screen
            if tile.rect.right - camera_offset.x < 0 or tile.rect.left - camera_offset.x > Window.SIZE[0] or \
                    tile.rect.bottom - camera_offset.y < 0 or tile.rect.top - camera_offset.y > Window.SIZE[1]:
                continue

            tile_hitbox_rect = pygame.FRect(
                tile.rect.x + tile.hitbox.x, tile.rect.y + tile.hitbox.y,
                tile.hitbox.width, tile.hitbox.height
            )

            if player_rect.colliderect(tile_hitbox_rect):
                collided_tiles.append(tile)

        return tuple(collided_tiles)

    def update_collision(self, camera_offset: pygame.Vector2) -> None:
        game_mode_hitbox: pygame.Rect = self.player.game_modes.get(self.player.current_game_mode).hitbox
        player_rect = pygame.FRect(pygame.Vector2(self.player.rect.topleft) + game_mode_hitbox.topleft, game_mode_hitbox.size)
        collided_with: set[Tile] = set()
        self.player.collision = {
            "top": False, "left": False, "bottom": False, "right": False
        }

        # checks collision on X axis
        player_rect.x += self.player.velocity.x
        collided_on_x = self.__get_collided_tiles(camera_offset, player_rect)
        collided_with.update(collided_on_x)
        for tile in collided_on_x:
            if not TileManager.TILE_DATA.get(tile.id).get("is_solid"):
                continue

            tile_hitbox_rect = pygame.FRect(
                tile.rect.x + tile.hitbox.x, tile.rect.y + tile.hitbox.y,
                tile.hitbox.width, tile.hitbox.height
            )

            if self.player.velocity.x > 0:
                player_rect.right = tile_hitbox_rect.left
                self.player.collision["right"] = TileManager.TILE_DATA.get(tile.id, {}).get("is_solid", False)

            elif self.player.velocity.x < 0:
                player_rect.left = tile_hitbox_rect.right
                self.player.collision["left"] = TileManager.TILE_DATA.get(tile.id, {}).get("is_solid", False)

        # checks collision on Y axis
        player_rect.y += self.player.velocity.y
        collided_on_y = self.__get_collided_tiles(camera_offset, player_rect)
        collided_with.update(collided_on_y)
        for tile in collided_on_y:
            if not TileManager.TILE_DATA.get(tile.id).get("is_solid"):
                continue

            tile_hitbox_rect = pygame.FRect(
                tile.rect.x + tile.hitbox.x, tile.rect.y + tile.hitbox.y,
                tile.hitbox.width, tile.hitbox.height
            )

            if self.player.velocity.y > 0:
                player_rect.bottom = tile_hitbox_rect.top
                self.player.collision["bottom"] = TileManager.TILE_DATA.get(tile.id, {}).get("is_solid", False)

            elif self.player.velocity.y < 0:
                player_rect.top = tile_hitbox_rect.bottom
                self.player.collision["top"] = TileManager.TILE_DATA.get(tile.id, {}).get("is_solid", False)

        # updates player position
        self.player.rect.topleft = pygame.Vector2(player_rect.topleft) - game_mode_hitbox.topleft

        if self.player.collision["left"] or self.player.collision["right"]:
            self.player.velocity.x = 0

        if self.player.collision["bottom"] or self.player.collision["top"]:
            self.player.velocity.y = 0
        for tile in collided_with:
            tile.on_player_collide(player=self.player, level=self.level)
