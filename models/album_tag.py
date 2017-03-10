from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from resources.database import Base

class Album_tag(Base):
    __tablename__ = 'album_tag'

    a_tag_name = Column(String(20), primary_key=True)
    album_aid = Column(Integer, ForeignKey('album.aid'))
    album = relationship("Album", backref=backref('album_tags'))

    def __init__(self, a_tag_name=None):
        self.a_tag_name = a_tag_name