from pymongo import MongoClient


class ReportsRepository:
    def __init__(self, mongo_db_connection):
        client = MongoClient(mongo_db_connection)
        db = client.get_default_database()
        self.collection = db.reports

    def insert_document(self, document):
        self.collection.insert_one(document)

    def get_by_id(self, key):
        doc = self.collection.find_one({'_id': key})

        if doc is not None:
            return doc['report']

        return None
