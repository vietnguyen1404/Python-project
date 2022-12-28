from app.mongodb.index import connect
db = connect()

class Vaccine:
    def findAll():
        collection = db["vaccines"]
        docs = collection.find({})
        return docs