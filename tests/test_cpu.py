import unittest
from unittest.mock import patch, Mock

from src.system_info_texx.cpu import Cpu


class TestCpu(unittest.TestCase):
    def setUp(self):
        # Create a Cpu instance
        self.cpu = Cpu()

    @patch('platform.system', return_value='Linux')
    @patch('io.open', create=True)
    def test_init_linux(self, mock_io_open, mock_platform_system):
        # Set up mock file content and open function for Linux platform
        mock_io_open.return_value.__enter__ = lambda s: s
        mock_io_open.return_value.__exit__ = Mock()
        mock_io_open.return_value.read.return_value = '50000\n'  # Assuming a temperature value of 50.000°C

        # Create a Cpu instance on Linux
        cpu_linux = Cpu()

        # Check if the temperature is correctly set
        self.assertEqual(cpu_linux.temperature, 50.0)

    @patch('platform.system', return_value='Windows')
    def test_init_windows(self, mock_platform_system):
        # Create a Cpu instance on Windows
        cpu_windows = Cpu()

        # Check if the temperature is set to 0 on non-Linux platforms
        self.assertEqual(cpu_windows.temperature, 0)

    def test_serialize(self):
        # Set up values for the Cpu instance
        self.cpu.percentage = 75.0
        self.cpu.temperature = 60.0
        self.cpu.min_temp = 0
        self.cpu.max_temp = 100
        self.cpu.unit = "°C"

        # Call the serialize method
        result = self.cpu.serialize()

        # Check if the result matches the expected JSON string
        expected_result = '{"percentage": 75.0, "temperature": 60.0, "min_temp": 0, "max_temp": 100, "unit": "°C"}'
        self.assertEqual(result, expected_result)

