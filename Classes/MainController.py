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
        return user_id[0][0]
    
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
            "prefence type": table, 
            "old prefs": old_pref, 
            "deleted prefs": dltpref, 
            "added prefs": addpref, 
            "new prefs": new_pref
            }
        }