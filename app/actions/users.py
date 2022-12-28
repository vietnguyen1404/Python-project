from bson.objectid import ObjectId
from app.mongodb.index import connect
db = connect()


class User:
    def findAll():
        collection = db["users"]
        docs = collection.find({})
        return docs

    def findOne(id):
        collection = db["users"]
        doc = collection.find_one({"_id": ObjectId(id)})
        return doc

    def appendOne(entry):
        collection = db["users"]
        collection.insert_one(entry)

    def updateOne(_id, entry):
        collection = db["users"]
        newEntry = {"$set": entry}
        collection.update_one({"_id": ObjectId(_id)}, newEntry)

    def deleteOne(id):
        collection = db["users"]
        collection.delete_one({"_id": ObjectId(id)})
    
    def findLogin(phone, password):
        collection = db["users"]
        doc = collection.find_one({"phone": phone, "password": password})
        return doc
