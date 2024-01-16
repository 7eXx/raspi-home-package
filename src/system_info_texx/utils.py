
class Utils:

    @staticmethod
    def convert_byte_to_unit(bytes_val, unit="MB") -> float:
        unit_power = 20
        if unit == "GB":
            unit_power = 30

        return Utils.__convert_byte_with_power(bytes_val, unit_power)

    @staticmethod
    def __convert_byte_with_power(bytes_val, power: int) -> float:
        return round(bytes_val / (2.0 ** power), 2)
