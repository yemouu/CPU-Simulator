from .process import Process
from .scheduler import Scheduler


class FirstComeFirstServe(Scheduler):
    def __init__(self, processes: list[Process]):
        super().__init__(processes)

    def tick(self) -> bool:
        print(self._processes)

        self._ready_queue.extend(self.new_arrivals())
        print(self._ready_queue)

        if self._ready_queue:
            self._ready_queue[0].step()
            if self._ready_queue[0].is_done:
                self._ready_queue.popleft()

        self.increment_time()

        return bool(self._processes) or bool(self._ready_queue)
