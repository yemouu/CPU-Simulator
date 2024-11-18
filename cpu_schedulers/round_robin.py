from typing import override

from .process import Process, ProcessState, processes_str
from .resource_manager import ResourceManager
from .scheduler import Scheduler


class RoundRobin(Scheduler):
    def __init__(self, processes: list[Process], resource_manager: ResourceManager, time_quantum: int) -> None:
        super().__init__(processes, resource_manager)
        self._time_quantum = time_quantum
        self._time_quantum_left = time_quantum

        if self._time_quantum < 1:
            raise ValueError("Time Quantum is less than one")

    @override
    def tick(self) -> bool:
        print(f"\nNew Tick ({self._time})\n")
        print(f"Time Quantum: {self._time_quantum}")
        print(f"Time Quantum Left: {self._time_quantum_left}")

        self.deadlock_detection()

        new_arrivals = self.new_arrivals()
        print(f"New Processes: {processes_str(new_arrivals)}")
        self.make_resource_claims(new_arrivals)
        self._ready_queue.extend(new_arrivals)

        if self._time_quantum_left == 0:
            print("Time Quantum reached 0, placing process at the back of the queue")
            if self._ready_queue:
                self._ready_queue.append(self._ready_queue.popleft())
            self._time_quantum_left = self._time_quantum
            print(f"Time Quantum Left: {self._time_quantum_left}")

        print(f"Ready Queue: {processes_str(self._ready_queue)}")
        print(f"Wait List: {processes_str(self._wait_list)}")

        self.increment_wait_time()

        tick_time_quantum: bool = False
        if self._ready_queue:
            process_state: ProcessState = self._ready_queue[0].step(self._time)
            match process_state:
                case ProcessState.DONE:
                    print(f"{self._ready_queue[0]} is done executing")
                    self.revoke_resource_claims(self._ready_queue[0])
                    self._processes_done.append(self._ready_queue.popleft())
                    self._time_quantum_left = self._time_quantum
                    print(f"Time Quantum Left: {self._time_quantum_left}")
                case ProcessState.READY:
                    tick_time_quantum = True
                case ProcessState.RESOURCE_WAIT:
                    print(f"{self._ready_queue[0]} is waiting on a resource")
                    self._wait_list.append(self._ready_queue.popleft())
                    self._time_quantum_left = self._time_quantum
                    print(f"Time Quantum Left: {self._time_quantum_left}")
                case ProcessState.SLEEP:
                    print(f"{self._ready_queue[0]} is sleeping")
                    self._wait_list.append(self._ready_queue.popleft())
                    self._time_quantum_left = self._time_quantum
                    print(f"Time Quantum Left: {self._time_quantum_left}")
                case _:
                    raise NotImplementedError
        else:
            self._idle_time += 1

        self.process_waiting_processes()
        self.increment_time()
        self._time_quantum_left = self._time_quantum_left - 1 if tick_time_quantum else self._time_quantum_left
        self.print_metrics()
        print(f"\tTime Quantum Left: {self._time_quantum_left}")

        print(f"Completed Processes: {processes_str(self._processes_done)}")
        print(f"End Tick Ready Queue: {processes_str(self._ready_queue)}")
        print(f"End Tick Wait List: {processes_str(self._wait_list)}")

        return bool(self._processes) or bool(self._ready_queue) or bool(self._wait_list)
