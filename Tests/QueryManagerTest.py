import unittest

from Classes import QueryManager


class QueryManagerTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.qm = QueryManager()

    def test_select_user_basecase(self):
        result = self.qm.select_user("meowmer")
        self.assertEqual(type(result), list, 
            "QueryManager: select_user did not return list format object")
        
    def test_select_all_user_basecase(self):
        result = self.qm.select_all_users()
        self.assertEqual(type(result), list, 
            "QueryManager: select_all_users did not return list format object")
        
    def test_insert_user_basecase(self):
        before = len(self.qm.select_user("Tom123"))
        self.qm.insert_user(True, 'Tom123')
        after = len(self.qm.select_user("Tom123"))
        self.assertEqual(after-before, 1, 
            "QueryManager: insert_user did not insert successfully")