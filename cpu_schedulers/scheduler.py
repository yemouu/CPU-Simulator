from collections import deque

from .process import Process


class Scheduler:
    def __init__(self, processes: list[Process]):
        self._processes: list[Process] = processes
        self._ready_queue: deque[Process] = deque()
        self._time: int = 0

    def new_arrivals(self) -> list[Process]:
        new = list(
            filter(
                lambda process: process.arrival_time == self._time,
                self._processes,
            )
        )

        self._processes = list(
            filter(
                lambda process: process.arrival_time > self._time,
                self._processes,
            ),
        )

        return new

    def increment_time(self, amount: int = 1) -> None:
        self._time += amount

    def tick(self) -> bool:
        pass
