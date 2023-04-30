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
    
    def get_user_telename(self, user_id):
        query = "SELECT telename FROM users WHERE user_id = %s"
        data = (user_id,)
        record = self.db.execute_select(query, data)
        return record
    
    def get_user_info(self, telename, column, table="users"):
        query = f"SELECT {column} FROM {table} WHERE telename = %s"
        data = (telename,)
        record = self.db.execute_select(query, data)
        return record
    
    def get_info(self, column, table):
        query = f"SELECT {column} FROM {table}"
        record = self.db.execute_select(query)
        return record
    
    def update_user_info(self, telename, value, column):
        query = f"UPDATE users SET {column} = %s WHERE telename = %s"
        data = (value, telename)
        self.db.execute_change(query, data)

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
        queue_users_info = "SELECT users.user_id, users.age_ref_id, users.gender_ref_id FROM users JOIN queue ON users.user_id = queue.user_id"
        age_gender_match_A = f"SELECT qui.user_id FROM ({queue_users_info}) AS qui WHERE age_ref_id = ANY(%s) AND gender_ref_id = ANY(%s) AND NOT user_id = %s"
        data = (age_pref, gender_pref, user_id)
        return self.db.execute_select(age_gender_match_A, data)
    
    def person_match_B(self, matches_A, primary_age, primary_gender):
        age_match_B_query = "SELECT DISTINCT user_ref_id FROM age_ref WHERE user_ref_id = ANY(%s) AND age_ref_id = %s"
        data_age = (matches_A, primary_age)
        age_match_B = self.db.execute_select(age_match_B_query, data_age)
        age_match_B = [row["user_ref_id"] for row in age_match_B]
        age_gender_match_B_query = "SELECT user_ref_id FROM gender_ref WHERE user_ref_id = ANY(%s) AND gender_ref_id = %s"
        data_gender = (age_match_B, primary_gender)
        return self.db.execute_select(age_gender_match_B_query, data_gender)
    
    def person_match_cuisine(self, matches_B, cuisine_pref):
        cuisine_match_C = "SELECT user_ref_id FROM cuisine_ref LEFT JOIN queue ON cuisine_ref.user_ref_id = queue.user_id WHERE user_ref_id = ANY(%s) and cuisine_ref_id = ANY(%s) GROUP BY user_ref_id ORDER BY MIN(timestamp)"
        data = (matches_B, cuisine_pref)
        return self.db.execute_select(cuisine_match_C, data)
    
    def person_match_dietBlacklist(self, matches_C, diet_pref_blacklist):
        diet_match_blacklist = "SELECT DISTINCT user_ref_id FROM diet_ref WHERE user_ref_id = ANY(%s) AND diet_ref_id != ANY(%s)"
        data = (matches_C, diet_pref_blacklist)
        return self.db.execute_select(diet_match_blacklist, data)

    # # to be used for problem: queued user dequeues the moment they are matched with someone, hence need to check if they still in queue and want to be matched. Need to change MainController to use this function.
    # def person_match_timestamp(self, matches_final):
    #     query = "SELECT user_id FROM queue where user_id = ANY(%s) ORDER BY timestamp"
    #     data = (matches_final,)
    #     return self.db.execute_select(query, data)
 

    # delete functions

    def delete_user(self, user_id, column, table):
        query = f"DELETE FROM {table} WHERE {column} = ANY(%s)"
        data = (user_id,)
        return self.db.execute_change(query, data)