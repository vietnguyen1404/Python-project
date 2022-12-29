from bson.objectid import ObjectId
from app.mongodb.index import connect
from app.actions.users import User
db = connect()

class Auth:
    def login(phone, password):
        doc = User.findLogin(phone, password)
        return doc