from .fcfs import FirstComeFirstServe
from .process import Process


def main() -> None:
    processes = [
        Process(0, 5, "1"),
        Process(1, 2, "2"),
        Process(2, 2, "3"),
        Process(3, 1, "4"),
        Process(3, 1, "5"),
        Process(5, 5, "6"),
        Process(10, 4, "7,"),
        Process(10, 4, "8,"),
    ]

    fcfs = FirstComeFirstServe(processes)

    while fcfs.tick():
        pass


if __name__ == "__main__":
    main()
