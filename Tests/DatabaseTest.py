import unittest

from Classes import Database


class DatabaseTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.db = Database()

    def test_execute_basecase(self):
        result = self.db.execute_select("SELECT * FROM users")
        self.assertEqual(type(result), list, 
            "Database: execute_select does not return list format object")
