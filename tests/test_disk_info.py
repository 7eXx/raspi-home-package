from unittest import TestCase

from src.system_info_texx.cpu import Cpu
from src.system_info_texx.disk import Disk
from src.system_info_texx.memory import Memory


class SystemInfoTest(TestCase):

    disk: Disk
    memory: Memory
    cpu: Cpu

    def setUp(self):
        self.disk = Disk()
        self.memory = Memory()
        self.cpu = Cpu()

    def test_disk_info_serialization(self):
        serialized = self.disk.serialize()
        self.assertTrue("unit" in serialized)
        self.assertTrue("total" in serialized)
        self.assertTrue("used" in serialized)
        self.assertTrue("free" in serialized)
        self.assertTrue("percentage" in serialized)

    def test_disk_info_default(self):
        self.assertEqual(self.disk.unit, "GB")

    def test_disk_info_mb(self):
        self.disk = Disk(unit="MB")

        self.assertEqual(self.disk.unit, "MB")

    def test_disk_info_kb(self):
        self.disk = Disk(unit="KB")

        self.assertEqual(self.disk.unit, "KB")

    def test_disk_info_unknown(self):
        self.disk = Disk(unit="unknown")

        self.assertEqual(self.disk.unit, "B")

    def test_memory_info(self):
        self.assertEqual(self.memory.unit, "MB")

    def test_memory_serialization(self):
        serialized = self.memory.serialize()
        self.assertTrue("unit" in serialized)
        self.assertTrue("total" in serialized)
        self.assertTrue("available" in serialized)
        self.assertTrue("percentage" in serialized)
        self.assertTrue("used" in serialized)
        self.assertTrue("free" in serialized)

    def test_cpu_info(self):
        self.assertEqual(self.cpu.unit, "°C")
