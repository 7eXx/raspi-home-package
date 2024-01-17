import psutil
import json

from .utils import Utils


class DiskInfo:
    def __init__(self, unit="GB") -> None:
        disk_usage = psutil.disk_usage("/")
        self.unit = unit
        self.total = Utils.convert_byte_to_unit(disk_usage[0], self.unit)
        self.used = Utils.convert_byte_to_unit(disk_usage[1], self.unit)
        self.free = Utils.convert_byte_to_unit(disk_usage[2], self.unit)
        self.percentage = disk_usage[3]

    def serialize(self) -> str:
        return json.dumps(self.__dict__)
