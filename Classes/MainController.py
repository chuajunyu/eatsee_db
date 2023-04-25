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
                "message": "User Creation Failed: User already Exists"
                }
        self.qm.insert_user(availability, telename, age, gender)
        return {
            "code": 200,
            "message": "User Successfully Created"
            }
    
    def get_user_id(self, telename):
        # if invalid telename, user_id = []
        user_id = self.qm.get_user_id(telename)
        if len(user_id) == 0:
            return {
                "code": 404, 
                "message": f"invalid user: {telename}"
            }
        # if user_id is not Integer
        if not isinstance(user_id[0][0], int):
            return {
                "code": 404, 
                "message": f"invalid user id: {user_id}"
            }
        return {
            "code": 200,
            "message": f"user_id successfully returned",
            "data": user_id[0][0]
        }
    
    def get_user_info(self, telename, column, table):
        # if invalid telename, user_id = []
        user_info = self.qm.get_user_info(telename, column, table)
        if len(user_info) == 0:
            return {
                "code": 404, 
                "message": f"invalid user: {telename}"
            }
        return user_info[0][0]
    
    def show_profile(self, telename):
        user_id = self.qm.get_user_id(telename)[0][0]
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
    
    def show_choices(self, column, table):
        choices = self.qm.get_info(column, table)
        return [choice[0] for choice in choices]

    def show_all_choices(self):
        return {
            "age": self.show_choices("age_range", "age"),
            "gender": self.show_choices("gender", "gender"),
            "cuisine": self.show_choices("cuisine", "cuisine"),
            "diet": self.show_choices("diet_res_type", "diet"),
        }
    
    def select_pref(self, telename, table, column):
        user_id = self.get_user_id(telename)
        return self.qm.select_pref(user_id, table, column)
    
    def change_pref(self, telename, new_pref, table, column):
        # get user_id
        user_id = self.get_user_id(telename)
        # returns error if invalid telename or invalid user id
        if not isinstance(user_id, int):
            return user_id

        # select old pref type list[tuple]
        old_pref = self.qm.select_pref(user_id, table, column)
        old_pref = [pref[0] for pref in old_pref]

        dltpref = []
        addpref = []

        for pref_id in old_pref:
            if pref_id not in new_pref:
                dltpref.append(pref_id)

        for pref_id in new_pref:
            if pref_id not in old_pref:
                addpref.append(pref_id)

        if dltpref:
            self.qm.dlt_pref(user_id, tuple(dltpref), table, column)

        for each_pref in addpref:
            self.qm.add_pref(user_id, each_pref, table)

        return {
            "code": 201,
            "message" : f"{table} preferences successfully updated",
            "data" : {
            "pref type": table, 
            "old prefs": old_pref, 
            "deleted prefs": dltpref, 
            "added prefs": addpref, 
            "new prefs": new_pref
            }
        }

    # queue
    def queue(self, telename):
        user_id = self.get_user_id(telename)
        self.qm.queue(user_id)
        return {
            "code": 200,
            "message": f"{telename} successfully queued"
        }
    
    def dequeue(self, telename):
        user_id = self.get_user_id(telename)
        self.qm.dequeue(user_id)
        return {
            "code": 200,
            "message": f"{telename} successfully dequeued"
        }

    # given preferences
    def person_match(self, telename):
        user_id = self.get_user_id(telename)
        age_pref = self.qm.select_pref(user_id, "age_ref", "age_ref_id")
        gender_pref = self.qm.select_pref(user_id, "gender_ref", "gender_ref_id")
        queue_users = self.qm.select_queue_users()

        if not age_pref:
            age_pref = [1,2,3,4,5,6]       # populate with all choices
        if not gender_pref:
            gender_pref = [1,2,3]    # populate with all choices

        matches_A = self.qm.person_match_A(user_id, age_pref, gender_pref)

        primary_age = self.qm.get_user_info(telename, "age_ref_id", "users")[0][0]
        primary_gender = self.qm.get_user_info(telename, "gender_ref_id", "users")[0][0]

        matches_B = self.qm.person_match_B(matches_A, primary_age, primary_gender)

        return {
            "matches": matches_B
        }
    