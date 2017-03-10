from sqlalchemy import Column, Integer, String, Boolean, DATETIME, ForeignKey, Table, Text
from resources.database import Base
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash
from models.album import Album


like_photo = Table("like_photo", Base.metadata,
                    Column('user_uid', Integer, ForeignKey('user.uid'), nullable=False),
                    Column('photo_pid', Integer, ForeignKey('photo.pid'), nullable=False)
)

follow_album = Table("follow_album", Base.metadata,
                    Column('user_uid', Integer, ForeignKey('user.uid'), nullable=False),
                    Column('album_aid', Integer, ForeignKey('album.aid'), nullable=False)
)

followers = Table('followers', Base.metadata,
                    Column('follower_id', Integer, ForeignKey('user.uid'), nullable=False),
                    Column('followed_id', Integer, ForeignKey('user.uid'), nullable=False)
)

comment = Table("comment", Base.metadata,
                    Column('comment_cid', Integer, primary_key=True),
                    Column('user_uid', Integer, ForeignKey('user.uid'), nullable=False),
                    Column('photo_pid', Integer, ForeignKey('photo.pid'), nullable=False),
			        Column('reply', Text, nullable=False),
                    Column('created_at', DATETIME)
)

class User(Base):
    __tablename__ = 'user'

    uid = Column(Integer, primary_key=True)
    username = Column(String(10), unique=True, nullable=False)
    email = Column(String(35), unique=True, nullable=False)
    salted_password = Column(String(100), unique=True, nullable=False)
    profile_pic = Column(String(100))
    authorization = Column(Boolean)
    expiry = Column(DATETIME)
    fcm_token = Column(String(45))
    created_at = Column(DATETIME)
    like_photo = relationship('Photo', secondary=like_photo, backref='like')
    follow_album = relationship('Album', secondary=follow_album, backref='follow')
    followed = relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == uid),
                               secondaryjoin=(followers.c.followed_id == uid),
                               backref=backref('followers', lazy='dynamic'),
                               lazy='dynamic')
    comment = relationship('Photo', secondary=comment)

    def set_password(self, password):
        self.salted_password = generate_password_hash(password)

    def __init__(self, username=None, email=None, salted_password=None, profile_pic=None, expriy=None, token=None, authorized=None, created_at=None):
        self.username = username
        self.email = email
        self.set_password(salted_password)
        self.profile_pic = profile_pic
        self.expiry = expriy
        self.token = token
        self.authorized = authorized
        self.created_at = created_at

    def __repr__(self):
        return "<User('%s', '%s')>" % (self.username, self.email)