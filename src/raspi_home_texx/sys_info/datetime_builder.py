
import datetime


class DatetimeStringBuilder:

    def __init__(self) -> None:
        super().__init__()
        
    def now(self) -> str:
        now = datetime.datetime.now()

        return now.strftime("%d-%m-%Y %H:%M:%S")
