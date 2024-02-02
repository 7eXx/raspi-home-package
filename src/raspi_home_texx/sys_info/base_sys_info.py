from abc import abstractmethod, ABC


class _BaseSysInfo(ABC):

    def get_all_attributes(self):
        return self.__dict__

    @abstractmethod
    def serialize(self) -> str:
        pass

    @abstractmethod
    def format_pretty(self) -> str:
        pass