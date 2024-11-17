import dataclasses
import enum
from collections.abc import Sequence

from .resource_manager import ResourceManager


class TaskAction(enum.Enum):
    IO = enum.auto()
    NONE = enum.auto()
    RESOURCE_RELEASE = enum.auto()
    RESOURCE_REQUEST = enum.auto()


class ProcessState(enum.Enum):
    DONE = enum.auto()
    READY = enum.auto()
    RESOURCE_WAIT = enum.auto()
    SLEEP = enum.auto()


@dataclasses.dataclass
class Task:
    action: TaskAction
    data: int


class Process:
    _next_id: int = 0

    def __init__(self, arrival_time: int, duration: int, tasks: list[Task]):
        self._id: int = Process._next_id
        Process._next_id += 1

        self._process_state: ProcessState = ProcessState.READY

        self._tasks: list[Task] = tasks[::-1]
        self._held_resources: list[int] = []
        self._resource_manager: ResourceManager | None = None

        self._arrival_time: int = arrival_time
        self._completion_time: int = -1
        self._time_left: int = duration

        self._io_wait_time: int = 0
        self._io_wait_time_left: int = 0

        self._resource_wait_time: int = 0
        self._wait_time: int = 0

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
    def resource_wait_time(self) -> int:
        return self._resource_wait_time

    @property
    def time_left(self) -> int:
        return self._time_left

    @property
    def wait_time(self) -> int:
        return self._wait_time

    @property
    def held_resources(self) -> list[int]:
        return self._held_resources

    @property
    def process_state(self) -> ProcessState:
        return self._process_state

    def wait(self) -> ProcessState:
        match self.process_state:
            case ProcessState.DONE:
                pass
            case ProcessState.READY:
                self._wait_time += 1
            case ProcessState.RESOURCE_WAIT:
                self._resource_wait_time += 1
                resource_id = self._tasks[0].data

                if self._resource_manager and self._resource_manager.request(resource_id, self._id):
                    self._held_resources.append(resource_id)
                    self._process_state = ProcessState.READY
            case ProcessState.SLEEP:
                self._io_wait_time += 1
                self._io_wait_time_left -= 1

                if self._io_wait_time_left == 0:
                    del self._tasks[0]
                    self._process_state = ProcessState.READY

        return self._process_state

    def step(self, current_system_time: int) -> ProcessState:
        if self.process_state == ProcessState.DONE:
            return self._process_state

        if self._tasks:
            current_task = self._tasks[0]
            match current_task:
                case TaskAction.IO:
                    self._io_wait_time += 1
                    self._io_wait_time_left = current_task.data - 1
                    self._process_state = ProcessState.SLEEP
                    return self._process_state
                case TaskAction.NONE:
                    pass
                case TaskAction.RESOURCE_RELEASE:
                    resource_id = current_task.data

                    # In the real world, we would likely return an
                    # error to indicate to the caller that they tried
                    # to release the same resource twice. (At this
                    # point, their state is probably inconsistent and
                    # they probably need to fix that)
                    if resource_id in self._held_resources:
                        self._resource_manager.release(resource_id, self._id)
                        self._held_resources.remove(resource_id)
                case TaskAction.RESOURCE_REQUEST:
                    resource_id = current_task.data

                    if resource_id not in self._held_resources:
                        if self._resource_manager.request(resource_id, self._id):
                            self._held_resources.append(resource_id)
                        else:
                            self._resource_wait_time += 1
                            self._process_state = ProcessState.RESOURCE_WAIT
                            return self._process_state

            del self._tasks[0]

        self._time_left -= 1

        if self.time_left == 0:
            if self._held_resources and self._resource_manager:
                for resource_id in self._held_resources:
                    self._resource_manager.release(resource_id, self._id)
                del self._held_resources

            self._completion_time = current_system_time
            self._process_state = ProcessState.DONE

        return self._process_state


def processes_str(processes: Sequence[Process], separator: str = ", ") -> str:
    return separator.join(str(process) for process in processes)
