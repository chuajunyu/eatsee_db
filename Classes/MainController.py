from .QueryManager import QueryManager
from res_stuff.find_res_optim import *

class MainController:
    """
    Handles the logic and calls the relevant queries using QueryManager
    to provide the services of the API Endpoints.
    """
    def __init__(self):
        self.qm = QueryManager()

    def select_user(self, user_id: int):
        """
        Returns a list of users from database with that telegram name.
        By right, there should only be one user.

        Input:
            - telename: Telegram username to search for

        Returns:
            - List containing users with that telename.
        """
        print(self.qm.select_user(user_id))
        return self.qm.select_user(user_id)

    def insert_user(self, user_id: int, telename: str, age: int, gender: int):
        """
        Inserts a user into the database
        
        Input:
            - availability: Boolean value describing availability of user 
                            (Might be deprecated)
            - telename:     Telegram username of new user to be inserted

        Return:
            - Dictionary containing message
        """
        if self.qm.select_user(user_id):  # Check if user alr exists
            return {
                "code": 405,
                "message": "User creation failed: User already exists.",
                "data": None
                }
        self.qm.insert_user(user_id, telename, age, gender)
        return {
            "code": 200,
            "message": f"User {telename} successfully created.",
            "data": None
            }
    
    def get_user_id(self, telename: str):
        """
        Obtains user's id
        
        Input:
            - telename: Telegram username of new user to be inserted

        Return:
            - user_id = return["data"]["user_id"]
        """

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
                "message": f"{telename}'s user id obtained.",
                "data": user_id[0]
            }
    
    def get_user_info(self, user_id: int, select_column: str, table: str ="users", user_id_column: str ="user_id"):
        """
        Obtains user's info(s)
        
        Input:
            - user_id:        user's id
            - select_column:  target column(s) (e.g. "age_ref_id, gender_ref_id" for multiple columns)
            - table:          target table (default = "users")
            - user_id_column: column containing user's id (default = "user_id")
              
            some tables require different user_id_column (i.e. table = "age_ref", user_id_column = "user_ref_id")

        Return:
            - List of dictionaries containing "column name": column value, 
              len(List) = number of rows selected from SQL
        """

        user_info = self.qm.get_user_info(user_id, select_column, table, user_id_column)
        if len(user_info) == 0:
            return {
                "code": 404, 
                "message": "User not found.",
                "data": None
            }
        return user_info
    
    def show_profile(self, user_id: int):
        """
        Obtains user's profile
        
        Input:
            - user_id: user's id

        Return:
            - user_id
            - telename
            - age
            - gender
            - preferences (x4)
        """
        
        telename = self.get_user_info(user_id, "telename")[0]["telename"]
        age = self.get_user_info(user_id, "age_ref_id", "users")[0]["age_ref_id"]
        gender = self.get_user_info(user_id, "gender_ref_id", "users")[0]["gender_ref_id"]
        age_pref = self.qm.select_pref(user_id, "age_ref_id",  "age_ref")
        gender_pref = self.qm.select_pref(user_id, "gender_ref_id", "gender_ref")
        pax_pref = self.qm.select_pref(user_id, "pax_ref_id", "pax_ref")
        cuisine_pref = self.qm.select_pref(user_id, "cuisine_ref_id", "cuisine_ref")
        diet_pref = self.qm.select_pref(user_id, "diet_ref_id", "diet_ref")
        return {
            "code": 200,
            "message": "Profile successfully acquired.",
            "data": {
                "user_id": user_id,
                "telename": telename,
                "age": age,
                "gender": gender,
                "age pref": [pref["age_ref_id"] for pref in age_pref],
                "gender pref": [pref["gender_ref_id"] for pref in gender_pref],
                "pax pref": [pref["pax_ref_id"] for pref in pax_pref],
                "cuisine pref": [pref["cuisine_ref_id"] for pref in cuisine_pref],
                "diet pref": [pref["diet_ref_id"] for pref in diet_pref]
            }
        }


    # CHOICE
    def show_choices_template(self, column1: str, column2: str, table: str):
        """
        Obtains user's profile
        
        Input:
            - column1: preference_id
            - column2: preference_type

        Return:
            Dictionary containing preference_id: preference_type for each preference choice
        """

        choices = self.qm.get_info("*", table)
        dict_choice = {}
        for row in choices:
            dict_choice[row[column1]] = row[column2]
        return dict_choice
    
    def show_one_choice(self, column1: str, column2: str, table: str):
        """
        see show_choices_template()
        """

        return {
            "code": 200,
            "message": f"{table} choices shown.",
            "data": {
            table: self.show_choices_template(column1, column2, table)
            }
        }

    def show_all_choices(self):
        """
        see show_choices_template()
        """

        return {
            "code": 200,
            "message": "All choices shown.",
            "data": {
            "age": self.show_choices_template("age_id", "age_range", "age"),
            "gender": self.show_choices_template("gender_id", "gender", "gender"),
            "cuisine": self.show_choices_template("cuisine_id", "cuisine", "cuisine"),
            "diet": self.show_choices_template("diet_id", "diet_res_type", "diet"),
            "pax": self.show_choices_template("pax_id", "pax_number", "pax")
            }
        }


    # USER CHARACTERISTIC
    def change_user_info(self, user_id: int, value: int or str, column: str, msg_type: str):
        """
        Changes user's info in "users" Table
        
        Input:
            - user_id:  user's id
            - value:    new value
            - column:   target info column
            - msg_type: what kind of info updated (for return["message"] purpose)

        Return:
            Dictionary["message"] shows whose info updated to which new value
        """

        telename = self.get_user_info(user_id, "telename")[0]["telename"]
        self.qm.update_user_info(user_id, value, column)
        return {
            "code": 200,
            "message": f"{telename}'s {msg_type} updated to {value}.",
            "data": None
        }
    
    
    # PREFERENCE
    def select_pref(self, user_id: int, column: str, table: str):
        """
        Obtains user's existing preferences
        
        Input:
            - user_id: user's id
            - column:  "{preference type}_ref_id"
            - table:   "{preference_type}_ref"

        Return:
            Dictionary["data"] = List of user's existing preference_id
        """

        return {
            "code": 200,
            "message": f"Successfully selected {table[:-4]} preferences.",
            "data": [row[column] for row in self.qm.select_pref(user_id, column, table)]
        }

    
    def change_pref(self, user_id: int, new_pref: list, column: str, table: str, adding: bool, deleting: bool):
        """
        Change user's preferences
        
        Input:
            - user_id:  user's id
            - new_pref: list of preference_ids to add/delete/change_to
            - column:   "{preference type}_ref_id"
            - table:    "{preference_type}_ref"
            - adding:   True if either adding/changing_to,   False if deleting prefs
            - deleting: True is either deleting/changing_to, False if adding prefs

        Return:
            if invalid preferences:
                Dictionary["data"] = List of invalid preferences

            if valid preferences:
                Dictionary["data"]:
                    ["pref type"]
                    ["old prefs"]
                    ["added prefs"]
                    ["deleted prefs"]
                    ["new prefs"]
        """
        
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
        old_pref = sorted([row[column] for row in old_pref])

        addpref = []
        dltpref = []
        finalpref = []

        for pref in new_pref:
                if pref not in old_pref:
                    addpref.append(pref)
        addpref.sort()
        
        if adding and not deleting:
            if addpref:
                self.qm.add_multiple_prefs(user_id, addpref, column, table)
            dltpref = None
            finalpref = sorted(list(set(old_pref + new_pref)))

        elif deleting and not adding:
            for pref in old_pref:
                if pref in new_pref:
                    dltpref.append(pref)
                else:
                    finalpref.append(pref)
            if dltpref:
                self.qm.dlt_pref(user_id, dltpref, column, table)
            addpref = None
            finalpref.sort()

        elif adding and deleting:
            for pref in old_pref:
                if pref not in new_pref:
                    dltpref.append(pref)
            if addpref:
                self.qm.add_multiple_prefs(user_id, addpref, column, table)
            if dltpref:
                self.qm.dlt_pref(user_id, dltpref, column, table)
            finalpref = sorted(new_pref)
            
        return {
                "code": 200,
                "message" : f"{table} preferences successfully updated.",
                "data" : {
                "pref type": table[:-4], 
                "old prefs": old_pref, 
                "added prefs": addpref, 
                "deleted prefs": dltpref, 
                "new prefs": finalpref
                }
            }
    
    # CHECK TABLES FOR USERS
    def check_table_for_user(self, user_id: int, table: str, user_id_column: str ="user_id"):
        """
        Check if user exists in table
        
        Input:
            - user_id:        user's id
            - table:          table
            - user_id_column: default = "user_id"

        Return:
            Dictionary["data"] = True if user in Table, False if user not in Table
        """

        if len(self.qm.get_user_info(user_id, "*", table, user_id_column)) == 1:
            return {
                "code": 200,
                "message": f"User found in {table}",
                "data": True
            }
        else:
            return {
                "code": 404,
                "message": f"User not found in {table}",
                "data": False
            }


    # QUEUE
    def queued_users(self):
        """
        Obtains user_ids of queued users
        
        Input:
            No input

        Return:
            Dictionary["data"] = list of user_ids in queue
        """
        
        # check if user already in queue
        user_id_queued = self.qm.get_info("user_id", "queue")
        user_id_queued_list = [row["user_id"] for row in user_id_queued]
        return {
            "code": 200,
            "message": "Successfully obtained user_ids currently in queue.",
            "data": user_id_queued_list
        }
    
    def queue(self, user_id: int):
        """
        Adds user to queue
        
        Input:
            - user_id: user's id

        Return:
            Dictionary["code"] = 200 if user successfully queued, 404 if user already in queue
        """

        telename = self.get_user_info(user_id, "telename")[0]["telename"]
        user_id_queued_list = self.queued_users()["data"]

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
    
    def dequeue(self, user_id: int):
        """
        Removes user from queue
        
        Input:
            - user_id: user's id

        Return:
            Dictionary["code"] = 200 if user successfully dequeued
        """

        telename = self.get_user_info(user_id, "telename")[0]["telename"]
        self.qm.dequeue(user_id)
        return {
            "code": 200,
            "message": f"{telename} successfully dequeued.",
            "data": None
        }

    # MATCH
    def person_match(self, user_id: int):
        """
        Adds user to queue
        
        Input:
            - user_id: user's id

        Return:
            Dictionary["code"] = 200 if user successfully queued, 404 if user already in queue.
            Dictionary["data"] = {"user_ids and telenames found": list(tuple(user_id1, telename1), tuple(user_id2, telename2), ...),    # 1 tuple for each compatible user found
                                  "user_id_list":                 list(user_id1, user_id2, ...),                                        # including Main user's user_id
                                  "chatroom":                     int(chatroom_id)}
        """

        telename = self.get_user_info(user_id, "telename")[0]["telename"]

        # Match A: find users who satisfy Main user's age and gender preferences

        age_pref = self.qm.select_pref(user_id, "age_ref_id", "age_ref")
        age_pref = [row["age_ref_id"] for row in age_pref]
        gender_pref = self.qm.select_pref(user_id, "gender_ref_id", "gender_ref")
        gender_pref = [row["gender_ref_id"] for row in gender_pref]

        if not age_pref:
            age_pref = [1,2,3,4,5,6]       # populate with all choices
        if not gender_pref:
            gender_pref = [1,2,3]    # populate with all choices

        matches_A = self.qm.person_match_A(user_id, age_pref, gender_pref)
        matches_A = [row["user_id"] for row in matches_A]
        if not matches_A:
            self.queue(user_id)
            return {
                "code": 404,
                "message": "No matches found. User added to queue list.",
                "data": "matches_A empty"
            }
        
        # Match B: find users who prefers Main user's age and gender

        primary_age = self.qm.get_user_info(user_id, "age_ref_id", "users")[0]["age_ref_id"]
        primary_gender = self.qm.get_user_info(user_id, "gender_ref_id", "users")[0]["gender_ref_id"]

        matches_B = self.qm.person_match_B(matches_A, primary_age, primary_gender)
        matches_B = [row["user_ref_id"] for row in matches_B]
        if not matches_B:
            self.queue(user_id)
            return {
                "code": 404,
                "message": "No matches found. User added to queue list.",
                "data": "matches_B empty"
            }
        
        # Match C: find users with same cuisine prefrences as Main user
        
        cuisine_pref = self.qm.select_pref(user_id, "cuisine_ref_id", "cuisine_ref")
        cuisine_pref = [row["cuisine_ref_id"] for row in cuisine_pref]
        diet_pref = self.qm.select_pref(user_id, "diet_ref_id", "diet_ref")
        diet_pref = [row["diet_ref_id"] for row in diet_pref]
        pax_pref = self.qm.select_pref(user_id, "pax_ref_id", "pax_ref")
        pax_pref = [row["pax_ref_id"] for row in pax_pref]


        matches_C = self.qm.person_match_cuisine(matches_B, cuisine_pref)
        matches_C = [row["user_ref_id"] for row in matches_C]

        if not matches_C:
            self.queue(user_id)
            return {
                "code": 404,
                "message": "No matches found. User added to queue list.",
                "data": "matches_C empty"
            }

        if not diet_pref:
            penultimate_matches = matches_C
        
        # Match D: blacklist users who have opposing dietary requirements from Main user
        
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

            if matches_D_blacklist:
                matches_D = []
                for match in matches_C:
                    if match not in matches_D_blacklist:
                        matches_D.append(match)

                if not matches_D:
                    self.queue(user_id)
                    return {
                        "code": 404,
                        "message": "No matches found. User added to queue list.",
                        "data": "matches_D empty"
                    }
                else:
                    penultimate_matches = matches_D
        
        # Match P: find users with same pax preferences as Main user

        matches_P = self.qm.person_match_pax(penultimate_matches, pax_pref)
        if not matches_P:
            self.queue(user_id)
            return {
                        "code": 404,
                        "message": "No matches found. User added to queue list.",
                        "data": "matches_P empty"
            }

        matches_P_users = []
        matches_P_paxes = []
        final_matches = []

        for row in matches_P:
            matches_P_users.append(row["user_ref_id"])
            matches_P_paxes.append(row["pax_ref_id"])

        current_user_id = matches_P_users[0]
        matches_P_user_id_list = [current_user_id]
        for each_user_id in matches_P_users:
            if current_user_id != each_user_id:
                matches_P_user_id_list.append(each_user_id)
                current_user_id = each_user_id

        final_pax = 0
        matches_P_paxes.sort(reverse=True)
        for each_pax in matches_P_paxes:
            if matches_P_paxes.count(each_pax) >= each_pax-1:
                final_pax = each_pax
                break
        
        if final_pax == 0:
            self.queue(user_id)
            return {
                        "code": 404,
                        "message": "No matches found. User added to queue list.",
                        "data": "matches_P empty"
            }
        
        counter = 1
        for row in matches_P:
            if row["pax_ref_id"] == final_pax and counter < final_pax:
                counter += 1
                final_matches.append(row["user_ref_id"])
                print(final_matches)

        final_id_and_names = [(match_id, self.qm.get_user_telename(match_id)[0]["telename"]) for match_id in final_matches]
        matches_P_user_id_list_final = matches_P_user_id_list[:final_pax-1]
        matches_P_user_id_list_final.append(user_id)
        add_chatroom_user_info = self.add_chatroom_user(matches_P_user_id_list_final)
        self.qm.dequeue(matches_P_user_id_list_final)

        return {
            "code": 200,
            "message": "Match found. Dequeued users and added them to chatroom.",
            "data": {"user_ids and telenames found": final_id_and_names,
                     "user_id_list": add_chatroom_user_info["data"]["user_id_list"],
                     "chatroom": add_chatroom_user_info["data"]["chatroom_id"]
            }
        }
    
    # CHATROOM
    def add_chatroom_user(self, user_id_list: list):
        """
        Adds list of users to chatroom
        
        Input:
            - user_id_list: list of user_ids

        Return:
            Dictionary["data"] = {"user_id_list": list of user_ids added to chatroom,
                                  "chatroom_id":  int(chatroom_id)}
        """

        chatroom_id = self.qm.get_chatroom_id()[0]["max"]
        if not chatroom_id:
            chatroom_id = 1
        else:
            chatroom_id += 1
        self.qm.delete_chatroom_user(user_id_list)
        self.qm.add_chatroom_user(chatroom_id, user_id_list)
        user_telename_dict = self.qm.get_user_telename(user_id_list)
        user_telename_list = [row["telename"] for row in user_telename_dict]
        user_telename_str = str(user_telename_list)[1:-1]
        return {
                "code": 200,
                "message": f"Users {user_telename_str} successfully added to Chatroom {chatroom_id}.",
                "data": {
                    "user_id_list": user_id_list,
                    "chatroom_id": chatroom_id
                }
            }

    def delete_chatroom_user(self, user_id_list: list):
        """
        Removes list of users from chatroom
        
        Input:
            - user_id_list: list of user_ids

        Return:
            Dictionary["data"] = {"user_id_list": list of user_ids removed from chatroom}
        """

        user_telename_dict = self.qm.get_user_telename(user_id_list)
        user_telename_list = [row["telename"] for row in user_telename_dict]
        user_telename_str = str(user_telename_list)[1:-1]
        self.qm.delete_chatroom_user(user_id_list)
        return {
                "code": 200,
                "message": f"Users {user_telename_str} successfully deleted from Chatroom.",
                "data": {
                    "user_id_list": user_id_list,
                }
            }
    
    def select_chatroom_user(self, chatroom_id: int):
        """
        Obtains list of users from chatroom
        
        Input:
            - chatroom_id: int(chatroom_id)

        Return:
            Dictionary["code"] = 200 if users found in Chatroom, 404 if no users found
            Dictionary["data"] = {"user_id_list": list of user_ids found in specified Chatroom}    # None if code = 404
        """

        record = self.qm.select_chatroom_user(chatroom_id)
        if not record:
            return {
                "code": 404,
                "message": f"No users in Chatroom {chatroom_id}",
                "data": None
            }
        user_id_list = [row["user_id"] for row in record]
        return {
                "code": 200,
                "message": f"Successfully selected user_id from Chatroom {chatroom_id}.",
                "data": user_id_list
            } 
    
    def select_chatroom(self, user_id: int):
        """
        Obtains chatroom_id which user is in
        
        Input:
            - user_id: int(user_id)

        Return:
            Dictionary["code"] = 200 if user found in Chatroom, 404 if user not in Chatroom
            Dictionary["data"] = {"chatroom_id": int(chatroom_id)}    # None if code = 404
        """

        record = self.qm.select_chatroom(user_id)
        if not record:
            return {
                "code": 404,
                "message": "User not in Chatroom",
                "data": None
            }

        chatroom_id = record[0]["chatroom_id"]
        return {
                "code": 200,
                "message": f"Successfully selected chatroom_id {chatroom_id}.",
                "data": chatroom_id
            }
    
    def find_restaurant(self, coordinates: list, distance: int, white_cuisine: list, white_diet: list, black_cuisine_diet: list, include_all_cuisine: bool):
        pass

    # DELETE ACCOUNT because no love
    def delete_user(self, user_id: int or list):
        """
        Deletes user
        
        Input:
            - user_id: int(user_id)

        Return:
            Dictionary["code"] = 200 if user successfully deleted user(s)
        """
        if isinstance(user_id, int):
            user_id = [user_id]

        telename = ""
        for each_user_id in user_id:
            telename += self.get_user_info(each_user_id, "telename")[0]["telename"]
            telename += ", "

        self.qm.delete_user(user_id, "user_ref_id", "age_ref")
        self.qm.delete_user(user_id, "user_ref_id", "gender_ref")
        self.qm.delete_user(user_id, "user_ref_id", "cuisine_ref")
        self.qm.delete_user(user_id, "user_ref_id", "diet_ref")
        self.qm.delete_user(user_id, "user_id", "queue")
        self.qm.delete_user(user_id, "user_id", "chat")
        self.qm.delete_user(user_id, "user_id", "users")

        return {
                "code": 200,
                "message": f"User {telename[:-2]} successfully deleted. Goodbye.",
                "data": None
            }

    def test_function(self):
        return {
            'code': 200,
            'data': find_res_optim()
        }