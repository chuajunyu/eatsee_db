from .Database import Database


class QueryManager:
    def __init__(self):
        self.db = Database()

    def select_user(self, telename):
        query = "SELECT * FROM users WHERE telename = %s"
        data = (telename,)
        record = self.db.execute_select(query, data)
        return record
    
    def select_all_users(self):
        query = "SELECT * FROM users"
        record = self.db.execute_select(query)
        return record

    def insert_user(self, availability, telename):
        query = """INSERT INTO users (availability, telename)
                VALUES (%s, %s)"""
        data = (availability, telename)
        self.db.execute_change(query, data)