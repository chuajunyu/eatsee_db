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
                "message": "User creation failed: User already exists.",
                "data": None
                }
        self.qm.insert_user(availability, telename, age, gender)
        return {
            "code": 200,
            "message": f"User {telename} successfully created.",
            "data": None
            }
    
    def get_user_id(self, telename):
        # if invalid telename, user_id = []
        user_id = self.qm.get_user_id(telename)
        if not user_id:
            return {
                "code": 404, 
                "message": f"invalid user: {telename}.",
                "data": None
            }
        else:
            return {
                "code": 200, 
                "message": f"{telename}'s user id obtained.",
                "data": user_id[0]
            }
        
    
    def get_user_info(self, telename, column, table):
        # if invalid telename, user_id = []
        user_info = self.qm.get_user_info(telename, column, table)
        if len(user_info) == 0:
            return {
                "code": 404, 
                "message": f"Invalid user: {telename}.",
                "data": None
            }
        return user_info
    
    def show_profile(self, telename):
        # check if valid telename  
        user_id = self.get_user_id(telename)
        if not user_id["data"]:
            return user_id
        else:
            user_id = user_id["data"]["user_id"]
        
        age = self.get_user_info(telename, "age_ref_id", "users")[0]["age_ref_id"]
        gender = self.get_user_info(telename, "gender_ref_id", "users")[0]["gender_ref_id"]
        age_pref = self.qm.select_pref(user_id, "age_ref_id",  "age_ref")
        gender_pref = self.qm.select_pref(user_id, "gender_ref_id", "gender_ref")
        cuisine_pref = self.qm.select_pref(user_id, "cuisine_ref_id", "cuisine_ref")
        diet_pref = self.qm.select_pref(user_id, "diet_ref_id", "diet_ref")
        return {
            "code": 200,
            "message": "Profile successfully acquired.",
            "data": {
            "telename": telename,
            "age": age,
            "gender": gender,
            "age pref": [pref["age_ref_id"] for pref in age_pref],
            "gender pref": [pref["gender_ref_id"] for pref in gender_pref],
            "cuisine pref": [pref["cuisine_ref_id"] for pref in cuisine_pref],
            "diet pref": [pref["diet_ref_id"] for pref in diet_pref]
            }
        }
    
    # CHOICE
    def show_choices_template(self, column, table):
        choices = self.qm.get_info(column, table)
        return [row[column] for row in choices]
    
    def show_one_choice(self, column, table):
        return {
            "code": 200,
            "message": f"{table} choices shown.",
            "data": {
            table: self.show_choices_template(column, table)
            }
        }

    def show_all_choices(self):
        return {
            "code": 200,
            "message": "All choices shown.",
            "data": {
            "age": self.show_choices_template("age_range", "age"),
            "gender": self.show_choices_template("gender", "gender"),
            "cuisine": self.show_choices_template("cuisine", "cuisine"),
            "diet": self.show_choices_template("diet_res_type", "diet")            
            }
        }
    
    # USER CHARACTERISTIC
    def change_user_info(self, telename, value, column, msg_type):
        self.qm.update_user_info(telename, value, column)
        return {
            "code": 200,
            "message": f"{telename}'s {msg_type} updated to {value}.",
            "data": None
        }
    
    
    # PREFERENCE
    def select_pref(self, telename, column, table):
        # check if valid telename  
        user_id = self.get_user_id(telename)
        if not user_id["data"]:
            return user_id
        else:
            user_id = user_id["data"]["user_id"]
        
        return {
            "code": 200,
            "message": f"Successfully selected {table[:-4]} preferences.",
            "data": [row[column] for row in self.qm.select_pref(user_id, column, table)]
        }

    
    def change_pref(self, telename, new_pref, column, table, adding, deleting):
        # check if valid telename  
        user_id = self.get_user_id(telename)
        if not user_id["data"]:
            return user_id
        else:
            user_id = user_id["data"]["user_id"]

        # check if valid preference
        map_table = table[:-4]
        map_column = f"{map_table}_id"
        map_result_tuple = self.qm.get_info(map_column, map_table)
        map_result_list = [row[map_column] for row in map_result_tuple]
        for pref in new_pref:
            if pref not in map_result_list:
                return {
                    "code": 404,
                    "message": "Invalid preference input.",
                    "data": pref
                }       

        # select old pref type list[tuple]
        old_pref = self.qm.select_pref(user_id, column, table)
        old_pref = [row[column] for row in old_pref]

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
                "message" : f"{table} preferences successfully updated.",
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
                "message" : f"{table} preferences successfully updated.",
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
                "message" : f"{table} preferences successfully updated.",
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
            user_id = user_id["data"]["user_id"]

        # check if user already in queue
        user_id_queued = self.qm.get_info("user_id", "queue")
        user_id_queued_list = [row["user_id"] for row in user_id_queued]
        if user_id in user_id_queued_list:
            return {
            "code": 404,
            "message": f"{telename} already in queue.",
            "data": None
        }

        self.qm.queue(user_id)
        return {
            "code": 200,
            "message": f"{telename} successfully queued.",
            "data": None
        }
    
    def dequeue(self, telename):
        # check if valid telename  
        user_id = self.get_user_id(telename)
        if not user_id["data"]:
            return user_id
        else:
            user_id = user_id["data"]["user_id"]

        self.qm.dequeue(user_id)
        return {
            "code": 200,
            "message": f"{telename} successfully dequeued.",
            "data": None
        }

    # MATCH
    def person_match(self, telename):
        # check if valid telename  
        user_id = self.get_user_id(telename)
        if not user_id["data"]:
            return user_id
        else:
            user_id = user_id["data"]["user_id"]

        # Match A

        age_pref = self.qm.select_pref(user_id, "age_ref_id", "age_ref")
        age_pref = [row["age_ref_id"] for row in age_pref]
        gender_pref = self.qm.select_pref(user_id, "gender_ref_id", "gender_ref")
        gender_pref = [row["gender_ref_id"] for row in gender_pref]
        queue_users = self.qm.select_queue_users()

        if not age_pref:
            age_pref = [1,2,3,4,5,6]       # populate with all choices
        if not gender_pref:
            gender_pref = [1,2,3]    # populate with all choices

        matches_A = self.qm.person_match_A(user_id, age_pref, gender_pref)
        matches_A = [row["user_id"] for row in matches_A]
        if not matches_A:
            self.queue(telename)
            return {
                "code": 404,
                "message": "No matches found. User added to queue list.",
                "data": "matches_A empty"
            }
        
        # Match B

        primary_age = self.qm.get_user_info(telename, "age_ref_id", "users")[0]["age_ref_id"]
        primary_gender = self.qm.get_user_info(telename, "gender_ref_id", "users")[0]["gender_ref_id"]

        matches_B = self.qm.person_match_B(matches_A, primary_age, primary_gender)
        matches_B = [row["user_ref_id"] for row in matches_B]
        if not matches_B:
            self.queue(telename)
            return {
                "code": 404,
                "message": "No matches found. User added to queue list.",
                "data": "matches_B empty"
            }
        
        # Match C
        
        cuisine_pref = self.qm.select_pref(user_id, "cuisine_ref_id", "cuisine_ref")
        cuisine_pref = [row["cuisine_ref_id"] for row in cuisine_pref]
        diet_pref = self.qm.select_pref(user_id, "diet_ref_id", "diet_ref")
        diet_pref = [row["diet_ref_id"] for row in diet_pref]

        if not cuisine_pref:
            cuisine_pref = [1,2,3,4,5,6,7,8]    # populate with all choices

        matches_C = self.qm.person_match_cuisine(matches_B, cuisine_pref)
        matches_C = [row["user_ref_id"] for row in matches_C]

        if not matches_C:
            self.queue(telename)
            return {
                "code": 404,
                "message": "No matches found. User added to queue list.",
                "data": "matches_C empty"
            }

        if not diet_pref:
                return {
                        "code": 200,
                        "message": "Match found",
                        "data": matches_C
                    }
        
        # Match D
        
        else:
            diet_dict = {
            "Halal": 1,
            "No Halal": 2,
            "Vegetarian": 3,
            "No Vegetarian": 4,
            "Vegan": 5,
            "No Vegan": 6
            }

            diet_pref_blacklist = []
            for pref in diet_pref:
                if pref%2 == 1:
                    diet_pref_blacklist.append(pref+1)
            else:
                diet_pref_blacklist.append(pref-1)
            
            matches_D_blacklist = self.qm.person_match_dietBlacklist(matches_C, diet_pref_blacklist)
            matches_D_blacklist = [row["user_ref_id"] for row in matches_D_blacklist]

            if not matches_D_blacklist:
                return {
                        "code": 200,
                        "message": "Match found",
                        "data": matches_C
                    }
            else:
                matches_D = []
                for match in matches_C:
                    if match not in matches_D_blacklist:
                        matches_D.append(match)

                if not matches_D:
                    return {
                        "code": 404,
                        "message": "No matches found. User added to queue list.",
                        "data": "matches_D empty"
                    }
                else:
                    return {
                        "code": 200,
                        "message": "Match found",
                        "data": matches_D
                    }
                

    # DELETE ACCOUNT because no love
    def delete_user(self, telename):
        # check if valid telename  
        user_id = self.get_user_id(telename)
        if not user_id["data"]:
            return user_id
        else:
            user_id = user_id["data"]["user_id"]

        user_id = [user_id]

        self.qm.delete_user(user_id, "user_ref_id", "age_ref")
        self.qm.delete_user(user_id, "user_ref_id", "gender_ref")
        self.qm.delete_user(user_id, "user_ref_id", "cuisine_ref")
        self.qm.delete_user(user_id, "user_ref_id", "diet_ref")
        self.qm.delete_user(user_id, "user_id", "queue")
        self.qm.delete_user(user_id, "user_id", "chat")
        self.qm.delete_user(user_id, "user_id", "users")

        return {
                "code": 200,
                "message": f"User {telename} has been deleted. Goodbye.",
                "data": None
            }