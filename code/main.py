import pygame

from window import Window
from game_loop import GameLoop
from tile import TileManager
from game_state import GameStateManager
from ui import UIConfig

def main() -> None:
    pygame.init()

    window: Window = Window()
    TileManager.load_tile_data()
    game_state_manager: GameStateManager = GameStateManager()
    UIConfig.init()
    game_loop: GameLoop = GameLoop(window, game_state_manager)
    game_loop.run()

if __name__ == '__main__':
    main()
