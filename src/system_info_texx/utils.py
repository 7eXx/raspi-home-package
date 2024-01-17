
class Utils:

    @staticmethod
    def convert_byte_to_unit(bytes_val: float, unit="MB") -> float:
        if unit == "GB":
            return Utils.convert_byte_to_gigabyte(bytes_val)

        if unit == "MB":
            return Utils.convert_byte_to_megabyte(bytes_val)

        if unit == "KB":
            return Utils.convert_byte_to_kilobyte(bytes_val)

        return Utils.__convert_byte_with_power(bytes_val)

    @staticmethod
    def convert_byte_to_kilobyte(bytes_val: float):
        return Utils.__convert_byte_with_power(bytes_val, 10)

    @staticmethod
    def convert_byte_to_megabyte(bytes_val: float):
        return Utils.__convert_byte_with_power(bytes_val, 20)

    @staticmethod
    def convert_byte_to_gigabyte(bytes_val: float):
        return Utils.__convert_byte_with_power(bytes_val, 30)

    @staticmethod
    def __convert_byte_with_power(bytes_val: float, power: int = 0) -> float:
        return round(bytes_val / (2.0 ** power), 2)
