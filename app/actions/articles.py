from app.mongodb.index import connect
db = connect()

class Article:
    def findAll():
        collection = db["articles"]
        docs = collection.find({})
        for x in docs:
            print(x)
