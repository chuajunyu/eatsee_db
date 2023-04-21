from .QueryManager import QueryManager

class MainController:
    """
    Handles the logic and calls the relevant queries using QueryManager
    to provide the services of the API Endpoints.
    """
    def __init__(self):
        self.qm = QueryManager()

    def select_user(self, telename: str):
        """
        Returns a list of users from database with that telegram name.
        By right, there should only be one user.

        Input:
            - telename: Telegram username to search for

        Returns:
            - List containing users with that telename.
        """
        print(self.qm.select_user(telename))
        return self.qm.select_user(telename)

    def insert_user(self, availability: bool, telename: str, age: int, gender: int):
        """
        Inserts a user into the database
        
        Input:
            - availability: Boolean value describing availability of user 
              (Might be deprecated)
            - telename: Telegram username of new user to be inserted

        Return:
            - Dictionary containing message
        """
        if self.qm.select_user(telename):  # Check if user alr exists
            return {
                "code": 405,
                "message": "User Creation Failed: User already Exists",
                "data": None
                }
        self.qm.insert_user(availability, telename, age, gender)
        return {
            "code": 200,
            "message": "User Successfully Created",
            "data": None
            }
    
    def get_user_id(self, telename):
        # if invalid telename, user_id = []
        user_id = self.qm.get_user_id(telename)
        if not user_id:
            return {
                "code": 404, 
                "message": f"invalid user: {telename}",
                "data": None
            }
        else:
            return {
                "code": 200, 
                "message": f"{telename}'s user id obtained",
                "data": user_id[0][0]
            }
        
    
    def get_user_info(self, telename, column, table):
        # if invalid telename, user_id = []
        user_info = self.qm.get_user_info(telename, column, table)
        if len(user_info) == 0:
            return {
                "code": 404, 
                "message": f"invalid user: {telename}",
                "data": None
            }
        return user_info[0][0]
    
    def show_profile(self, telename):
        # check if valid telename  
        user_id = self.get_user_id(telename)
        if not user_id["data"]:
            return user_id
        else:
            user_id = user_id["data"]
        
        age = self.get_user_info(telename, "age_ref_id", "users")
        gender = self.get_user_info(telename, "gender_ref_id", "users")
        age_pref = self.qm.select_pref(user_id,  "age_ref", "age_ref_id")
        gender_pref = self.qm.select_pref(user_id,  "gender_ref", "gender_ref_id")
        cuisine_pref = self.qm.select_pref(user_id,  "cuisine_ref", "cuisine_ref_id")
        diet_pref = self.qm.select_pref(user_id,  "diet_ref", "diet_ref_id")
        return {
            "code": 200,
            "message": "profile successfully acquired",
            "data": {
            "telename": telename,
            "age": age,
            "gender": gender,
            "age pref": [pref[0] for pref in age_pref],
            "gender pref": [pref[0] for pref in gender_pref],
            "cuisine pref": [pref[0] for pref in cuisine_pref],
            "diet pref": [pref[0] for pref in diet_pref]
            }
        }
    
    # CHOICE
    def show_choices_template(self, column, table):
        choices = self.qm.get_info(column, table)
        return [choice[0] for choice in choices]
    
    def show_one_choice(self, column, table):
        choices = self.qm.get_info(column, table)
        return {
            "code": 200,
            "message": f"{table} choices shown",
            "data": {
            table: self.show_choices_template(column, table)
            }
        }

    def show_all_choices(self):
        return {
            "code": 200,
            "message": "all choices shown",
            "data": {
            "age": self.show_choices_template("age_range", "age"),
            "gender": self.show_choices_template("gender", "gender"),
            "cuisine": self.show_choices_template("cuisine", "cuisine"),
            "diet": self.show_choices_template("diet_res_type", "diet")            
            }
        }
    
    # PREFERENCE
    def select_pref(self, telename, column, table):
        # check if valid telename  
        user_id = self.get_user_id(telename)
        if not user_id["data"]:
            return user_id
        else:
            user_id = user_id["data"]
        
        return {
            "code": 200,
            "message": f"successfully selected {table[:-4]} preferences",
            "data": [pref[0] for pref in self.qm.select_pref(user_id, column, table)]
        }

    
    def change_pref(self, telename, new_pref, column, table, adding, deleting):
        # check if valid telename        
        user_id = self.get_user_id(telename)
        if not user_id["data"]:
            return user_id
        else:
            user_id = user_id["data"]

        # check if valid preference
        map_table = table[:-4]
        map_column = f"{map_table}_id"
        map_result_tuple = self.qm.get_info(map_column, map_table)
        map_result_list = [result[0] for result in map_result_tuple]
        for pref in new_pref:
            if pref not in map_result_list:
                return {
                    "code": 404,
                    "message": "invalid preference",
                    "data": pref
                }       

        # select old pref type list[tuple]
        old_pref = self.qm.select_pref(user_id, column, table)
        old_pref = [pref[0] for pref in old_pref]

        addpref = []
        dltpref = []
        finalpref = []

        for pref in new_pref:
                if pref not in old_pref:
                    addpref.append(pref)
        
        if adding and not deleting:
            for each_pref in addpref:
                self.qm.add_pref(user_id, each_pref, table)
            finalpref = list(set(old_pref + new_pref))
            return {
                "code": 201,
                "message" : f"{table} preferences successfully updated",
                "data" : {
                "pref type": table[:-4], 
                "old prefs": old_pref, 
                "added prefs": addpref, 
                "new prefs": finalpref
                }
            }

        elif deleting and not adding:
            for pref in old_pref:
                if pref in new_pref:
                    dltpref.append(pref)
                else:
                    finalpref.append(pref)
            if dltpref:
                self.qm.dlt_pref(user_id, tuple(dltpref), column, table)
            return {
                "code": 201,
                "message" : f"{table} preferences successfully updated",
                "data" : {
                "pref type": table[:-4], 
                "old prefs": old_pref, 
                "deleted prefs": dltpref, 
                "new prefs": finalpref
                }
            }

        elif adding and deleting:
            for pref in old_pref:
                if pref not in new_pref:
                    dltpref.append(pref)
            for each_pref in addpref:
                self.qm.add_pref(user_id, each_pref, table)
            if dltpref:
                self.qm.dlt_pref(user_id, tuple(dltpref), column, table)
            return {
                "code": 201,
                "message" : f"{table} preferences successfully updated",
                "data" : {
                "pref type": table[:-4], 
                "old prefs": old_pref, 
                "added prefs": addpref, 
                "deleted prefs": dltpref, 
                "new prefs": new_pref
                }
            }


    # QUEUE
    def queue(self, telename):
        # check if valid telename  
        user_id = self.get_user_id(telename)
        if not user_id["data"]:
            return user_id
        else:
            user_id = user_id["data"]

        # check if user already in queue
        user_id_queued = self.qm.get_info("user_id", "queue")
        user_id_queued_list = [user_id[0] for user_id in user_id_queued]
        if user_id in user_id_queued_list:
            return {
            "code": 404,
            "message": f"{telename} already in queue",
            "data": None
        }

        self.qm.queue(user_id)
        return {
            "code": 200,
            "message": f"{telename} successfully queued",
            "data": None
        }
    
    def dequeue(self, telename):
        # check if valid telename  
        user_id = self.get_user_id(telename)
        if not user_id["data"]:
            return user_id
        else:
            user_id = user_id["data"]

        self.qm.dequeue(user_id)
        return {
            "code": 200,
            "message": f"{telename} successfully dequeued",
            "data": None
        }

    # MATCH
    def person_match(self, telename):
        # check if valid telename  
        user_id = self.get_user_id(telename)
        if not user_id["data"]:
            return user_id
        else:
            user_id = user_id["data"]

        age_pref = self.qm.select_pref(user_id, "age_ref_id", "age_ref")
        gender_pref = self.qm.select_pref(user_id, "gender_ref_id", "gender_ref")
        queue_users = self.qm.select_queue_users()

        if not age_pref:
            age_pref = [1,2,3,4,5,6]       # populate with all choices
        if not gender_pref:
            gender_pref = [1,2,3]    # populate with all choices

        matches_A = self.qm.person_match_A(user_id, age_pref, gender_pref)

        primary_age = self.qm.get_user_info(telename, "age_ref_id", "users")[0][0]
        primary_gender = self.qm.get_user_info(telename, "gender_ref_id", "users")[0][0]

        matches_B = self.qm.person_match_B(matches_A, primary_age, primary_gender)

        if matches_B:
            return {
                "code": 200,
                "message": "matches found",
                "data": matches_B
            }
        else:
            self.queue(user_id)
            return {
                "code": 200,
                "message": "no matches found; user added to queue list",
                "data": None
            }

    