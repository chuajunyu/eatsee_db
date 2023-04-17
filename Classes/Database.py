import psycopg2

from .ConfigManager import ConfigManager


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass = Singleton):
    def __init__(self):
        config = ConfigManager()
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
