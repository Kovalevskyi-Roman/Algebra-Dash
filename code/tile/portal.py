import pygame

from .tile import Tile


class Portal(Tile):
    def __init__(self, id_: str, position: pygame.typing.SequenceLike[int], size: pygame.typing.SequenceLike[int],
                 hitbox: pygame.typing.SequenceLike[int], *args, **kwargs) -> None:
        super().__init__(id_, position, size, hitbox, *args, **kwargs)
        self.__was_used: bool = False

    def on_player_collide(self, *args, **kwargs) -> None:
        if self.__was_used:
            return

        self.__was_used = True
        player = kwargs.get("player")
        level = kwargs.get("level")
        gravity = Tile.TILE_MANAGER.TILE_DATA.get(self.id, {}).get("properties", {}).get("gravity", None)
        game_mode = Tile.TILE_MANAGER.TILE_DATA.get(self.id, {}).get("properties", {}).get("game_mode", None)

        if gravity is not None:
            player.gravity_multiplier = abs(player.gravity_multiplier) * gravity

        if game_mode is not None:
            player.current_game_mode = player.get_game_mode_type(game_mode)

            if game_mode == "cube":
                level.ground_tile.rect.y = player.current_game_mode.ground_level
                level.ceil_tile.rect.y = player.current_game_mode.ceil_level
                return

            level.ground_tile.rect.y = self.rect.centery // Tile.SIZE * Tile.SIZE + Tile.SIZE * player.current_game_mode.ground_level
            level.ceil_tile.rect.y = self.rect.centery // Tile.SIZE * Tile.SIZE - Tile.SIZE * (player.current_game_mode.ceil_level + 1)

    def reset(self) -> None:
        super().reset()
        self.__was_used = False
