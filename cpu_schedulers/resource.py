class Resource:
    _next_id: int = 0

    def __init__(self) -> None:
        self._id: int = Resource._next_id
        Resource._next_id += 1

        self._available = True
        self._process_id: int | None = None

    @staticmethod
    def reset_ids() -> None:
        Resource._next_id = 0

    @property
    def r_id(self) -> int:
        return self._id

    @property
    def process_id(self) -> int | None:
        return self._process_id

    @property
    def available(self) -> bool:
        return self._available

    def toggle_availability(self, process_id) -> None:
        self._process_id = process_id if self._available else None
        self._available = not self._available
