import pygame

from window import Window
from game_loop import GameLoop
from tile import TileManager
from trigger import TriggerManager
from game_state import GameStateManager
from ui import UIConfig
from music_manager import MusicManager
from sfx_manager import SFXManager
from level import Level

def main() -> None:
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.init()

    window: Window = Window()

    UIConfig.init()
    TileManager.load_tile_data()
    TriggerManager.load_textures()
    MusicManager.init()
    SFXManager.init()
    Level.load_levels()

    game_state_manager: GameStateManager = GameStateManager()
    game_loop: GameLoop = GameLoop(window, game_state_manager)
    game_loop.run()

if __name__ == '__main__':
    main()
