from abc import ABC, abstractmethod

class EnvironmentInfo(ABC):

    def __init__(self, status = "n/a"):
        self._status = status

    @abstractmethod
    def serialize(self) -> str:
        pass

    @abstractmethod
    def format_pretty(self) -> str:
        pass

    def set_status(self, status) -> None:
        self._status = status
