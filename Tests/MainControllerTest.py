import unittest
# python -m unittest -v Tests

from Classes import MainController
from Classes import QueryManager

# helper functions
def user_creation(self, telename, age, gender, age_pref, gender_pref, cuisine_pref, diet_pref, queue_bool, chat_bool):
    self.mc.insert_user(True, telename, age, gender)
    user_id = self.mc.get_user_id(telename)["data"]
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

def test_successCode(self, code, test_function):
    self.assertEqual(code, 200,
        f"MainController: {test_function} did not return code 200")
    
def test_failureCode(self, code, test_function):
    self.assertEqual(code, 404,
        f"MainController: {test_function} did not return code 404")

def test_int(self, value, test_function, text):
    self.assertIsInstance(value, int,
        f"MainController: {test_function} did not return int type for {text}")
    
def test_str(self, value, test_function, text):
    self.assertIsInstance(value, str,
        f"MainController: {test_function} did not return str type for {text}")

def test_list(self, value, test_function, text):
    self.assertIsInstance(value, list,
        f"MainController: {test_function} did not return list type for {text}")

def test_dict(self, value, test_function, text):
    self.assertIsInstance(value, dict,
        f"MainController: {test_function} did not return dict type for {text}")

def test_format(self, select_result, test_function):
    self.assertIsInstance(select_result, list,
        f"MainController: {test_function} did not return list() type object")
    for row in select_result:
        self.assertIsInstance(row, dict,
            f"MainController: {test_function} did not return list(dict()) type object")
        
def test_delete_user_NotIn(self, element, container, test_function, telename, table_name):
    self.assertNotIn(element, container,
        f"MainController: {test_function} did not successfully delete {telename} from {table_name}")


class MainControllerTest(unittest.TestCase):

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


    def test_select_user(self):
        pass

    def test_insert_user(self):
        pass

    def test_get_user_info(self):
        user_deletion(self, self.telename)
        user_creation(self, self.telename, self.age, self.gender, self.initialAgePref, self.initialGenderPref, self.initialCuisinePref, self.initialDietPref, True, True)
        result = self.mc.get_user_info(self.telename, "age_ref_id", "users")
        test_int(self, result[0]["age_ref_id"], "get_user_info", """result[0]["age_ref_id"]""")

    def test_show_profile(self):
        user_deletion(self, self.telename)
        user_creation(self, self.telename, self.age, self.gender, self.initialAgePref, self.initialGenderPref, self.initialCuisinePref, self.initialDietPref, True, True)
        test_function = "show_profile"
        result = self.mc.show_profile(self.telename)
        test_successCode(self, result["code"], test_function)
        test_str(self, result["data"]["telename"], test_function, """result["data"]["age"]""")
        test_int(self, result["data"]["age"], test_function, """result["data"]["age"]""")
        test_int(self, result["data"]["gender"], test_function, """result["data"]["gender"]""")
        test_list(self, result["data"]["age pref"], test_function, """result["data"]["age pref"]""")
        test_list(self, result["data"]["gender pref"], test_function, """result["data"]["gender pref"]""")
        test_list(self, result["data"]["cuisine pref"], test_function, """result["data"]["cuisine pref"]""")
        test_list(self, result["data"]["diet pref"], test_function, """result["data"]["diet pref"]""")

    def test_show_choices_template(self):
        result = self.mc.show_choices_template("gender_id", "gender", "gender")
        test_dict(self, result, "show_choices_template", "dict_choice")

    def test_show_one_choice(self):
        test_function = "show_one_choice"
        result = self.mc.show_one_choice("age_id", "age_range", "age")
        test_successCode(self, result["code"], test_function)

    def test_show_all_choices(self):
        test_function = "show_all_choices"
        result = self.mc.show_all_choices()
        test_successCode(self, result["code"], test_function)
        test_dict(self, result["data"]["age"], test_function, """result["data"]["age"]""")
        test_dict(self, result["data"]["gender"], test_function, """result["data"]["gender"]""")
        test_dict(self, result["data"]["cuisine"], test_function, """result["data"]["cuisine"]""")
        test_dict(self, result["data"]["diet"], test_function, """result["data"]["diet"]""")

    def test_change_user_info(self):
        user_deletion(self, self.telename)
        user_creation(self, self.telename, self.age, self.gender, self.initialAgePref, self.initialGenderPref, self.initialCuisinePref, self.initialDietPref, True, True)
        
        test_function = "change_user_info"

        age_return_result = self.mc.change_user_info(self.telename, self.changeUserAge, "age_ref_id", "age")
        test_successCode(self, age_return_result["code"], test_function)
        age_result = self.mc.get_user_info(self.telename, "age_ref_id")
        test_format(self, age_result, test_function)
        final_age = age_result[0]["age_ref_id"]
        test_int(self, final_age, test_function, "final_age")
        self.assertEqual(self.changeUserAge, final_age,
            f"MainController: {test_function} did not change Value in age_ref_id Column in users Table successfully to {self.changeUserAge}")
        
        gender_return_result = self.mc.change_user_info(self.telename, self.changeUserGender, "gender_ref_id", "gender")
        test_successCode(self, gender_return_result["code"], test_function)
        gender_result = self.mc.get_user_info(self.telename, "gender_ref_id")
        test_format(self, gender_result, test_function)
        final_gender = gender_result[0]["gender_ref_id"]
        test_int(self, final_gender, test_function, "final_gender")
        self.assertEqual(self.changeUserGender, final_gender,
            f"MainController: {test_function} did not change Value in age_gender_id Column in users Table successfully to {self.changeUserGender}")
        
    def test_select_pref(self):
        user_deletion(self, self.telename)
        user_creation(self, self.telename, self.age, self.gender, self.initialAgePref, self.initialGenderPref, self.initialCuisinePref, self.initialDietPref, True, True)
        test_function = "select_pref"
        result = self.mc.select_pref(self.telename, "gender_ref_id", "gender_ref")
        test_successCode(self, result["code"], test_function)
        test_list(self, result["data"], test_function, """result["data"]""")

    def test_change_pref(self):
        user_deletion(self, self.telename)
        user = user_creation(self, self.telename, self.age, self.gender, self.initialAgePref, self.initialGenderPref, self.initialCuisinePref, self.initialDietPref, True, True)
        user_id = user["user_id"]
        test_function = "change_pref"

        initial_pref = self.mc.select_pref(self.telename, self.changePrefColumn, self.changePrefTable)["data"]

        result = self.mc.change_pref(self.telename, self.changepref, self.changePrefColumn, self.changePrefTable, self.addPrefBool, self.dltPrefBool)
        test_successCode(self, result["code"], test_function)
        if not self.addPrefBool:
            self.assertEqual(result["data"]["added prefs"], None,
                f"""MainController: {test_function} did not return None for result["data"]["added prefs"]""")
        if not self.dltPrefBool:
            self.assertEqual(result["data"]["deleted prefs"], None,
                f"""MainController: {test_function} did not return None for result["data"]["deleted prefs"]""")
        
        final_pref = self.mc.select_pref(self.telename, self.changePrefColumn, self.changePrefTable)["data"]
        final_pref.sort()
        test_pref = []

        if self.addPrefBool and not self.dltPrefBool:
            test_function = "change_pref(add)"
            test_pref = initial_pref + self.changepref
            test_pref_set = set(test_pref)
            test_pref = list(test_pref_set)
            test_pref.sort()      
            
        elif self.dltPrefBool and not self.addPrefBool:
            test_function = "change_pref(delete)"
            for each_pref in initial_pref:
                if each_pref not in self.changepref:
                    test_pref.append(each_pref)

        elif self.addPrefBool and self.dltPrefBool:
            test_function = "change_pref(change)"
            test_pref = self.changepref
            test_pref.sort

        self.assertEqual(final_pref, test_pref,
                f"MainController: {test_function} did not change pref successfully, correct: {final_pref}; wrong: {test_pref}")

    def test_check_queue(self):
        user_deletion(self, self.telename)
        user_creation(self, self.telename, self.age, self.gender, self.initialAgePref, self.initialGenderPref, self.initialCuisinePref, self.initialDietPref, True, True)
        test_function = "check_queue"
        result = self.mc.check_queue()
        test_successCode(self, result["code"], test_function)
        test_list(self, result["data"], test_function, """result["data"]""")

    def test_queue(self):
        user_deletion(self, self.telename)
        user = user_creation(self, self.telename, self.age, self.gender, self.initialAgePref, self.initialGenderPref, self.initialCuisinePref, self.initialDietPref, True, True)
        test_function = "queue"
        user_id_queued_list_before = self.mc.check_queue()["data"]
        result = self.mc.queue(self.telename)
        user_id = user["user_id"]
        user_id_queued_list_after = self.mc.check_queue()["data"]
        if user_id in user_id_queued_list_before:
            test_failureCode(self, result["code"], test_function)
        elif user_id in user_id_queued_list_after:
            test_successCode(self, result["code"], test_function)

    def test_dequeue(self):
        user_deletion(self, self.telename)
        user = user_creation(self, self.telename, self.age, self.gender, self.initialAgePref, self.initialGenderPref, self.initialCuisinePref, self.initialDietPref, True, True)
        test_function = "dequeue"
        self.mc.queue(self.telename)
        result = self.mc.dequeue(self.telename)
        test_successCode(self, result["code"], test_function)
        user_id = user["user_id"]
        user_id_queued_list = self.mc.check_queue()["data"]
        self.assertNotIn(user_id, user_id_queued_list,
            f"MainController: {test_function} did not successfully dequeue {self.telename} with user_id: {user_id}")
        
    def test_person_match(self):
        pass

    def test_delete_user(self):
        user_deletion(self, self.telename)
        user = user_creation(self, self.telename, self.age, self.gender, self.initialAgePref, self.initialGenderPref, self.initialCuisinePref, self.initialDietPref, True, True)

        test_function = "delete_user"
        user_id = user["user_id"]
        result = self.mc.delete_user(self.telename)
        test_successCode(self, result["code"], test_function)

        users_table = [row["user_id"] for row in self.qm.get_info("user_id", "users")]
        chat_table = [row["user_id"] for row in self.qm.get_info("user_id", "chat")]
        queue_table = [row["user_id"] for row in self.qm.get_info("user_id", "queue")]
        ageref_table = [row["user_id"] for row in self.qm.get_info("user_ref_id", "age_ref")]
        genderref_table = [row["user_id"] for row in self.qm.get_info("user_ref_id", "gender_ref")]
        cuisineref_table = [row["user_id"] for row in self.qm.get_info("user_ref_id", "diet_ref")]
        dietref_table = [row["user_id"] for row in self.qm.get_info("user_ref_id", "cuisine_ref")]
        test_delete_user_NotIn(self, user_id, users_table, test_function, self.telename, "users")
        test_delete_user_NotIn(self, user_id, chat_table, test_function, self.telename, "chat")
        test_delete_user_NotIn(self, user_id, queue_table, test_function, self.telename, "queue")
        test_delete_user_NotIn(self, user_id, ageref_table, test_function, self.telename, "age_ref")
        test_delete_user_NotIn(self, user_id, genderref_table, test_function, self.telename, "gender_ref")
        test_delete_user_NotIn(self, user_id, cuisineref_table, test_function, self.telename, "cuisine_ref")
        test_delete_user_NotIn(self, user_id, dietref_table, test_function, self.telename, "diet_ref")

