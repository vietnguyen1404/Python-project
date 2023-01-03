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
    
    def appendOne(entry):
        collection = db["villages"]
        collection.insert_one(entry)

    def deleteOne(id):
        collection = db["villages"]
        collection.delete_one({"_id": ObjectId(id)})

    def updateOne(_id, entry):
        collection = db["villages"]
        newEntry = {"$set": entry}
        collection.update_one({"_id": ObjectId(_id)}, newEntry)