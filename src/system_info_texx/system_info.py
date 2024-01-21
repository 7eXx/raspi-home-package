from abc import ABC

from .cpu import Cpu
from .disk import Disk
from .memory import Memory


class SystemInfo(ABC):
    pass

class SimpleSystemInfo(SystemInfo):

    def __init__(self):
        def __init__(self):
            self.cpu = Cpu()
            self.memory = Memory()
            self.disk = Disk()

        def serialize(self):
            return f'{{"cpu": {self.cpu.serialize()}, "memory": {self.memory.serialize()}, "disk": {self.disk.serialize()}}}'