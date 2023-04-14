import psycopg2

from .ConfigManager import ConfigManager


class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


class Database(Singleton):
    def __init__(self):
        config = ConfigManager._instance
        self.conn = psycopg2.connect(
                host=config.get("database_host"),
                database=config.get("database_name"),
                user=config.get("database_user"),
                password=config.get("password")
                )
        
    def execute_select(self, *query):
        cursor = self.conn.cursor()
        cursor.execute(*query)
        records = cursor.fetchall()
        cursor.close()
        return records
    
    def execute_change(self, *query):
        cursor = self.conn.cursor()
        cursor.execute(*query)
        self.conn.commit()
        cursor.close()


if __name__ == "__main__":
    ConfigManager(path=r"dev.config")
    db = Database()
    print(db.execute("SELECT * FROM users"))

