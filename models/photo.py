from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from resources.database import Base

class Photo(Base):
    __tablename__ = 'photo'

    id = Column(Integer, primary_key=True)
    image = Column(String(100), unique=True, nullable=False)
    content = Column(String(1500))
    created_at = Column(DATETIME)
    album_id = Column(Integer, ForeignKey('album.id'), nullable=False)
    photo_tag = relationship("Photo_tag", backref=backref('photo'))

    def __init__(self, image=None, content=None, created_at=None):
        self.image = image
        self.content = content
        self.created_at = created_at