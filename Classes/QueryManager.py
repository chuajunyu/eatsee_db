from .Database import Database


class QueryManager:
    def __init__(self):
        self.db = Database()

    def select_user(self, telename):
        """
        Select users with a given telegram username

        Input:
            - telename: Telegram Username to search for

        Return:
            - List of users with that telegram username
        """
        query = "SELECT * FROM users WHERE telename = %s"
        data = (telename,)
        record = self.db.execute_select(query, data)
        return record
    
    def select_all_users(self):
        """
        Select all users in the database

        Return:
            - List of all users in our database
        """
        query = "SELECT * FROM users"
        record = self.db.execute_select(query)
        return record

    def insert_user(self, availability, telename, age, gender):
        """
        Insert a user into the database

        Input:
            - availability: Boolean value describing availability of user
                            (might be deprecated)
            - telename: Telegram username of new user to be inserted
        """
        query = """INSERT INTO users (availability, telename, age, gender)
                VALUES (%s, %s, %s, %s)"""
        data = (availability, telename, age, gender)
        self.db.execute_change(query, data)

    def get_user_id(self, telename):
        query = "SELECT user_id FROM users WHERE telename = %s"
        data = (telename,)
        record = self.db.execute_select(query, data)
        return record

    def select_pref(self, user_id, table, column):
        query = f"SELECT {column} FROM {table} WHERE user_id = %s"
        data = (user_id,)
        record = self.db.execute_select(query, data)
        return record
    
    # turn list(dltpref) into tuple DONE
    def dlt_pref(self, user_id, dltpref, table):
        query = f"DELETE FROM {table} WHERE userref_id = %s AND ageref_id in %s"
        data = (user_id, dltpref)
        self.db.execute_change(query, data)
    
    def add_pref(self, user_id, addpref, table):
        query = f"INSERT INTO {table} VALUES (%s, %s)"
        data = (user_id, addpref)
        self.db.execute_change(query, data)