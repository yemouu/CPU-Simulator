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
    resource_manager_1: ResourceManager = ResourceManager((Resource(),))
    processes_1: list[Process] = [
        Process(3, 4, []),
        Process(2, 1, []),
        Process(0, 4, []),
        Process(2, 4, []),
        Process(5, 2, []),
        Process(7, 3, []),
        Process(9, 4, []),
        Process(7, 2, []),
        Process(5, 3, []),
        Process(2, 3, []),
    ]

    fcfs_1 = FirstComeFirstServe(processes_1, resource_manager_1)

    print("---------- fcfs_1 ----------")
    while fcfs_1.tick():
        pass

    Process.reset_ids()
    Resource.reset_ids()

    resource_manager_2: ResourceManager = ResourceManager((Resource(),))
    processes_2: list[Process] = [
        Process(
            3,
            4,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.IO, 1),
                Task(TaskAction.IO, 1),
            ],
        ),
        Process(2, 1, [Task(TaskAction.NONE, -1)]),
        Process(
            0,
            4,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.IO, 1),
            ],
        ),
        Process(
            2,
            4,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_RELEASE, 0),
                Task(TaskAction.NONE, 1),
                Task(TaskAction.NONE, 1),
            ],
        ),
        Process(
            5,
            2,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
            ],
        ),
        Process(
            7,
            3,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 1),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            9,
            4,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_RELEASE, 0),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            7,
            2,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            5,
            3,
            [
                Task(TaskAction.IO, 1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_RELEASE, 0),
            ],
        ),
        Process(
            2,
            3,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_RELEASE, 0),
            ],
        ),
    ]

    fcfs_2 = FirstComeFirstServe(processes_2, resource_manager_2)

    print("---------- fcfs_2 ----------")
    while fcfs_2.tick():
        pass

    Process.reset_ids()
    Resource.reset_ids()

    resource_manager_3: ResourceManager = ResourceAllocationGraph((Resource(), Resource()))
    processes_3: list[Process] = [
        Process(
            3,
            4,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.IO, 1),
                Task(TaskAction.IO, 1),
            ],
        ),
        Process(2, 1, [Task(TaskAction.NONE, -1)]),
        Process(
            0,
            4,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.IO, 1),
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.IO, 1),
            ],
        ),
        Process(
            2,
            4,
            [
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.NONE, 1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.NONE, 1),
            ],
        ),
        Process(
            5,
            2,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
            ],
        ),
        Process(
            7,
            3,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 1),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            9,
            4,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.RESOURCE_RELEASE, 1),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            7,
            2,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            5,
            3,
            [
                Task(TaskAction.IO, 1),
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
            ],
        ),
        Process(
            2,
            3,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_RELEASE, 0),
            ],
        ),
    ]

    fcfs_3 = FirstComeFirstServe(processes_3, resource_manager_3)

    print("---------- fcfs_3 ----------")
    while fcfs_3.tick():
        pass

    Process.reset_ids()
    Resource.reset_ids()

    resource_manager_4: ResourceManager = AvoidantResourceAllocationGraph((Resource(),))
    processes_4: list[Process] = [
        Process(3, 4, []),
        Process(2, 1, []),
        Process(0, 4, []),
        Process(2, 4, []),
        Process(5, 2, []),
        Process(7, 3, []),
        Process(9, 4, []),
        Process(7, 2, []),
        Process(5, 3, []),
        Process(2, 3, []),
    ]

    fcfs_4 = FirstComeFirstServe(processes_4, resource_manager_4)

    print("---------- fcfs_4 ----------")
    while fcfs_4.tick():
        pass

    Process.reset_ids()
    Resource.reset_ids()

    resource_manager_5: ResourceManager = AvoidantResourceAllocationGraph((Resource(),))
    processes_5: list[Process] = [
        Process(
            3,
            4,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.IO, 1),
                Task(TaskAction.IO, 1),
            ],
        ),
        Process(2, 1, [Task(TaskAction.NONE, -1)]),
        Process(
            0,
            4,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.IO, 1),
            ],
        ),
        Process(
            2,
            4,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_RELEASE, 0),
                Task(TaskAction.NONE, 1),
                Task(TaskAction.NONE, 1),
            ],
        ),
        Process(
            5,
            2,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
            ],
        ),
        Process(
            7,
            3,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 1),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            9,
            4,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_RELEASE, 0),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            7,
            2,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            5,
            3,
            [
                Task(TaskAction.IO, 1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_RELEASE, 0),
            ],
        ),
        Process(
            2,
            3,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_RELEASE, 0),
            ],
        ),
    ]

    fcfs_5 = FirstComeFirstServe(processes_5, resource_manager_5)

    print("---------- fcfs_5 ----------")
    while fcfs_5.tick():
        pass

    Process.reset_ids()
    Resource.reset_ids()

    resource_manager_6: ResourceManager = AvoidantResourceAllocationGraph((Resource(), Resource()))
    processes_6: list[Process] = [
        Process(
            3,
            4,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.IO, 1),
                Task(TaskAction.IO, 1),
            ],
        ),
        Process(2, 1, [Task(TaskAction.NONE, -1)]),
        Process(
            0,
            4,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.IO, 1),
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.IO, 1),
            ],
        ),
        Process(
            2,
            4,
            [
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.NONE, 1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.NONE, 1),
            ],
        ),
        Process(
            5,
            2,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
            ],
        ),
        Process(
            7,
            3,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 1),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            9,
            4,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.RESOURCE_RELEASE, 1),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            7,
            2,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            5,
            3,
            [
                Task(TaskAction.IO, 1),
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
            ],
        ),
        Process(
            2,
            3,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_RELEASE, 0),
            ],
        ),
    ]

    fcfs_6 = FirstComeFirstServe(processes_6, resource_manager_6)

    print("---------- fcfs_6 ----------")
    while fcfs_6.tick():
        pass

    Process.reset_ids()
    Resource.reset_ids()

    resource_manager_7: ResourceManager = ResourceManager((Resource(),))
    processes_7: list[Process] = [
        Process(3, 4, []),
        Process(2, 1, []),
        Process(0, 4, []),
        Process(2, 4, []),
        Process(5, 2, []),
        Process(7, 3, []),
        Process(9, 4, []),
        Process(7, 2, []),
        Process(5, 3, []),
        Process(2, 3, []),
    ]

    rr_1 = RoundRobin(processes_7, resource_manager_7, 2)

    print("----------- rr_1 -----------")
    while rr_1.tick():
        pass

    Process.reset_ids()
    Resource.reset_ids()

    resource_manager_8: ResourceManager = ResourceManager((Resource(),))
    processes_8: list[Process] = [
        Process(
            3,
            4,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.IO, 1),
                Task(TaskAction.IO, 1),
            ],
        ),
        Process(2, 1, [Task(TaskAction.NONE, -1)]),
        Process(
            0,
            4,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.IO, 1),
            ],
        ),
        Process(
            2,
            4,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_RELEASE, 0),
                Task(TaskAction.NONE, 1),
                Task(TaskAction.NONE, 1),
            ],
        ),
        Process(
            5,
            2,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
            ],
        ),
        Process(
            7,
            3,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 1),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            9,
            4,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_RELEASE, 0),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            7,
            2,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            5,
            3,
            [
                Task(TaskAction.IO, 1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_RELEASE, 0),
            ],
        ),
        Process(
            2,
            3,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_RELEASE, 0),
            ],
        ),
    ]

    rr_2 = RoundRobin(processes_8, resource_manager_8, 2)

    print("----------- rr_2 -----------")
    while rr_2.tick():
        pass

    Process.reset_ids()
    Resource.reset_ids()

    resource_manager_9: ResourceManager = ResourceAllocationGraph((Resource(), Resource()))
    processes_9: list[Process] = [
        Process(
            3,
            4,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.IO, 1),
                Task(TaskAction.IO, 1),
            ],
        ),
        Process(2, 1, [Task(TaskAction.NONE, -1)]),
        Process(
            0,
            4,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.IO, 1),
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.IO, 1),
            ],
        ),
        Process(
            2,
            4,
            [
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.NONE, 1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.NONE, 1),
            ],
        ),
        Process(
            5,
            2,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
            ],
        ),
        Process(
            7,
            3,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 1),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            9,
            4,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.RESOURCE_RELEASE, 1),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            7,
            2,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            5,
            3,
            [
                Task(TaskAction.IO, 1),
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
            ],
        ),
        Process(
            2,
            3,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_RELEASE, 0),
            ],
        ),
    ]

    rr_3 = RoundRobin(processes_9, resource_manager_9, 2)

    print("----------- rr_3 -----------")
    while rr_3.tick():
        pass

    Process.reset_ids()
    Resource.reset_ids()

    resource_manager_10: ResourceManager = AvoidantResourceAllocationGraph((Resource(),))
    processes_10: list[Process] = [
        Process(3, 4, []),
        Process(2, 1, []),
        Process(0, 4, []),
        Process(2, 4, []),
        Process(5, 2, []),
        Process(7, 3, []),
        Process(9, 4, []),
        Process(7, 2, []),
        Process(5, 3, []),
        Process(2, 3, []),
    ]

    rr_4 = RoundRobin(processes_10, resource_manager_10, 2)

    print("----------- rr_4 -----------")
    while rr_4.tick():
        pass

    Process.reset_ids()
    Resource.reset_ids()

    resource_manager_11: ResourceManager = AvoidantResourceAllocationGraph((Resource(),))
    processes_11: list[Process] = [
        Process(
            3,
            4,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.IO, 1),
                Task(TaskAction.IO, 1),
            ],
        ),
        Process(2, 1, [Task(TaskAction.NONE, -1)]),
        Process(
            0,
            4,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.IO, 1),
            ],
        ),
        Process(
            2,
            4,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_RELEASE, 0),
                Task(TaskAction.NONE, 1),
                Task(TaskAction.NONE, 1),
            ],
        ),
        Process(
            5,
            2,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
            ],
        ),
        Process(
            7,
            3,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 1),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            9,
            4,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_RELEASE, 0),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            7,
            2,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            5,
            3,
            [
                Task(TaskAction.IO, 1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_RELEASE, 0),
            ],
        ),
        Process(
            2,
            3,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_RELEASE, 0),
            ],
        ),
    ]

    rr_5 = RoundRobin(processes_11, resource_manager_11, 2)

    print("----------- rr_5 -----------")
    while rr_5.tick():
        pass

    Process.reset_ids()
    Resource.reset_ids()

    resource_manager_12: ResourceManager = AvoidantResourceAllocationGraph((Resource(), Resource()))
    processes_12: list[Process] = [
        Process(
            3,
            4,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.IO, 1),
                Task(TaskAction.IO, 1),
            ],
        ),
        Process(2, 1, [Task(TaskAction.NONE, -1)]),
        Process(
            0,
            4,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.IO, 1),
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.IO, 1),
            ],
        ),
        Process(
            2,
            4,
            [
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.NONE, 1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.NONE, 1),
            ],
        ),
        Process(
            5,
            2,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
            ],
        ),
        Process(
            7,
            3,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.IO, 1),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            9,
            4,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.RESOURCE_RELEASE, 1),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            7,
            2,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.NONE, -1),
            ],
        ),
        Process(
            5,
            3,
            [
                Task(TaskAction.IO, 1),
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
            ],
        ),
        Process(
            2,
            3,
            [
                Task(TaskAction.NONE, -1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.RESOURCE_RELEASE, 0),
            ],
        ),
    ]

    rr_6 = RoundRobin(processes_12, resource_manager_12, 2)

    print("----------- rr_6 -----------")
    while rr_6.tick():
        pass

    Process.reset_ids()
    Resource.reset_ids()

    resource_manager_13: ResourceManager = AvoidantResourceAllocationGraph((Resource(), Resource()))
    processes_13: list[Process] = [
        Process(
            0,
            5,
            [
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.IO, 1),
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.IO, 1),
            ],
        ),
        Process(
            0,
            5,
            [
                Task(TaskAction.RESOURCE_REQUEST, 1),
                Task(TaskAction.IO, 1),
                Task(TaskAction.RESOURCE_REQUEST, 0),
                Task(TaskAction.IO, 1),
            ],
        ),
    ]

    rr_7 = RoundRobin(processes_13, resource_manager_13, 2)

    print("----------- rr_7 -----------")
    while rr_7.tick():
        pass


if __name__ == "__main__":
    main()
