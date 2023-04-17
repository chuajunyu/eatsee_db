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

    def insert_user(self, availability, telename):
        """
        Insert a user into the database

        Input:
            - availability: Boolean value describing availability of user
                            (might be deprecated)
            - telename: Telegram username of new user to be inserted
        """
        query = """INSERT INTO users (availability, telename)
                VALUES (%s, %s)"""
        data = (availability, telename)
        self.db.execute_change(query, data)