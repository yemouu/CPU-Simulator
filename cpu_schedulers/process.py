import dataclasses
import enum
from collections.abc import Sequence

from .resource_manager import ResourceManager


class TaskAction(enum.Enum):
    """The possible actions that a process can perform

    NONE: A non-specific task, simulates a single unit of execution and
      is used to pad the space between other tasks.
    RESOURCE_RELEASE: Release an already held resource
    RESOURCE_REQUEST: Request a resource from the resource manager
    YIELD: Give up execution and place itself in the wait list
    """

    NONE = enum.auto()
    RESOURCE_RELEASE = enum.auto()
    RESOURCE_REQUEST = enum.auto()
    YIELD = enum.auto()


class ProcessState(enum.Enum):
    """The possible states that a process can be in

    DONE: The process is done executing
    READY: The process is ready to execute
    WAIT: The process is waiting on a resource
    SLEEP: The process has yielded and is sleeping
    """

    DONE = enum.auto()
    READY = enum.auto()
    WAIT = enum.auto()
    SLEEP = enum.auto()


@dataclasses.dataclass
class Task:
    """Task with data

    The data in our current cases is either a reousrce id or the sleep
    duration.
    """

    action: TaskAction
    data: int


class Process:
    """A Process within our system"""

    _next_id: int = 0

    def __init__(self, arrival_time: int, duration: int, tasks: list[Task]):
        self._id: int = Process._next_id
        Process._next_id += 1

        self._process_state: ProcessState = ProcessState.READY

        self._tasks: list[Task] = tasks
        self._held_resources: list[int] = []
        self._resource_manager: ResourceManager | None = None

        self._arrival_time: int = arrival_time
        self._completion_time: int = -1
        self._time_left: int = duration

        self._sleep_time: int = 0
        self._sleep_time_left: int = 0

        self._resource_wait_time: int = 0
        self._wait_time: int = 0

        if self._time_left < 1:
            raise ValueError("Duration is less than 1")

    # A better representation for printing a process object
    def __str__(self):
        return f"pid-{self._id}"

    @staticmethod
    def reset_ids() -> None:
        """Reset the ID counter"""
        Process._next_id = 0

    @property
    def pid(self) -> int:
        """Return the process id"""
        return self._id

    @property
    def arrival_time(self) -> int:
        """Return the tick that the process should have arrived at"""
        return self._arrival_time

    @property
    def completion_time(self) -> int:
        """Return the tick that the process completed execution"""
        return self._completion_time

    @property
    def resource_wait_time(self) -> int:
        """Return the time spent waiting on resources"""
        return self._resource_wait_time

    @property
    def sleep_time(self) -> int:
        """Return the time spent sleeping"""
        return self._sleep_time

    @property
    def time_left(self) -> int:
        """Return how many process ticks are left for this process"""
        return self._time_left

    @property
    def wait_time(self) -> int:
        """Return the time spent waiting in the ready queue"""
        return self._wait_time

    @property
    def resource_manager(self) -> ResourceManager:
        """Return the resource manager assigned to this process

        If the process was never given a resource manager, this method
        will raise a ValueError.
        """
        if self._resource_manager:
            return self._resource_manager

        raise ValueError("resource_manager was not set")

    @resource_manager.setter
    def resource_manager(self, resource_manager: ResourceManager) -> None:
        """Set the resource manager for the process"""
        if isinstance(resource_manager, ResourceManager):
            self._resource_manager = resource_manager
            return

        raise ValueError("Tried to set resource_manager to non-resource manager object")

    @property
    def held_resources(self) -> list[int]:
        """Return the resources that the process is holding"""
        return self._held_resources

    @property
    def process_state(self) -> ProcessState:
        """Return the process state"""
        return self._process_state

    def needed_resources(self) -> list[int]:
        """Return all the resource ids used for the process lifetime"""
        return [task.data for task in self._tasks if task.action == TaskAction.RESOURCE_REQUEST]

    def wait(self) -> ProcessState:
        """Perform wait tasks

        This method should only be called if the process is in some
        wait list or is waiting to become the first process in the
        queue.
        """
        match self.process_state:
            case ProcessState.DONE:
                pass
            case ProcessState.READY:
                self._wait_time += 1
            case ProcessState.WAIT:
                self._resource_wait_time += 1
                resource_id = self._tasks[0].data

                if self.resource_manager.request(resource_id, self._id):
                    self._held_resources.append(resource_id)
                    self._process_state = ProcessState.READY
            case ProcessState.SLEEP:
                if self._sleep_time_left == 0:
                    del self._tasks[0]
                    self._process_state = ProcessState.READY

                self._sleep_time += 1
                self._sleep_time_left -= 1
            case _:
                raise NotImplementedError

        return self._process_state

    def step(self, current_system_time: int) -> ProcessState:
        """Perform tasks

        This method should only be called if the process is ready to
        execute and is in the primary position in the ready queue.
        """
        if self.process_state != ProcessState.READY:
            return self.process_state

        if self._tasks:
            current_task = self._tasks[0]
            match current_task.action:
                case TaskAction.YIELD:
                    self._sleep_time += 1
                    self._sleep_time_left = current_task.data - 1
                    self._process_state = ProcessState.SLEEP
                    return self.process_state
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
                        self.resource_manager.release(resource_id, self._id)
                        self._held_resources.remove(resource_id)
                case TaskAction.RESOURCE_REQUEST:
                    resource_id = current_task.data

                    if resource_id not in self._held_resources:
                        if self.resource_manager.request(resource_id, self._id):
                            self._held_resources.append(resource_id)
                        else:
                            self._resource_wait_time += 1
                            self._process_state = ProcessState.WAIT
                            return self._process_state
                case _:
                    raise NotImplementedError

            del self._tasks[0]

        self._time_left -= 1

        if self.time_left == 0:
            if self._held_resources and self.resource_manager:
                for resource_id in self._held_resources:
                    self.resource_manager.release(resource_id, self._id)
                del self._held_resources

            self._completion_time = current_system_time
            self._process_state = ProcessState.DONE

        return self._process_state


def processes_str(processes: Sequence[Process], separator: str = ", ") -> str:
    """Turn a list of processes into a single string"""
    return separator.join(str(process) for process in processes)
