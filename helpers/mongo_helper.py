from pymongo import MongoClient, ASCENDING

class MongoHelper:
    database_name = 'movie_meta'
    def __init__(self):
        self.client = MongoClient("localhost", 27018)
        self.db = self.client[self.database_name]
        self.collection = self.db['movies']

    def insert_doc(self, data):
        return self.collection.insert_one(data).inserted_id

    def update_doc(self, data):
        self.collection.update_one({"_id": data.get("_id")}, {"$set": data})

    def get_all_data(self):
        return self.collection.find({}).sort("title", ASCENDING)

    def find_by_path(self, path):
        return self.collection.find_one({"path": path})