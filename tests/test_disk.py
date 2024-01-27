import unittest
from unittest.mock import patch
from src.system_info_texx.disk import Disk


class TestDisk(unittest.TestCase):
    @patch('psutil.disk_usage', return_value=(1024 * 1024 * 1024 * 10, 1024 * 1024 * 1024 * 5, 1024 * 1024 * 1024 * 2, 50.0))
    def test_init(self, mock_disk_usage):
        # Create a Disk instance
        disk = Disk(unit="GB")

        # Check if the attributes are set correctly
        self.assertEqual(disk.unit, "GB")
        self.assertEqual(disk.total, 10)
        self.assertEqual(disk.used, 5)
        self.assertEqual(disk.free, 2)
        self.assertEqual(disk.percentage, 50.0)

    def test_init_invalid_unit(self):
        # Create a Disk instance with an invalid unit
        disk = Disk(unit="InvalidUnit")

        # Check if the unit is set to "B" as a default
        self.assertEqual(disk.unit, "B")

    def test_serialize(self):
        # Set up values for the Disk instance
        disk = Disk(unit="GB")
        disk.total = 10
        disk.used = 5
        disk.free = 2
        disk.percentage = 50.0

        # Call the serialize method
        result = disk.serialize()

        # Check if the result matches the expected JSON string
        expected_result = '{"unit": "GB", "total": 10, "used": 5, "free": 2, "percentage": 50.0}'
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
