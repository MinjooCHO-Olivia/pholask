from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from resources.database import Base

class Album_tag(Base):
    __tablename__ = 'album_tag'

    a_tag_name = Column(String(20), primary_key=True)
    album_id = Column(Integer, ForeignKey('album.id'), nullable=False)

    def __init__(self, a_tag_name=None):
        self.a_tag_name = a_tag_name