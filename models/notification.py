from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from resources.database import Base

class Notification(Base):
    __tablename__ = 'notification'

    nid = Column(Integer, primary_key=True)
    user_uid = Column(Integer, ForeignKey('user.uid'))
    type = Column(String(10), nullable=False)
    target = Column(String(20))
    message = Column(Text, nullable=False)
    read = Column(Boolean, nullable=False)
    created_at = Column(DATETIME)
    user = relationship("User", backref=backref('notifications', order_by=nid))

    def __init__(self, type=None, message=None, read=None, created_at=None):
        self.type = type
        self.massage = message
        self.read = read
        self.created_at = created_at