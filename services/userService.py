from sqlalchemy import func
from models.user import User
from resources.database import db_session

class UserService :

    def findByUid(self, uid):
        return User.query.filter(User.uid == uid).first()

    def findByUsername(self, username):
        return User.query.filter(User.username == username).first()

    def findByEmail(self, email):
        return User.query.filter(User.email == email).first()

    def giveAuth(self, u):
        u.authorization = True

    def isValidUid(self, uid):
        uid = int(uid)
        max_uid_string = str(db_session.query(func.max(User.uid)).first())
        max_uid = int(max_uid_string[1:-2])

        if uid < 0 or uid > max_uid:
            return False

        return True

    def addUser(self, u):
        db_session.add(u)
        db_session.commit()

    def deleteUser(self, u):
        db_session.delete(u)
        db_session.commit()

    def usernameCount(self, username):
        return User.query.filter(User.username == username).count()

    def emailCount(self, email):
        return User.query.filter(User.email == email).count()