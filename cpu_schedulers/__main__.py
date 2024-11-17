from .fcfs import FirstComeFirstServe
from .process import Process
from .round_robin import RoundRobin


def main() -> None:
    processes_1: list[Process] = [
        Process(0, 5, []),
        Process(1, 2, []),
        Process(2, 2, []),
        Process(3, 1, []),
        Process(3, 1, []),
        Process(5, 5, []),
        Process(10, 4, []),
        Process(10, 4, []),
    ]

    fcfs = FirstComeFirstServe(processes_1)

    while fcfs.tick():
        pass

    processes_2: list[Process] = [
        Process(0, 5, []),
        Process(1, 2, []),
        Process(2, 2, []),
        Process(3, 1, []),
        Process(3, 1, []),
        Process(5, 5, []),
        Process(10, 4, []),
        Process(10, 4, []),
    ]

    round_robin = RoundRobin(processes_2, 2)

    while round_robin.tick():
        pass


if __name__ == "__main__":
    main()
