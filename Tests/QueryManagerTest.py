import unittest

from Classes import QueryManager
from Classes import MainController

# helper functions
def user_creation(self, telename, age, gender, age_pref, gender_pref, cuisine_pref, diet_pref, queue_bool, chat_bool):
    self.mc.insert_user(True, telename, age, gender)
    user_id = self.mc.get_user_id(telename)["data"]["user_id"]
    self.mc.change_pref(telename, age_pref, "age_ref_id", "age_ref", True, True)
    self.mc.change_pref(telename, gender_pref, "gender_ref_id", "gender_ref", True, True)
    self.mc.change_pref(telename, cuisine_pref, "cuisine_ref_id", "cuisine_ref", True, True)
    self.mc.change_pref(telename, diet_pref, "diet_ref_id", "diet_ref", True, True)
    if queue_bool:
        self.mc.queue(telename)
    else:
        self.mc.dequeue(telename)
    if chat_bool:
        pass
    return {
        "user_id": user_id,
        "telename": telename, 
        "age": age, 
        "gender": gender, 
        "age_pref": age_pref, 
        "gender_pref": gender_pref, 
        "cuisine_pref": cuisine_pref, 
        "diet_pref": diet_pref, 
        "queue_bool": queue_bool, 
        "chat_bool": chat_bool
    }

def user_deletion(self, telename):
    self.mc.delete_user(telename)

def test_format(self, select_result, test_function):
        self.assertIsInstance(select_result, list,
            f"QueryManager: {test_function} did not return list() type object")
        for row in select_result:
            self.assertIsInstance(row, dict,
                f"QueryManager: {test_function} did not return list(dict()) type object")

# test for list and dict lengths
def test_length(self, select_result, test_function, list_length=1, dict_length=1, list_compare="equal", dict_compare="equal"):
    if list_compare == "equal":
        self.assertEqual(len(select_result), list_length,
            f"QueryManager: {test_function} did not return list of length {list_length}. {select_result}")
    elif list_compare == "greaterequal":
        self.assertGreaterEqual(len(select_result), list_length,
            f"QueryManager: {test_function} did not return list of length >= {list_length}. {select_result}")

    for row in select_result:
        if dict_compare == "equal":
            self.assertEqual(len(row), dict_length,
                f"QueryManager: {test_function} did not return dict of length {dict_length} within list result. {select_result}")
            
        elif dict_compare == "greaterequal":
            self.assertGreaterEqual(len(row), dict_length,
                f"QueryManager: {test_function} did not reutrn dict of length >= {dict_length} within list result")

class QueryManagerTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.qm = QueryManager()
        cls.mc = MainController()
        # setup user
        cls.telename = "TangoNovember"
        cls.age = 1
        cls.gender = 1
        cls.availability = True
        cls.initialAgePref = [1,2,4]
        cls.initialGenderPref = [1,3]
        cls.initialCuisinePref = [3,6,7]
        cls.initialDietPref = [1,3]
        # change bio info
        cls.changeUserAge = 2
        cls.changeUserGender = 3
        # change pref
        cls.addPrefBool = True
        cls.dltPrefBool = True
        cls.changepref = [1,3]
        cls.dltpref = [1,3]
        cls.addpref = [1,2,3]
        cls.changePrefColumn = "age_ref_id"
        cls.changePrefTable = "age_ref"
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
        user_deletion(self, self.telename)
        user_creation(self, self.telename, self.age, self.gender, self.initialAgePref, self.initialGenderPref, self.initialCuisinePref, self.initialDietPref, True, True)
        test_function = "select_user"
        result = self.qm.select_user(self.telename)
        test_format(self, result, test_function)
        test_length(self, result, test_function, dict_length=5)

    def test_insert_user(self):
        user_deletion(self, self.telename)
        user_creation(self, self.telename, self.age, self.gender, self.initialAgePref, self.initialGenderPref, self.initialCuisinePref, self.initialDietPref, True, True)
        before = len(self.qm.select_user(self.telename))
        if before == 0:
            self.qm.insert_user(self.availability, self.telename, self.age, self.gender)
            after = len(self.qm.select_user(self.telename))
            self.assertEqual(after-before, 1, 
                "QueryManager: insert_user did not insert successfully")

    def test_get_user_id(self):
        user_deletion(self, self.telename)
        user = user_creation(self, self.telename, self.age, self.gender, self.initialAgePref, self.initialGenderPref, self.initialCuisinePref, self.initialDietPref, True, True)
        user_id = user["user_id"]
        test_function = "get_user_id"
        result = self.qm.get_user_id(self.telename)
        test_format(self, result, test_function)
        test_length(self, result, test_function)
        self.assertIsInstance(user_id, int,
            f"QueryManager: {test_function} user_id not int type")

    def test_get_user_telename(self):
        user_deletion(self, self.telename)
        user = user_creation(self, self.telename, self.age, self.gender, self.initialAgePref, self.initialGenderPref, self.initialCuisinePref, self.initialDietPref, True, True)
        user_id = user["user_id"]
        test_function = "get_user_telename"
        result = self.qm.get_user_telename(user_id) 
        test_format(self, result, test_function)
        test_length(self, result, test_function)
        telename = result[0]["telename"]
        self.assertIsInstance(telename, str,
            f"QueryManager: {test_function} telename not str type")
        
    def test_get_user_info(self):
        user_deletion(self, self.telename)
        user_creation(self, self.telename, self.age, self.gender, self.initialAgePref, self.initialGenderPref, self.initialCuisinePref, self.initialDietPref, True, True)     
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
        user_deletion(self, self.telename)
        user = user_creation(self, self.telename, self.age, self.gender, self.initialAgePref, self.initialGenderPref, self.initialCuisinePref, self.initialDietPref, True, True)
        user_id = user["user_id"]
        test_function = "dlt_pref"

        initial_prefs = self.qm.select_pref(user_id, self.changePrefColumn, self.changePrefTable)
        expected_final_prefs = []
        for each_pref in initial_prefs:
            if (each_final_pref := each_pref[self.changePrefColumn]) not in self.dltpref:
                expected_final_prefs.append(each_final_pref)
        expected_final_prefs.sort()

        self.qm.dlt_pref(user_id, tuple(self.dltpref), self.changePrefColumn, self.changePrefTable)
        actual_final_prefs = self.qm.select_pref(user_id, self.changePrefColumn, self.changePrefTable)
        actual_final_prefs = sorted([each_pref[self.changePrefColumn] for each_pref in actual_final_prefs])
        self.assertEqual(expected_final_prefs, actual_final_prefs,
            f"QueryManager: {test_function} expected_final_prefs != actual_final_prefs")

    def test_add_multiple_prefs(self):
        user_deletion(self, self.telename)
        user = user_creation(self, self.telename, self.age, self.gender, self.initialAgePref, self.initialGenderPref, self.initialCuisinePref, self.initialDietPref, True, True)
        user_id = user["user_id"]
        test_function = "add_pref"

        initial_prefs = self.qm.select_pref(user_id, self.changePrefColumn, self.changePrefTable)
        expected_final_prefs = sorted(list(set([each_pref[self.changePrefColumn] for each_pref in initial_prefs] + self.addpref)))

        self.qm.add_multiple_prefs(user_id, self.addpref, self.changePrefColumn, self.changePrefTable)
        actual_final_prefs = self.qm.select_pref(user_id, self.changePrefColumn, self.changePrefTable)
        actual_final_prefs = sorted(list(set([each_pref[self.changePrefColumn] for each_pref in actual_final_prefs])))
        self.assertEqual(expected_final_prefs, actual_final_prefs,
            f"QueryManager: {test_function} expected_final_prefs != actual_final_prefs")

    # ensures age/gender/cuisine prefs >= 1 and diet prefs >= 0
    def test_select_pref(self):
        user_deletion(self, self.telename)
        user = user_creation(self, self.telename, self.age, self.gender, self.initialAgePref, self.initialGenderPref, self.initialCuisinePref, self.initialDietPref, True, True)
        user_id = user["user_id"]
        
        test_function = "select_pref(age)"

        age_result = self.qm.select_pref(user_id, "age_ref_id", "age_ref")
        test_format(self, age_result, test_function)
        test_length(self, age_result, test_function, list_length=1, list_compare="greaterequal")

        test_function = "select_pref(gender)"
        gender_result = self.qm.select_pref(user_id, "gender_ref_id", "gender_ref")
        test_format(self, gender_result, test_function)
        test_length(self, gender_result, test_function, list_length=1, list_compare="greaterequal")

        test_function = "select_pref(cuisine)"
        cuisine_result = self.qm.select_pref(user_id, "cuisine_ref_id", "cuisine_ref")
        test_format(self, cuisine_result, test_function)
        test_length(self, cuisine_result, test_function, list_length=1, list_compare="greaterequal")

        test_function = "select_pref(diet)"
        diet_result = self.qm.select_pref(user_id, "diet_ref_id", "diet_ref")
        test_format(self, diet_result, test_function)
        test_length(self, diet_result, test_function, list_length=1, list_compare="greaterequal")
        