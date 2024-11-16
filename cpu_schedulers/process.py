class Process:
    _next_id: int = 0

    def __init__(self, arrival_time: int, duration: int):
        self._arrival_time: int = arrival_time
        self._time_left: int = duration

        self._done: bool = False
        self._wait_time: int = 0
        self._completion_time: int = 0

        self._id: int = Process._next_id
        Process._next_id += 1

        if self._time_left < 1:
            raise ValueError("Duration is less than 1")

    def __str__(self):
        return f"pid-{self._id}"

    @property
    def arrival_time(self) -> int:
        return self._arrival_time

    @property
    def completion_time(self) -> int:
        return self._completion_time

    @property
    def is_done(self) -> bool:
        return self._done

    @property
    def time_left(self) -> int:
        return self._time_left

    @property
    def wait_time(self) -> int:
        return self._wait_time

    def wait(self) -> int:
        self._wait_time += 1

    def step(self, current_system_time: int) -> None:
        if self.is_done:
            return

        self._time_left -= 1

        if self.time_left == 0:
            self._done = True
            self._completion_time = current_system_time


def processes_str(processes: list[Process], separator: str = ", ") -> str:
    return separator.join(str(process) for process in processes)
