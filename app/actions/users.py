from bson.objectid import ObjectId
from app.mongodb.index import connect
db = connect()

class User:
    def findAll():
        collection = db["users"]
        docs = collection.find({})
        return docs
    def appendOne(entry):
        collection = db["users"]
        collection.insert_one(entry)
    def deleteOne(id):
        collection = db["users"]
        collection.delete_one({"_id": ObjectId(id)})