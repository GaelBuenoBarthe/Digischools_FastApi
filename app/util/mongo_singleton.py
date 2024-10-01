from pymongo import MongoClient

class MongoSingleton:
    _client = None
    _db = None

    def __init__(self):
        if MongoSingleton._client is None:
            MongoSingleton._client = MongoClient("mongodb://localhost:27017/")
            MongoSingleton._db = MongoSingleton._client["digischools"]

    @staticmethod
    def get_db():
        if MongoSingleton._db is None:
            MongoSingleton()
        return MongoSingleton._db

    @staticmethod
    def close():
        if MongoSingleton._client:
            MongoSingleton._client.close()
            MongoSingleton._client = None
            MongoSingleton._db = None