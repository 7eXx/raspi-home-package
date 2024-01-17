import psutil
import json

from gpiozero import CPUTemperature


class Cpu:
    def __init__(self) -> None:
        self.percentage = psutil.cpu_percent()
        self.__retrieve_cpu_temperature()
        self.unit = "°C"

    def __retrieve_cpu_temperature(self) -> None:
        # recupero della temperatura della cpu
        try:
            cpu = CPUTemperature()
            self.min_temp = cpu.min_temp
            self.max_temp = cpu.max_temp
            self.temperature = cpu.temperature
        except FileNotFoundError as err:
            self.min_temp = 0
            self.max_temp = 0
            self.temperature = 0

    def serialize(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False)