from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app import db

Base = declarative_base()

# Define the association table for the many-to-many relationship between Post and Tag
post_tag_association = Table('post_tag_association', Base.metadata,
                             Column('post_id', Integer, ForeignKey('posts.id')),
                             Column('tag_id', Integer, ForeignKey('tags.id'))
                            )

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)

    # Establish a many-to-many relationship with Post using the association table
    posts = relationship("Post", secondary=post_tag_association, back_populates="tags")

class PostTag(db.Model):
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, ForeignKey('tags.id'), primary_key=True)

    # Establish a many-to-one relationship with Post
    post = relationship("Post", back_populates="post_tags")

    # Establish a many-to-one relationship with Tag
    tag = relationship("Tag", back_populates="post_tags")

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, default='default_profile_image.jpg')

    # Establish a one-to-many relationship between User and Post
    posts = relationship("Post", back_populates="user")

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)

    # Establish a many-to-one relationship with User
    user = relationship("User", back_populates="posts")

    # Establish a many-to-many relationship with Tag using the association table
    tags = relationship("Tag", secondary=post_tag_association, back_populates="posts")

class PostTag(db.Model):
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, ForeignKey('tags.id'), primary_key=True)

    # Establish a many-to-one relationship with Post
    post = relationship("Post", back_populates="post_tags")

    # Establish a many-to-one relationship with Tag
    tag = relationship("Tag", back_populates="post_tags")
