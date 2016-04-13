from pymongo import MongoClient


class MongoDB(object):
    def __init__(self, uri, database, collection):
        self.uri = uri
        self.database_name = database
        self.collection_name = collection

    def write(self, results):
        client = MongoClient(self.uri)
        db = client[self.database_name]
        collection = db[self.collection_name]
        collection.insert_one(results)
