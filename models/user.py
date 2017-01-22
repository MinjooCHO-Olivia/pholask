from sqlalchemy import Column, Integer, String, Boolean, DATETIME, ForeignKey, Table, Text
from resources.database import Base
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash


like_photo = Table("like_photo", Base.metadata,
                    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
                    Column('photo_id', Integer, ForeignKey('photo.id'), nullable=False)
)

follow_album = Table("follow_album", Base.metadata,
                    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
                    Column('album_id', Integer, ForeignKey('album.id'), nullable=False)
)

followers = Table('followers', Base.metadata,
                    Column('follower_id', Integer, ForeignKey('user.id')),
                    Column('followed_id', Integer, ForeignKey('user.id'))
)

comment = Table("comment", Base.metadata,
                    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
                    Column('photo_id', Integer, ForeignKey('photo.id'), nullable=False),
			        Column('reply', String(1000), nullable=False),
                    Column('created_at', DATETIME)
)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(10), unique=True, nullable=False)
    email = Column(String(35), unique=True, nullable=False)
    salted_password = Column(String(100), unique=True, nullable=False)
    profile_pic = Column(String(100))
    expiry = Column(DATETIME)
    token = Column(String(45))
    authorization = Column(Boolean)
    created_at = Column(DATETIME)
    album = relationship("Album", backref=backref('user', order_by=id))
    like_photo = relationship('Photo', secondary=like_photo, backref='user')
    follow_album = relationship('Album', secondary=follow_album)
    followed = relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
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

        def follow(self, user):
            if not self.is_following(user):
                self.followed.append(user)
                return self

        def unfollow(self, user):
            if self.is_following(user):
                self.followed.remove(user)
                return self

        def is_following(self, user):
            return self.followed.filter(followers.c.followed_id == user.id).count() > 0