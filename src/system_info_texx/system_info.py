import json
from abc import ABC, abstractmethod

from .cpu import Cpu
from .disk import Disk
from .memory import Memory


class SystemInfo(ABC):
    @abstractmethod
    def serialize(self) -> str:
        pass


class SimpleSystemInfo(SystemInfo):
    def __init__(self):
        self.cpu = Cpu()
        self.memory = Memory()
        self.disk = Disk()

    def serialize(self) -> str:
        return f'{{"cpu": {self.cpu.serialize()}, "memory": {self.memory.serialize()}, "disk": {self.disk.serialize()}}}'


class ExpandedSystemInfo(SystemInfo):
    def __init__(self):
        cpu = Cpu()
        memory = Memory()
        disk = Disk()

        self.cpu_temp = cpu.temperature
        self.cpu_perc = cpu.percentage

        self.tot_mem = memory.total
        self.ava_mem = memory.available
        self.per_mem = memory.percentage
        self.use_mem = memory.used
        self.fre_mem = memory.free

        self.tot_disk = disk.total
        self.use_disk = disk.used
        self.fre_disk = disk.free
        self.per_disk = disk.percentage

    def serialize(self) -> str:
        return json.dumps(self.__dict__)
