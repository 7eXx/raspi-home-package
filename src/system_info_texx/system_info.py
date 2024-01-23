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
        self.cpu_unit = cpu.unit

        self.mem_tot = memory.total
        self.mem_ava = memory.available
        self.mem_use = memory.used
        self.mem_fre = memory.free
        self.mem_uni = memory.unit
        self.mem_per = memory.percentage

        self.disk_tot = disk.total
        self.disk_use = disk.used
        self.disk_fre = disk.free
        self.disk_uni = disk.unit
        self.disk_per = disk.percentage

    def serialize(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False)

    def format_pretty(self) -> str:
        output = "CPU: \n"
        output += "Temperature : " + str(self.cpu_temp) + " " + self.cpu_unit + "\n"
        output += "Percentage : " + str(self.cpu_perc) + " %\n"
        output += "----------------------\n"
        output += "Memory: \n"
        output += "Total : " + str(self.mem_tot) + " " + self.mem_uni + "\n"
        output += "Available : " + str(self.mem_ava) + " " + self.mem_uni + "\n"
        output += "Used : " + str(self.mem_use) + " " + self.mem_uni + "\n"
        output += "Free : " + str(self.mem_fre) + " " + self.mem_uni + "\n"
        output += "Percentage : " + str(self.mem_per) + " %\n"
        output += "----------------------\n"
        output += "Disk: \n"
        output += "Total : " + str(self.disk_tot) + " " + self.disk_uni + "\n"
        output += "Used : " + str(self.disk_use) + " " + self.disk_uni + "\n"
        output += "Free : " + str(self.disk_fre) + " " + self.disk_uni + "\n"
        output += "Percentage : " + str(self.disk_per) + " %\n"

        return output
