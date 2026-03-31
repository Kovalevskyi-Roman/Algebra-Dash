from window import Window
from game_loop import GameLoop

def main() -> None:
    window: Window = Window()
    game_loop: GameLoop = GameLoop(window)
    game_loop.run()

if __name__ == '__main__':
    main()
