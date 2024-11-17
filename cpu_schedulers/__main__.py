from .fcfs import FirstComeFirstServe
from .process import Process, Task, TaskAction
from .resource import Resource
from .resource_manager import ResourceManager
from .round_robin import RoundRobin


def main() -> None:
    resource_manager: ResourceManager = ResourceManager((Resource(),))
    processes_1: list[Process] = [
        Process(
            0,
            5,
            [
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            1,
            2,
            [
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            2,
            2,
            [
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            3,
            1,
            [
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            3,
            1,
            [
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            5,
            5,
            [
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            10,
            4,
            [
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            10,
            4,
            [
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
            ],
        ),
    ]

    fcfs = FirstComeFirstServe(processes_1, resource_manager)

    while fcfs.tick():
        pass

    Process.reset_ids()

    processes_2: list[Process] = [
        Process(
            0,
            5,
            [
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            1,
            2,
            [
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            2,
            2,
            [
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            3,
            1,
            [
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            3,
            1,
            [
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            5,
            5,
            [
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            10,
            4,
            [
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            10,
            4,
            [
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 2),
                Task(TaskAction.NONE, -1),
            ],
        ),
    ]

    round_robin = RoundRobin(processes_2, resource_manager, 2)

    while round_robin.tick():
        pass


if __name__ == "__main__":
    main()
