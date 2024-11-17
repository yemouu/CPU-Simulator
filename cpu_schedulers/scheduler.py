from collections import deque

from .process import Process


class Scheduler:
    def __init__(self, processes: list[Process]):
        self._processes_done: list[Process] = []
        self._processes: list[Process] = processes
        self._ready_queue: deque[Process] = deque()

        self._idle_time: int = 0
        self._time: int = 0

    def calculate_cpu_usage(self) -> float:
        return float(self._time - self._idle_time) / float(self._time)

    def calculate_throughput(self) -> float:
        return float(len(self._processes_done)) / float(self._time)

    def calculate_average_wait_time(self) -> float:
        combined_process_list = list(self._ready_queue) + self._processes_done

        sum: int = 0
        for process in combined_process_list:
            sum += process.wait_time

        return float(sum) / float(len(combined_process_list))

    def calculate_average_turnaround_time(self) -> float:
        if len(self._processes_done) == 0:
            return 0

        sum: int = 0
        for process in self._processes_done:
            sum += process.completion_time - process.arrival_time

        return float(sum) / float(len(self._processes_done))

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

    def increment_wait_time(self) -> None:
        for process in list(self._ready_queue)[1:]:
            process.wait()

    def tick(self) -> bool:
        raise NotImplementedError
