from .fcfs import FirstComeFirstServe
from .process import Process


def main() -> None:
    processes = [
        Process(0, 5),
        Process(1, 2),
        Process(2, 2),
        Process(3, 1),
        Process(3, 1),
        Process(5, 5),
        Process(10, 4),
        Process(10, 4),
    ]

    fcfs = FirstComeFirstServe(processes)

    while fcfs.tick():
        pass


if __name__ == "__main__":
    main()
