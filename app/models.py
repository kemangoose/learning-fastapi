from sqlalchemy import Column, Integer, String, Boolean ,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from .database import Base 

class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default = text('TRUE'))
    created_at = Column(TIMESTAMP, server_default=text('now()'))

    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable = False)
    owner = relationship('User')

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, index = True)
    email = Column(String, unique = True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default = text('now()'))
    phone_number = Column(String)


class Vote(Base):
    __tablename__ = 'votes'

    post_id = Column(Integer, ForeignKey('posts.id', ondelete = 'CASCADE'), primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete = 'CASCADE'), primary_key = True)