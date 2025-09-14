from abc import ABC, abstractmethod

class EnvironmentInfo(ABC):

    def __init__(self, status = "n/a"):
        self._status = status
        self._timestamp = "n/a"

    @abstractmethod
    def serialize(self) -> str:
        pass

    @abstractmethod
    def format_pretty(self) -> str:
        pass

    def get_status(self) -> str:
        return self._status

    def set_status(self, status) -> None:
        self._status = status

    def get_timestamp(self) -> str:
        return self._timestamp

    def set_timestamp(self, timestamp) -> None:
        self._timestamp = timestamp
