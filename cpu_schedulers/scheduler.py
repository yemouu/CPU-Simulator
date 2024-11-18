from collections import deque

from .process import Process, ProcessState
from .resource_manager import AvoidantResourceAllocationGraph, ResourceAllocationGraph, ResourceManager


class Scheduler:
    def __init__(self, processes: list[Process], resource_manager: ResourceManager):
        self._processes_done: list[Process] = []
        self._processes: list[Process] = processes
        self._ready_queue: deque[Process] = deque()
        self._wait_list: list[Process] = []

        self._idle_time: int = 0
        self._time: int = 0

        self._resource_manager = resource_manager
        for process in self._processes:
            process.resource_manager = resource_manager

    def calculate_cpu_usage(self) -> float:
        return float(self._time - self._idle_time) / float(self._time)

    def calculate_throughput(self) -> float:
        return float(len(self._processes_done)) / float(self._time)

    def calculate_average_queue_wait_time(self) -> float:
        combined_process_list = list(self._ready_queue) + self._processes_done + self._wait_list
        if len(combined_process_list) == 0:
            return 0.0

        sum: int = 0
        for process in combined_process_list:
            sum += process.wait_time

        return float(sum) / float(len(combined_process_list))

    def calculate_average_total_wait_time(self) -> float:
        combined_process_list = list(self._ready_queue) + self._processes_done + self._wait_list
        if len(combined_process_list) == 0:
            return 0.0

        sum: int = 0
        for process in combined_process_list:
            sum += process.wait_time + process.io_wait_time + process.resource_wait_time

        return float(sum) / float(len(combined_process_list))

    def calculate_average_turnaround_time(self) -> float:
        if len(self._processes_done) == 0:
            return 0.0

        sum: int = 0
        for process in self._processes_done:
            sum += process.completion_time - process.arrival_time

        return float(sum) / float(len(self._processes_done))

    def new_arrivals(self) -> list[Process]:
        new_arrivals = [process for process in self._processes if process.arrival_time == self._time]
        self._processes = [process for process in self._processes if process.arrival_time > self._time]

        return new_arrivals

    def increment_time(self) -> None:
        self._time += 1

    def increment_wait_time(self) -> None:
        for process in list(self._ready_queue)[1:]:
            process.wait()

        for process in self._wait_list:
            process.wait()

    def process_waiting_processes(self) -> None:
        for process in self._wait_list:
            match process.process_state:
                case ProcessState.DONE:
                    print(f"{process} is done executing")
                    self._processes_done.append(process)
                case ProcessState.READY:
                    print(f"{process} is ready")
                    self._ready_queue.append(process)
                case ProcessState.RESOURCE_WAIT | ProcessState.SLEEP:
                    pass
                case _:
                    raise NotImplementedError

        self._wait_list = [
            process
            for process in self._wait_list
            if process.process_state == ProcessState.RESOURCE_WAIT or process.process_state == ProcessState.SLEEP
        ]

    def deadlock_detection(self) -> None:
        """Detect a deadlock after it happens

        This requires using the ResourceAllocationGraph or a child
        class as your Resource Manager.
        """
        if isinstance(self._resource_manager, ResourceAllocationGraph):
            if self._resource_manager.detect_deadlock():
                print("Deadlock Detected!")
            else:
                print("No deadlock has occured.")

    def make_resource_claims(self, processes: list[Process]) -> None:
        if isinstance(self._resource_manager, AvoidantResourceAllocationGraph):
            for process in processes:
                self._resource_manager.add_process_claims(process.p_id, process.needed_resources())

    def revoke_resource_claims(self, process: Process) -> None:
        if isinstance(self._resource_manager, AvoidantResourceAllocationGraph):
            self._resource_manager.remove_process_claims(process.p_id)

    def print_metrics(self) -> None:
        print(
            "Metrics:",
            f"CPU Usage: {self.calculate_cpu_usage():.2f}",
            f"Throughput: {self.calculate_throughput():.2f}",
            f"Average Ready Queue Wait Time: {self.calculate_average_queue_wait_time():.2f}",
            f"Average Total Wait Time: {self.calculate_average_total_wait_time():.2f}",
            f"Average Turnaround Time: {self.calculate_average_turnaround_time():.2f}",
            sep="\n\t",
        )

    def tick(self) -> bool:
        raise NotImplementedError
