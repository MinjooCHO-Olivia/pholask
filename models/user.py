from sqlalchemy import Column, Integer, String, Boolean, DATETIME, ForeignKey, Table, Text
from resources.database import Base
from sqlalchemy.orm import relationship, backref

follow_user = Table("follow_user", Base.metadata,
                    Column('follower', Integer, ForeignKey('user.id'), nullable=False),
                    Column('following', Integer, ForeignKey('user.id'), nullable=False)
)

follow_album = Table("follow_album", Base.metadata,
                     Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
                     Column('album_id', Integer, ForeignKey('album.id'), nullable=False)
)

like_photo = Table("like_photo", Base.metadata,
                   Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
                   Column('photo_id', Integer, ForeignKey('photo.id'), nullable=False)
)

comment = Table("comment", Base.metadata,
                Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
                Column('photo_id', Integer, ForeignKey('photo.id'), nullable=False),
                Column('reply', String(300), unique=True, nullable=False),
                Column('created_at', DATETIME)
)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(10), unique=True, nullable=False)
    email = Column(String(20), unique=True, nullable=False)
    salted_password = Column(String(45), unique=True, nullable=False)
    profile_pic = Column(String(100))
    expiry = Column(DATETIME)
    token = Column(String(45))
    authorized = Column(Boolean)
    created_at = Column(DATETIME)
    make_album = relationship("Album", backref="user")
    comment = relationship("Comment", backref="user")
    follow_user = relationship('User', secondary=follow_user, backref='user')
    follow_album = relationship('Album', secondary=follow_album, backref='user')
    like_photo = relationship('Photo', secondary=like_photo, backref='photo')

    def __init__(self, username=None, email=None, salted_password=None, profile_pic=None, expriy=None, token=None, authorized=None, created_at=None):
        self.username = username
        self.email = email
        self.salted_password = salted_password
        self.profile_pic = profile_pic
        self.expiry = expriy
        self.token = token
        self.authorized = authorized
        self.created_at = created_at