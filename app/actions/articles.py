from bson.objectid import ObjectId
from app.mongodb.index import connect
db = connect()


class Article:
    def findAll():
        collection = db["articles"]
        docs = collection.find({})
        return docs

    def appendOne(entry):
        collection = db["articles"]
        collection.insert_one(entry)

    def deleteOne(id):
        collection = db["articles"]
        collection.delete_one({"_id": ObjectId(id)})

    def findOne(id):
        collection = db["articles"]
        doc = collection.find_one({"_id": ObjectId(id)})
        return doc

    def updateOne(_id, entry):
        collection = db["articles"]
        newEntry = {"$set": entry}
        collection.update_one({"_id": ObjectId(_id)}, newEntry)