from sqlalchemy import func
from models.album import Album
from resources.database import db_session

class AlbumService :

    def findByAid(self, aid):
        a = Album.query.filter(Album.aid == aid).first()
        return a

    def findByUid(self, uid):
        a = Album.query.filter(Album.user_uid == uid).first()
        return a

    def isValidAid(self, aid):
        aid = int(aid)
        max_aid_string = str(db_session.query(func.max(Album.aid)).first())
        max_aid = int(max_aid_string[1:-2])

        if aid < 0 or aid > max_aid:
            return False

        return True

    def addAlbum(self, a):
        db_session.add(a)
        db_session.commit()