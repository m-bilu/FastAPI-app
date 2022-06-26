## Models file holds all PostgreSQL-type table information, while Database file holds code to connect
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, Boolean, String, text
from .database import Base
from sqlalchemy.orm import relationship


############################ IMPORTANT
####### THIS FILE HOLDS ALL SQLALCHEMY MODELS. THESE ARE RESPONSIBLE FOR 
#######     STRUCTURING THE ACTUAL TABLES, COLUMNS AND ENTRIES ON POSTGRESQL DATABASE

# class type is Post, is a child of the general table type Base
# Table of Posts
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key = True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))
    userid = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False) # onupdate is default noact
    user = relationship("User")

# Table of Users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))


# Table of Votes, Composite Key instead of Primary Key
class Vote(Base):
    __tablename__ = "votes"

    postid = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"),primary_key=True)
    userid = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))

# Table of Comments
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, nullable=False)
    postid = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    userid = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))
