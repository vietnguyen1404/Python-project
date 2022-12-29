from bson.objectid import ObjectId
from app.mongodb.index import connect
db = connect()


class Vaccine:
    def findAll():
        collection = db["vaccines"]
        docs = collection.find({})
        return docs

    def appendOne(entry):
        collection = db["vaccines"]
        collection.insert_one(entry)

    def deleteOne(id):
        collection = db["vaccines"]
        collection.delete_one({"_id": ObjectId(id)})

    def findOne(id):
        collection = db["vaccines"]
        doc = collection.find_one({"_id": ObjectId(id)})
        return doc
    
    def updateOne(_id, entry):
        collection = db["vaccines"]
        newEntry = {"$set": entry}
        collection.update_one({"_id": ObjectId(_id)}, newEntry)
