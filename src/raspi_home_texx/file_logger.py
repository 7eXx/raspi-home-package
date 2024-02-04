import os
from abc import ABC, abstractmethod
from datetime import datetime


class FileLogger(ABC):
    _file_path = "raspi_home.log"
    _max_size = 2097152

    # fuction to allow to write to file
    def write(self, msg):
        write_mode = self.__get_write_mode()

        with open(self._file_path, mode=write_mode) as file:
            file.write("[" + "{:%Y-%m-%d %H:%M:%S}".format(datetime.now()) + "] : " + msg + "\n")

    def __get_write_mode(self) -> str:
        if not os.path.exists(self._file_path):
            return 'w'

        stat_info = os.stat(self._file_path)
        if stat_info.st_size > self._max_size:
            return 'w'
        else:
            return 'a'

    def is_log_exists(self):
        return os.path.exists(self._file_path)

    def delete_if_log_exists(self):
        if self.is_log_exists():
            os.remove(self._file_path)

    def set_file_path(self, path: str):
        self._file_path = path


class __FileLoggerImpl(FileLogger):

    def __init__(self):
        super().__init__()
