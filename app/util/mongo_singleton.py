from pymongo import MongoClient
from pymongo.database import Database

#Création de la classe MongoDBConnection
class get_db:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(get_db, cls).__new__(cls)
            cls._instance.client = MongoClient("mongodb://localhost:27017/")
            cls._instance.db = cls._instance.client.digischools
        return cls._instance

    def get_db(self) -> Database:
        return self._instance.db