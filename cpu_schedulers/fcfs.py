from typing import override

from .process import Process, ProcessState, processes_str
from .resource_manager import ResourceManager
from .scheduler import Scheduler


class FirstComeFirstServe(Scheduler):
    def __init__(self, processes: list[Process], resource_manager: ResourceManager) -> None:
        super().__init__(processes, resource_manager)

    @override
    def tick(self) -> bool:
        print(f"\nNew Tick ({self._time})\n")

        self.deadlock_detection()

        new_arrivals = self.new_arrivals()
        print(f"New Processes: {processes_str(new_arrivals)}")

        self.make_resource_claims(new_arrivals)
        self._ready_queue.extend(new_arrivals)
        print(f"Ready Queue: {processes_str(self._ready_queue)}")
        print(f"Wait List: {processes_str(self._wait_list)}")

        self.increment_wait_time()

        if self._ready_queue:
            process_state: ProcessState = self._ready_queue[0].step(self._time)
            match process_state:
                case ProcessState.DONE:
                    print(f"{self._ready_queue[0]} is done executing")
                    self.revoke_resource_claims(self._ready_queue[0])
                    self._processes_done.append(self._ready_queue.popleft())
                case ProcessState.READY:
                    pass
                case ProcessState.RESOURCE_WAIT:
                    print(f"{self._ready_queue[0]} is waiting on a resource")
                    self._wait_list.append(self._ready_queue.popleft())
                case ProcessState.SLEEP:
                    print(f"{self._ready_queue[0]} is sleeping")
                    self._wait_list.append(self._ready_queue.popleft())
                case _:
                    raise NotImplementedError
        else:
            self._idle_time += 1

        self.process_waiting_processes()
        self.increment_time()
        self.print_metrics()

        print(f"Completed Processes: {processes_str(self._processes_done)}")
        print(f"End Tick Ready Queue: {processes_str(self._ready_queue)}")
        print(f"End Tick Wait List: {processes_str(self._wait_list)}")

        return bool(self._processes) or bool(self._ready_queue) or bool(self._wait_list)
