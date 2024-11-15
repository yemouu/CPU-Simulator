class Process:
    def __init__(self, arrival_time: int, duration: int, name: str | None = None):
        self._arrival_time: int = arrival_time
        self._name: str = name
        self._time_left: int = duration

        self._done: bool = False

        if self._time_left < 1:
            raise ValueError("Duration is less than 1")

    def __str__(self):
        return f"Process {self._name}" if self._name else super().__str__

    @property
    def arrival_time(self) -> int:
        return self._arrival_time

    @property
    def is_done(self) -> bool:
        return self._done

    @property
    def time_left(self) -> int:
        return self._time_left

    def step(self) -> None:
        if self.is_done:
            return

        self._time_left -= 1

        if self.time_left == 0:
            self._done = True
