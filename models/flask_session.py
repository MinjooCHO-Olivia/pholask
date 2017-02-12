from sqlalchemy import Column, String, BLOB
from resources.database import Base, db_session

class FlaskSession(Base):
    __tablename__ = 'flask_session'

    sid = Column(String(20), primary_key=True)
    value = Column(BLOB)

    def change(cls, sid, value):
        rec = db_session.query(cls).filter(cls.sid == sid).first()
        if not rec:
            rec = cls()
            rec.sid = sid
        rec.value = value

        return rec