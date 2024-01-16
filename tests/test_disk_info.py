from unittest import TestCase

from src.system_info_texx.disk_info import DiskInfo


class DiskInfoTest(TestCase):

    disk_info: DiskInfo

    def setUp(self):
        self.disk_info = DiskInfo()

    def test_disk_info_serialization(self):
        serialized = self.disk_info.serialize()
        self.assertTrue("unit" in serialized)
        self.assertTrue("total" in serialized)
        self.assertTrue("used" in serialized)
        self.assertTrue("free" in serialized)
        self.assertTrue("percentage" in serialized)

    def test_disk_info_default(self):
        self.assertEqual(self.disk_info.unit, "GB")

    def test_disk_info_mb(self):
        self.disk_info = DiskInfo(unit="MB")

        self.assertEqual(self.disk_info.unit, "MB")
