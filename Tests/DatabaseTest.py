import unittest

from Classes import Database


class DatabaseTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.db = Database()

    def test_execute_basecase(self):
        result = self.db.execute("SELECT * FROM users")
        self.assertEqual(type(result), list, 
            "Database object does not return list format object")
