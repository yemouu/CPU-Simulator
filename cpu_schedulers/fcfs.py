from .process import Process, processes_str
from .scheduler import Scheduler


class FirstComeFirstServe(Scheduler):
    def __init__(self, processes: list[Process]):
        super().__init__(processes)

    def tick(self) -> bool:
        new_arrivals = list(self.new_arrivals())
        print(f"New Processes: {processes_str(new_arrivals)}")

        self._ready_queue.extend(new_arrivals)
        print(f"Ready Queue: {processes_str(self._ready_queue)}")

        self.increment_wait_time()

        if self._ready_queue:
            self._ready_queue[0].step(self._time)
            if self._ready_queue[0].is_done:
                print(f"{self._ready_queue[0]} is done executing")
                self._processes_done.append(self._ready_queue.popleft())

        self.increment_time()

        print(
            "Metrics:",
            f"CPU Usage: {self.calculate_cpu_usage():.2f}",
            f"Throughput: {self.calculate_throughput():.2f}",
            f"Average Wait Time: {self.calculate_average_wait_time():.2f}",
            f"Average Turnaround Time: {self.calculate_average_turnaround_time():.2f}",
            sep="\n\t",
        )

        print(f"Completed Processes: {processes_str(self._processes_done)}")

        return bool(self._processes) or bool(self._ready_queue)
