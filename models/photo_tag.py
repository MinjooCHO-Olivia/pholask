from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from resources.database import Base

class Photo_tag(Base):
    __tablename__ = 'photo_tag'

    p_tag_name = Column(String(20), primary_key=True)
    photo_id = Column(Integer, ForeignKey('photo.id'), nullable=False)

    def __init__(self, p_tag_name=None):
        self.p_tag_name = p_tag_name