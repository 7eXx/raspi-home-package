import unittest
from unittest.mock import Mock, patch
from src.system_info_texx.system_info import SimpleSystemInfo, ExpandedSystemInfo, Cpu, Memory, Disk


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
        sys_info = SimpleSystemInfo()
        print(sys_info.format_pretty())


class TestExpandedSystemInfo(unittest.TestCase):

    def test_serialize(self):
        # Set up values for the ExpandedSystemInfo instance
        expanded_sys_info = ExpandedSystemInfo()
        expanded_sys_info.cpu_temp = 42.0
        expanded_sys_info.cpu_perc = 75.0
        expanded_sys_info.tot_mem = 1024
        expanded_sys_info.ava_mem = 512
        expanded_sys_info.per_mem = 50.0
        expanded_sys_info.use_mem = 512
        expanded_sys_info.fre_mem = 512
        expanded_sys_info.tot_disk = 2048
        expanded_sys_info.use_disk = 1024
        expanded_sys_info.fre_disk = 1024
        expanded_sys_info.per_disk = 50.0

        # Call the serialize method
        result = expanded_sys_info.serialize()

        # Check if the result matches the expected JSON string
        expected_result = '{"cpu_temp": 42.0, "cpu_perc": 75.0, "tot_mem": 1024, "ava_mem": 512, "per_mem": 50.0, "use_mem": 512, "fre_mem": 512, "tot_disk": 2048, "use_disk": 1024, "fre_disk": 1024, "per_disk": 50.0}'
        self.assertEqual(result, expected_result)

    # TODO: make test for pretty format
    def test_format_pretty(self):
        sys_info = ExpandedSystemInfo()
        print(sys_info.format_pretty())


if __name__ == '__main__':
    unittest.main()
