import unittest

from Classes import QueryManager

def test_format(self, select_result, test_function):
        self.assertIsInstance(select_result, list,
            f"QueryManager: {test_function} did not return list() type object")
        for row in select_result:
            self.assertIsInstance(row, dict,
                f"QueryManager: {test_function} did not return list(dict()) type object")

# test for list and dict lengths
def test_length(self, select_result, test_function, list_length=1, dict_length=1, dict_compare="equal", arg1=None):
    self.assertEqual(len(select_result), list_length,
        f"QueryManager: {test_function} did not return list of length {list_length}. {select_result}, {arg1}")
    for row in select_result:
        if dict_compare == "equal":
            self.assertEqual(len(row), dict_length,
                f"QueryManager: {test_function} did not return dict of length {dict_length} within list result. {select_result}")
            
        if dict_compare == "greaterequal":
            self.assertGreaterEqual(len(row), dict_length,
                f"QueryManager: {test_function} did not reutrn dict of length >= {dict_length} within list result")

class QueryManagerTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.qm = QueryManager()
        cls.telename = "TangoNovember"
        cls.age = 1
        cls.gender = 1
        cls.availability = True
        cls.dltpref = [1,3]
        cls.addpref = [1,2,3]
        cls.changePrefColumn = "age_ref_id"
        cls.changePrefTable = "age_ref"

    # test functions

    # def test_select_user_basecase(self):
    #     result = self.qm.select_user("meowmer")
    #     test_format(self, result, "select_user")
        
    # def test_select_all_user_basecase(self):
    #     result = self.qm.select_all_users()
    #     test_format(self, result, "select_all_user")

    # def test_insert_user_basecasepython -m unittest(self):
    #     before = len(self.qm.select_user(self.telename))
    #     self.qm.insert_user(self.availability, self.telename, self.age, self.gender)
    #     after = len(self.qm.select_user(self.telename))
    #     self.assertEqual(after-before, 1, 
    #         "QueryManager: insert_user did not insert successfully")

    def test_select_user(self):
        test_function = "select_user"
        result = self.qm.select_user(self.telename)
        test_format(self, result, test_function)
        test_length(self, result, test_function, dict_length=5)

    def test_insert_user(self):
        before = len(self.qm.select_user(self.telename))
        if before == 0:
            self.qm.insert_user(self.availability, self.telename, self.age, self.gender)
            after = len(self.qm.select_user(self.telename))
            self.assertEqual(after-before, 1, 
                "QueryManager: insert_user did not insert successfully")

    def test_get_user_id(self):
        result = self.qm.get_user_id(self.telename)
        test_function = "get_user_id"
        test_format(self, result, test_function)
        test_length(self, result, test_function)
        user_id = result[0]["user_id"]
        self.assertIsInstance(user_id, int,
            f"QueryManager: {test_function} user_id not int type")

    def test_get_user_telename(self):
        user_id = self.qm.get_user_id(self.telename)[0]["user_id"]
        result = self.qm.get_user_telename(user_id)
        test_function = "get_user_telename"
        test_format(self, result, test_function)
        test_length(self, result, test_function)
        telename = result[0]["telename"]
        self.assertIsInstance(telename, str,
            f"QueryManager: {test_function} telename not str type")
        
    def test_get_user_info(self):
        
        test_function = "get_user_info"

        age_result = self.qm.get_user_info(self.telename, "age_ref_id", "users")
        test_format(self, age_result, test_function)
        test_length(self, age_result, test_function)
        age_id = age_result[0]["age_ref_id"]
        self.assertIsInstance(age_id, int,
            f"QueryManager: {test_function} age_id not int type")
        
        gender_result = self.qm.get_user_info(self.telename, "gender_ref_id", "users")
        test_format(self, gender_result, test_function)
        test_length(self, gender_result, test_function)
        gender_id = gender_result[0]["gender_ref_id"]
        self.assertIsInstance(gender_id, int,
            f"QueryManager: {test_function} gender_id not int type")

    # def test_get_info(self):
    #     pass

    # def test_update_user_info(self):
    #     pass

    def test_dlt_pref(self):
        user_id = self.qm.get_user_id(self.telename)[0]["user_id"]
        test_function = "dlt_pref"

        initial_prefs = self.qm.select_pref(user_id, self.changePrefColumn, self.changePrefTable)
        untouched_prefs = []
        for each_pref in initial_prefs:
            refcolumn = tuple(each_pref)[0]
            if each_pref[refcolumn] not in self.dltpref:
                untouched_prefs.append(each_pref[refcolumn])
        untouched_prefs.sort()

        self.qm.dlt_pref(user_id, tuple(self.dltpref), self.changePrefColumn, self.changePrefTable)
        final_prefs = self.qm.select_pref(user_id, self.changePrefColumn, self.changePrefTable)
        final_prefs = [each_pref[refcolumn] for each_pref in final_prefs]
        final_prefs.sort()
        self.assertEqual(untouched_prefs, final_prefs,
            f"QueryManager: {test_function} untouched_prefs != final_prefs")

    def test_add_pref(self):
        user_id = self.qm.get_user_id(self.telename)[0]["user_id"]
        test_function = "add_pref"

        initial_prefs = self.qm.select_pref(user_id, self.changePrefColumn, self.changePrefTable)
        
        # ensures age/gender/cuisine prefs >= 1 and diet prefs >= 0
    # def test_select_pref(self):
    #     user_id = self.qm.get_user_id(self.telename)[0]["user_id"]
        
    #     test_function = "select_pref(age)"

    #     age_result = self.qm.select_pref(user_id, "age_ref_id", "age_ref")
    #     test_format(self, age_result, test_function)
    #     test_length(self, age_result, test_function, dict_length=0, dict_compare="greaterequal")

    #     test_function = "select_pref(gender)"
    #     gender_result = self.qm.select_pref(user_id, "gender_ref_id", "gender_ref")
    #     test_format(self, gender_result, test_function)
    #     test_length(self, gender_result, test_function, dict_length=0, dict_compare="greaterequal")

    #     test_function = "select_pref(cuisine)"
    #     cuisine_result = self.qm.select_pref(user_id, "cuisine_ref_id", "cuisine_ref")
    #     test_format(self, cuisine_result, test_function)
    #     test_length(self, cuisine_result, test_function, dict_length=0, dict_compare="greaterequal")

    #     test_function = "select_pref(diet)"
    #     diet_result = self.qm.select_pref(user_id, "diet_ref_id", "diet_ref")
    #     test_format(self, diet_result, test_function)
    #     test_length(self, diet_result, test_function, dict_length=0, dict_compare="greaterequal")

    
        
