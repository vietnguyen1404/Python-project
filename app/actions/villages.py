from bson.objectid import ObjectId
from app.mongodb.index import connect
db = connect()

class Village:
    def findAll():
        collection = db["villages"]
        docs = collection.find({})
        return docs
    def findOne(id):
        collection = db["villages"]
        doc = collection.find_one({"_id": ObjectId(id)})
        return doc