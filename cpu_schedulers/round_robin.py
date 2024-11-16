from .process import Process, processes_str
from .scheduler import Scheduler


class RoundRobin(Scheduler):
    def __init__(self, processes: list[Process], time_quantum: int):
        super().__init__(processes)
        self._time_quantum = time_quantum
        self._time_quantum_left = time_quantum

        if self._time_quantum < 1:
            raise ValueError("Time Quantum is less than one")

    def tick(self) -> bool:
        print(f"Time Quantum: {self._time_quantum}")
        print(f"Time Quantum Left: {self._time_quantum_left}")

        new_arrivals = list(self.new_arrivals())
        print(f"New Processes: {processes_str(new_arrivals)}")

        self._ready_queue.extend(new_arrivals)

        if self._time_quantum_left == 0:
            print("Time Quantum reached 0, placing process at the back of the queue")
            self._ready_queue.append(self._ready_queue.popleft())
            self._time_quantum_left = self._time_quantum
            print(f"Time Quantum Left: {self._time_quantum_left}")

        print(f"Ready Queue: {processes_str(self._ready_queue)}")

        self.increment_wait_time()

        if self._ready_queue:
            self._ready_queue[0].step(self._time)
            if self._ready_queue[0].is_done:
                print(f"{self._ready_queue[0]} is done executing")
                self._processes_done.append(self._ready_queue.popleft())
                self._time_quantum_left = self._time_quantum
                print(f"Time Quantum Left: {self._time_quantum_left}")
        else:
            self._idle_time += 1

        self.increment_time()
        self._time_quantum_left -= 1

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
