from collections.abc import Callable

from window import Window


class Timer:
    def __init__(self, time: float) -> None:
        self.time = time
        self.remaining_time = 0
        self.started: bool = False
        self.paused: bool = False

    def start(self) -> None:
        self.started = True
        self.remaining_time = self.time

    def pause(self) -> None:
        self.paused = True

    def unpause(self) -> None:
        self.paused = False

    def update(self, finish_func: Callable) -> None:
        if not self.paused and self.started:
            self.remaining_time -= Window.DELTA

            if self.remaining_time <= 0:
                finish_func()
                self.started = False
