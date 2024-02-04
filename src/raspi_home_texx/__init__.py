import logging
from functools import wraps
from .file_logger import FileLogger, __FileLoggerImpl


file_logger: FileLogger = __FileLoggerImpl()


def singleton(orig_cls):
    orig_new = orig_cls.__new__
    instance = None

    @wraps(orig_cls.__new__)
    def __new__(cls, *args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = orig_new(cls, *args, **kwargs)
        return instance

    orig_cls.__new__ = __new__

    return orig_cls


def get_console_logger(logger_name, level=logging.DEBUG) -> logging.Logger:
    # Create a custom logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a handler for console output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
