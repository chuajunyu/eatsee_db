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
            return {"message": "User Creation Failed: User already Exists"}
        self.qm.insert_user(availability, telename, age, gender)
        return {"message": "User Successfully Created"}
    

    def get_user_id(self, telename):
        return self.qm.get_user_id(telename)
    

    def change_pref(self, telename, preferences, table, column):
        
        # get user_id
        user_id_record = self.get_user_id(telename)
        user_id = user_id_record[0][0]

        # select old pref type list[tuple]
        old_age_pref1 = self.qm.select_pref(user_id, table, column)

        # get new pref type:list[int]
        new_age_pref = preferences

        old_age_pref2 = []
        dltpref = []
        addpref = []

        for row in old_age_pref1:
            old_age_pref2.append(row[0])
        
        # delete old prefs
        for each_pref in old_age_pref2:
            if each_pref not in new_age_pref:
                dltpref.append(each_pref)
        
        # add new pref
        for each_pref in new_age_pref:
            if each_pref not in old_age_pref2:
                addpref.append(each_pref)

        self.qm.dlt_pref(user_id, tuple(dltpref), table)

        for each_pref in addpref:
            self.qm.add_pref(user_id, each_pref, table)

    def change_age_pref(self, telename, preferences, table, column):
        return self.change_pref(telename, preferences, table, column)
    
    def change_cuisine_pref(self, telename, preferences, table, column):
        return self.change_pref(telename, preferences, table, column)
    
    def change_diet_pref(self, telename, preferences, table, column):
        return self.change_pref(telename, preferences, table, column)