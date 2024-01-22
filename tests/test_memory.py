import unittest
from unittest.mock import Mock, patch
import json
import psutil
from src.system_info_texx.memory import Memory, Utils


class TestMemory(unittest.TestCase):
    @patch('psutil.virtual_memory', return_value=(1024 * 1024 * 1024, 512 * 1024 * 1024, 50.0, 256 * 1024 * 1024, 256 * 1024 * 1024))
    def test_init(self, mock_virtual_memory):
        # Create a Memory instance
        memory = Memory()

        # Check if the attributes are set correctly
        self.assertEqual(memory.unit, "MB")
        self.assertEqual(memory.total, 1024)  # 1024 MB = 1 GB
        self.assertEqual(memory.available, 512)  # 512 MB
        self.assertEqual(memory.percentage, 50.0)
        self.assertEqual(memory.used, 256)  # 256 MB
        self.assertEqual(memory.free, 256)  # 256 MB

    def test_serialize(self):
        # Set up values for the Memory instance
        memory = Memory()
        memory.unit = "MB"
        memory.total = 1024
        memory.available = 512
        memory.percentage = 50.0
        memory.used = 256
        memory.free = 256

        # Call the serialize method
        result = memory.serialize()

        # Check if the result matches the expected JSON string
        expected_result = '{"unit": "MB", "total": 1024, "available": 512, "percentage": 50.0, "used": 256, "free": 256}'
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()

