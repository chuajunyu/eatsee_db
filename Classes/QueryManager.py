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
        query = """INSERT INTO users (availability, telename, age_ref_id, gender_ref_id)
                VALUES (%s, %s, %s, %s)"""
        data = (availability, telename, age, gender)
        self.db.execute_change(query, data)

    def get_user_id(self, telename):
        query = "SELECT user_id FROM users WHERE telename = %s"
        data = (telename,)
        record = self.db.execute_select(query, data)
        return record
    
    def get_user_info(self, telename, column, table):
        query = f"SELECT {column} FROM {table} WHERE telename = %s"
        data = (telename,)
        record = self.db.execute_select(query, data)
        return record
    
    def get_info(self, column, table):
        query = f"SELECT {column} FROM {table}"
        record = self.db.execute_select(query)
        return record

    # preference functions

    def select_pref(self, user_id, column, table):
        query = f"SELECT {column} FROM {table} WHERE user_ref_id = %s"
        data = (user_id,)
        record = self.db.execute_select(query, data)
        return record
    
    def dlt_pref(self, user_id, dltpref, column, table):
        query = f"DELETE FROM {table} WHERE user_ref_id = %s AND {column} in %s"
        data = (user_id, dltpref)
        self.db.execute_change(query, data)
    
    def add_pref(self, user_id, addpref, table):
        query = f"INSERT INTO {table} VALUES (%s, %s)"
        data = (user_id, addpref)
        self.db.execute_change(query, data)

    # queue functions

    def queue(self, user_id):
        query = "INSERT INTO queue VALUES (%s, current_timestamp)"
        data = (user_id,)
        self.db.execute_change(query, data)
    
    def dequeue(self, user_id):
        query = "DELETE FROM queue WHERE user_id = %s"
        data = (user_id,)
        self.db.execute_change(query, data)

    
    # matching functions

    def select_queue_users(self):
        query = "SELECT users.user_id, users.age_ref_id, users.gender_ref_id FROM users JOIN queue ON users.user_id = queue.user_id ORDER BY timestamp"
        return self.db.execute_select(query)
    
    def person_match_A(self, user_id, age_pref, gender_pref):
        queue_users_info = "SELECT users.user_id, users.age_ref_id, users.gender_ref_id FROM users JOIN queue ON users.user_id = queue.user_id ORDER BY timestamp"
        query = f"SELECT qui.user_id FROM ({queue_users_info}) AS qui WHERE age_ref_id = ANY(%s) AND gender_ref_id = ANY(%s) AND NOT user_id = %s"
        data = (age_pref, gender_pref, user_id)
        return self.db.execute_select(query, data)
    
    def person_match_B(self, matches_A, primary_age, primary_gender):
        age_match_B = self.db.execute_select("SELECT user_ref_id FROM age_ref WHERE age_ref_id = %s", (primary_age,))
        age_match_B = [row["user_ref_id"] for row in age_match_B]
        gender_match_B = self.db.execute_select("SELECT user_ref_id FROM gender_ref WHERE gender_ref_id = %s", (primary_gender,))
        gender_match_B = [row["user_ref_id"] for row in gender_match_B]
        query = f"SELECT user_id from users WHERE user_id = ANY(%s) AND user_id = ANY(%s) AND user_id = ANY(%s)"
        data = (matches_A, age_match_B, gender_match_B)
        return self.db.execute_select(query, data)