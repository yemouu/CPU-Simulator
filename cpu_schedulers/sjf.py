from .scheduler import Scheduler


class ShortestJobFirst(Scheduler):
    def __init__(self):
        raise NotImplementedError


class ShortestRemainingTimeFirst(ShortestJobFirst):
    def __init__(self):
        raise NotImplementedError
