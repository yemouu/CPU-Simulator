from .scheduler import Scheduler


class MultilevelQueue(Scheduler):
    def __init__(self):
        raise NotImplementedError

class MultilevelFeedbackQueue(MultilevelQueue):
    def __init__(self):
        raise NotImplementedError
