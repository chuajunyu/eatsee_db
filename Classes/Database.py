import psycopg2

from .ConfigManager import ConfigManager


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass = Singleton):
    """
    Wrapper of psycopg2. Makes connections to the postgreSQL database.
    Executes queries and commits changes to the database.

    Edit the configuration file with credentials to access database.
    """
    def __init__(self):
        config = ConfigManager()
        self.conn = psycopg2.connect(
                host=config.get("database_host"),
                database=config.get("database_name"),
                user=config.get("database_user"),
                password=config.get("password")
                )
        
    def execute_select(self, query, *data):
        """
        Executes a Select SQL query statement
        
        Input:
            - query: SQL Query Statement, with placeholders for data
            - data: Sequence containing data for the query (Optional)

        Return:
            - records: List of results from the database
        """
        cursor = self.conn.cursor()
        cursor.execute(query, *data)
        records = cursor.fetchall()
        cursor.close()
        return records
    
    def execute_change(self, query, *data):
        """
        Executes a SQL query statement which causes a change.
        Such as Insert, Update, Delete.
        
        Input:
            - query: SQL Query Statement, with placeholders for data
            - data: Sequence containing data for the query (Optional)
        """
        cursor = self.conn.cursor()
        cursor.execute(query, *data)
        self.conn.commit()
        cursor.close()
