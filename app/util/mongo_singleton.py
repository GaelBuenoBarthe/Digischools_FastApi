from pymongo import MongoClient
from pymongo.database import Database

class MongoSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoSingleton, cls).__new__(cls)
            cls._instance.client = MongoClient("mongodb://localhost:27017/")
            cls._instance.db = cls._instance.client.digischools
        return cls._instance

    @staticmethod
    def get_db() -> Database:
        if MongoSingleton._instance is None:
            MongoSingleton()
        return MongoSingleton._instance.db

    def close(self):
        self._instance.client.close()

# Function to get the database instance
def get_db() -> Database:
    return MongoSingleton().get_db()