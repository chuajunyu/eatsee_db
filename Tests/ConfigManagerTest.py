import unittest

from Classes import ConfigManager


class ConfigManagerTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.config = ConfigManager(path=r"dev.configtest")

    def test_get_basecase(self):
        result = self.config.get("database_host")
        self.assertEqual(type(result), str, 
            "ConfigManager : get did not return string format object")