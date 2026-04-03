from window import Window
from game_loop import GameLoop
from tile import TileManager
from game_state import GameStateManager

def main() -> None:
    window: Window = Window()
    TileManager.load_tile_data()
    game_state_manager: GameStateManager = GameStateManager()
    game_loop: GameLoop = GameLoop(window, game_state_manager)
    game_loop.run()

if __name__ == '__main__':
    main()
