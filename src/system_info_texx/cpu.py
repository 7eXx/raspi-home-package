import io
import platform

import psutil
import json


class Cpu:

    __sensor_file = '/sys/class/thermal/thermal_zone0/temp'

    def __init__(self) -> None:
        self.percentage = psutil.cpu_percent()
        self.temperature = 0

        if platform.system() == "Linux":
            try:
                with io.open(self.__sensor_file, 'r') as f:
                    self.temperature = float(f.read().strip()) / 1000
            except FileNotFoundError as err:
                pass

        self.min_temp = 0
        self.max_temp = 100
        self.unit = "°C"

    def serialize(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False)
