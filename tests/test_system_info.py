import unittest
from unittest.mock import Mock
from src.raspi_home_texx.sys_info.system_info import SimpleSystemInfo, ExpandedSystemInfo, Cpu, Memory, Disk


class TestSimpleSystemInfo(unittest.TestCase):
    def setUp(self):
        # Create mock objects for Cpu, Memory, and Disk
        self.mock_cpu = Mock(spec=Cpu)
        self.mock_memory = Mock(spec=Memory)
        self.mock_disk = Mock(spec=Disk)

        # Create a SimpleSystemInfo instance with the mock objects
        self.system_info = SimpleSystemInfo()
        self.system_info.cpu = self.mock_cpu
        self.system_info.memory = self.mock_memory
        self.system_info.disk = self.mock_disk

    def test_serialize(self):
        # Set up the return values for the serialize methods of Cpu, Memory, and Disk
        self.mock_cpu.serialize.return_value = '{"cpu_info": "mocked"}'
        self.mock_memory.serialize.return_value = '{"memory_info": "mocked"}'
        self.mock_disk.serialize.return_value = '{"disk_info": "mocked"}'

        # Call the serialize method of SimpleSystemInfo
        result = self.system_info.serialize()

        # Check if the result matches the expected JSON string
        expected_result = '{"cpu": {"cpu_info": "mocked"}, "memory": {"memory_info": "mocked"}, "disk": {"disk_info": "mocked"}}'
        self.assertEqual(result, expected_result)

        # Check if the serialize methods of Cpu, Memory, and Disk were called
        self.mock_cpu.serialize.assert_called_once()
        self.mock_memory.serialize.assert_called_once()
        self.mock_disk.serialize.assert_called_once()

    # TODO: make test for pretty format
    def test_format_pretty(self):
        self.mock_cpu.format_pretty.return_value = "CPU Details\n"
        self.mock_memory.format_pretty.return_value = "Memory Details\n"
        self.mock_disk.format_pretty.return_value = "Disk Details"

        formatted_result = self.system_info.format_pretty()
        # Add your assertion here based on the expected formatted result
        expected_result = ("CPU Details\n"
                           "--------------------------------------------\n"
                           "Memory Details\n"
                           "--------------------------------------------\n"
                           "Disk Details")
        self.assertEqual(formatted_result, expected_result)


class TestExpandedSystemInfo(unittest.TestCase):

    def setUp(self):
        self.expanded_sys_info = ExpandedSystemInfo()
        self.expanded_sys_info.cpu_temp = 42.0
        self.expanded_sys_info.cpu_perc = 75.0
        self.expanded_sys_info.cpu_unit = "°C"
        self.expanded_sys_info.mem_tot = 1024
        self.expanded_sys_info.mem_ava = 512
        self.expanded_sys_info.mem_use = 512
        self.expanded_sys_info.mem_fre = 512
        self.expanded_sys_info.mem_uni = "MB"
        self.expanded_sys_info.mem_per = 50.0
        self.expanded_sys_info.disk_tot = 2048
        self.expanded_sys_info.disk_use = 1024
        self.expanded_sys_info.disk_fre = 1024
        self.expanded_sys_info.disk_uni = "GB"
        self.expanded_sys_info.disk_per = 50.0

    def test_serialize(self):
        # Call the serialize method
        result = self.expanded_sys_info.serialize()

        # Check if the result matches the expected JSON string
        expected_result = ('{"cpu_temp": 42.0, "cpu_perc": 75.0, "cpu_unit": "°C", '
                           '"mem_tot": 1024, "mem_ava": 512, "mem_use": 512, "mem_fre": 512, "mem_uni": "MB", "mem_per": 50.0, '
                           '"disk_tot": 2048, "disk_use": 1024, "disk_fre": 1024, "disk_uni": "GB", "disk_per": 50.0}')
        self.assertEqual(result, expected_result)

    # TODO: make test for pretty format
    def test_format_pretty(self):
        formatted_result = self.expanded_sys_info.format_pretty()

        # Add your assertion here based on the expected formatted result
        expected_result = ("CPU: \n"
                           "Temperature : 42.0 °C\n"
                           "Percentage : 75.0 %\n"
                           "--------------------------------------------\n"
                           "Memory: \n"
                           "Total : 1024 MB\n"
                           "Available : 512 MB\n"
                           "Used : 512 MB\n"
                           "Free : 512 MB\n"
                           "Percentage : 50.0 %\n"
                           "--------------------------------------------\n"
                           "Disk: \n"
                           "Total : 2048 GB\n"
                           "Used : 1024 GB\n"
                           "Free : 1024 GB\n"
                           "Percentage : 50.0 %\n")
        self.assertEqual(formatted_result, expected_result)


if __name__ == '__main__':
    unittest.main()
