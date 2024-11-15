from .process import Process, processes_str
from .scheduler import Scheduler


class FirstComeFirstServe(Scheduler):
    def __init__(self, processes: list[Process]):
        super().__init__(processes)

    def tick(self) -> bool:
        new_arrivals = list(self.new_arrivals())
        print("New Processes: " + processes_str(new_arrivals))

        self._ready_queue.extend(new_arrivals)
        print("Ready Queue: " + processes_str(self._ready_queue))

        if self._ready_queue:
            self._ready_queue[0].step()
            if self._ready_queue[0].is_done:
                self._ready_queue.popleft()

        self.increment_time()

        return bool(self._processes) or bool(self._ready_queue)
