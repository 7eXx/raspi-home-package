import unittest
from src.raspi_home_texx import get_console_logger


class TestLogger(unittest.TestCase):

    def test_retrieve_same_logger(self):
        logger = get_console_logger("test")
        logger2 = get_console_logger("test")
        self.assertEqual(logger, logger2)

    def test_different_logger(self):
        logger = get_console_logger("test")
        logger2 = get_console_logger("test2")
        self.assertNotEqual(logger, logger2)


if __name__ == '__main__':
    unittest.main()