from bson.objectid import ObjectId
from app.mongodb.index import connect
db = connect()


class User:
    def findAll(search):
        collection = db["users"]
        docs = collection.find({'$or' : [
        { 'name': { '$regex': search, '$options': 'i' } },
        { 'card': { '$regex': search, '$options': 'i' } },
        { 'phone': { '$regex': search, '$options': 'i' } }
    ]})
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

    def changStatus(_id):
        collection = db["users"]
        doc = collection.find_one({"_id": ObjectId(_id)})
        if doc["enable"] == 1:
            doc["enable"] = 0
        else:
            doc["enable"] = 1
        collection.update_one({"_id": ObjectId(_id)}, {"$set": doc})
