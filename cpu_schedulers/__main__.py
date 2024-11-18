# TODO: Add a repl or something to allow the user to select the algorithm and the amount of processes and to customize
#     processes
# TODO: Create a function to randomly (seeded) generate a list of n processes **
# TODO: Create another function that will for sure create a deadlock(? I may not need to do this, I can just reduce
#     the amount of resources in the system and it should happen naturally)
# TODO: Collect Metrics **
# TODO: Generate a Gantt Chart?
# TODO: Generate Graphs

from .fcfs import FirstComeFirstServe
from .process import Process, Task, TaskAction
from .resource import Resource
from .resource_manager import AvoidantResourceAllocationGraph, ResourceAllocationGraph, ResourceManager
from .round_robin import RoundRobin


def main() -> None:
    resource_manager: ResourceManager = AvoidantResourceAllocationGraph((Resource(), Resource()))
    processes_1: list[Process] = [
        Process(
            0,
            6,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.IO, 1),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.IO, 1),
                Task(TaskAction.RESOURCE_RELEASE, 1),
                Task(TaskAction.IO, 1),
                Task(TaskAction.RESOURCE_RELEASE, 0),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            0,
            6,
            [
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.IO, 1),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.IO, 1),
                Task(TaskAction.RESOURCE_RELEASE, 1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.IO, 1),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(0, 6, []),
    ]

    fcfs = FirstComeFirstServe(processes_1, resource_manager)

    while fcfs.tick():
        pass

    Process.reset_ids()

    processes_2: list[Process] = [
        Process(
            0,
            6,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.IO, 1),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.IO, 1),
                Task(TaskAction.RESOURCE_RELEASE, 1),
                Task(TaskAction.IO, 1),
                Task(TaskAction.RESOURCE_RELEASE, 0),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            0,
            6,
            [
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.IO, 1),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.IO, 1),
                Task(TaskAction.RESOURCE_RELEASE, 1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.IO, 1),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(0, 6, []),
    ]

    round_robin = RoundRobin(processes_2, resource_manager, 2)

    while round_robin.tick():
        pass


if __name__ == "__main__":
    main()
