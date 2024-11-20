class Resource:
    """Object representing an object in this system"""

    _next_id: int = 0

    def __init__(self) -> None:
        self._id: int = Resource._next_id
        Resource._next_id += 1

        self._available = True
        self._process_id: int | None = None

    @staticmethod
    def reset_ids() -> None:
        """Reset the id counter for resources"""
        Resource._next_id = 0

    @property
    def rid(self) -> int:
        """Return the id of the resource"""
        return self._id

    @property
    def process_id(self) -> int | None:
        """Return the id of the process we are servicing"""
        return self._process_id

    @property
    def available(self) -> bool:
        """Return if this process is available"""
        return self._available

    def toggle_availability(self, process_id) -> None:
        """Toggle resource availability"""
        self._process_id = process_id if self.available else None
        self._available = not self.available
