from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from resources.database import Base

class Photo(Base):
    __tablename__ = 'photo'

    pid = Column(Integer, primary_key=True)
    image = Column(String(100), unique=True, nullable=False)
    content = Column(Text)
    created_at = Column(DATETIME)
    album_aid = Column(Integer, ForeignKey('album.aid'))
    album = relationship('Album', backref=backref('photos', order_by=pid))

    def __init__(self, image=None, content=None, created_at=None):
        self.image = image
        self.content = content
        self.created_at = created_at