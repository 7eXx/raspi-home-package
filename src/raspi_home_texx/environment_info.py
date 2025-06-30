from abc import ABC, abstractmethod

class EnvironmentInfo(ABC):
    @abstractmethod
    def serialize(self) -> str:
        pass

    @abstractmethod
    def format_pretty(self) -> str:
        pass