import json
import psutil

from .utils import Utils
from .base_sys_info import _BaseSysInfo


class Memory(_BaseSysInfo):
    def __init__(self) -> None:
        memory = psutil.virtual_memory()

        self.unit = "MB"
        self.total = Utils.convert_byte_to_megabyte(memory[0])
        self.available = Utils.convert_byte_to_megabyte(memory[1])
        self.percentage = memory[2]
        self.used = Utils.convert_byte_to_megabyte(memory[3])
        self.free = Utils.convert_byte_to_megabyte(memory[4])

    def serialize(self) -> str:
        return json.dumps(self.get_all_attributes())

    def format_pretty(self) -> str:
        output = "Memory: \n"
        output += "Total : " + str(self.total) + " " + self.unit + "\n"
        output += "Available : " + str(self.available) + " " + self.unit + "\n"
        output += "Used : " + str(self.used) + " " + self.unit + "\n"
        output += "Free : " + str(self.free) + " " + self.unit + "\n"
        output += "Percentage : " + str(self.percentage) + " %\n"

        return output
