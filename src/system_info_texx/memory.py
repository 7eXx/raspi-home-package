import json
import psutil

from .utils import Utils


class Memory:
    def __init__(self) -> None:
        memory = psutil.virtual_memory()

        self.unit = "MB"
        self.total = Utils.convert_byte_to_megabyte(memory[0])
        self.available = Utils.convert_byte_to_megabyte(memory[1])
        self.percentage = memory[2]
        self.used = Utils.convert_byte_to_megabyte(memory[3])
        self.free = Utils.convert_byte_to_megabyte(memory[4])

    def serialize(self) -> str:
        return json.dumps(self.__dict__)