import psutil
import json

from ..utils import Utils
from .base_sys_info import _BaseSysInfo


class Disk(_BaseSysInfo):
    def __init__(self, unit="GB") -> None:
        super().__init__()
        disk_usage = psutil.disk_usage("/")

        if unit != "GB" and unit != "MB" and unit != "KB":
            self.unit = "B"
        else:
            self.unit = unit

        self.total = Utils.convert_byte_to_unit(disk_usage[0], self.unit)
        self.used = Utils.convert_byte_to_unit(disk_usage[1], self.unit)
        self.free = Utils.convert_byte_to_unit(disk_usage[2], self.unit)
        self.percentage = disk_usage[3]

    def serialize(self) -> str:
        return json.dumps(self.get_all_attributes())

    def format_pretty(self) -> str:
        output = "Disk: \n"
        output += "Total : " + str(self.total) + " " + self.unit + "\n"
        output += "Used : " + str(self.used) + " " + self.unit + "\n"
        output += "Free : " + str(self.free) + " " + self.unit + "\n"
        output += "Percentage : " + str(self.percentage) + " %"

        return output
