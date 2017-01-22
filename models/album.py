from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from resources.database import Base


class Album(Base):
    __tablename__ = 'album'

    id = Column(Integer, primary_key=True)
    title = Column(String(45), unique=True, nullable=False)
    created_at = Column(DATETIME)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    photo = relationship("Photo", backref=backref('album', order_by=id))
    album_tag = relationship("Album_tag", backref=backref('album'))

    def __init__(self, title=None, created_at=None, user_uid=None):
        self.title = title
        self.created_at = created_at
        self.user_uid = user_uid