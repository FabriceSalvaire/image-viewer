class WorkerPool:
    """
    Pool of worker processes.
    """

    ##############################################

    def __init__(self) -> None:
        self.workers = []
        self._started = False
        self._counter = 0
