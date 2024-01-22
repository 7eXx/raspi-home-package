import json
from abc import ABC, abstractmethod

from .cpu import Cpu
from .disk import Disk
from .memory import Memory


class SystemInfo(ABC):
    @abstractmethod
    def serialize(self) -> str:
        pass

    @abstractmethod
    def format_pretty(self) -> str:
        pass


class SimpleSystemInfo(SystemInfo):
    def __init__(self):
        self.cpu = Cpu()
        self.memory = Memory()
        self.disk = Disk()

    def serialize(self) -> str:
        return f'{{"cpu": {self.cpu.serialize()}, "memory": {self.memory.serialize()}, "disk": {self.disk.serialize()}}}'

    def format_pretty(self) -> str:
        output = self.cpu.format_pretty()
        output += "----------------------\n"
        output += self.memory.format_pretty()
        output += "----------------------\n"
        output += self.disk.format_pretty()

        return output


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

    def format_pretty(self) -> str:
        output = "CPU: \n"
        output += "Temperature : " + str(self.cpu_temp) + " °C\n"
        output += "Percentage : " + str(self.cpu_perc) + " %\n"
        output += "----------------------\n"
        output += "Memory: \n"
        output += "Total : " + str(self.tot_mem) + " MB\n"
        output += "Available : " + str(self.ava_mem) + " MB\n"
        output += "Used : " + str(self.use_mem) + " MB\n"
        output += "Free : " + str(self.fre_mem) + " MB\n"
        output += "Percentage : " + str(self.per_mem) + " %\n"
        output += "----------------------\n"
        output += "Disk: \n"
        output += "Total : " + str(self.tot_disk) + " GB\n"
        output += "Used : " + str(self.use_disk) + " GB\n"
        output += "Free : " + str(self.fre_disk) + " GB\n"
        output += "Percentage : " + str(self.per_disk) + " %\n"

        return output
