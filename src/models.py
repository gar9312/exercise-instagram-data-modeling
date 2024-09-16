import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from eralchemy2 import render_er

Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    bio = Column(Text, nullable=True)
    profile_picture = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=func.now())

    posts = relationship('Post', back_populates='author')
    followers = relationship('Follower', back_populates='user')
    followings = relationship('Follower', back_populates='follower')

# Define the Post model
class Post(Base):
    __tablename__ = 'post'
    
    id = Column(Integer, primary_key=True)
    caption = Column(Text, nullable=True)
    image_url = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))

    author = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')

# Define the Comment model
class Comment(Base):
    __tablename__ = 'comment'
    
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))

    author = relationship('User')
    post = relationship('Post', back_populates='comments')

# Define the Follower model
class Follower(Base):
    __tablename__ = 'follower'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    follower_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', foreign_keys=[user_id], back_populates='followers')
    follower = relationship('User', foreign_keys=[follower_id], back_populates='followings')

# Create an engine and create all the tables
if __name__ == '__main__':
    engine = create_engine('sqlite:///instagram_clone.db')  # Replace with your database URL if needed
    Base.metadata.create_all(engine)

    # Generate the ER diagram
    try:
        result = render_er(Base, 'diagram.png')
        print("Success! Check the diagram.png file")
    except Exception as e:
        print("There was a problem generating the diagram")
        raise e
