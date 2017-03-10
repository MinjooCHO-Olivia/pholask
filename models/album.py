from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from resources.database import Base


class Album(Base):
    __tablename__ = 'album'

    aid = Column(Integer, primary_key=True)
    title = Column(String(45), unique=True, nullable=False)
    created_at = Column(DATETIME)
    user_uid = Column(Integer, ForeignKey('user.uid'))
    user = relationship('User', backref=backref('albums', order_by=aid))

    def __init__(self, title=None, created_at=None, user_uid=None):
        self.title = title
        self.created_at = created_at
        self.user_uid = user_uid