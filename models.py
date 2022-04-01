"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""
    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    first_name = db.Column(db.String,
                            nullable=False)

    last_name = db.Column(db.String,
                          nullable=False)
    
    image_url = db.Column(db.String,
                          nullable = False, 
                          default = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460__480.png" )
    
    # Sets up a posts attribute on each instance of user
    #SQLA will populate it with data from posts table automatically
    # direct navigation: user -> post & back
    posts = db.relationship('Post', backref="user")
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Post(db.Model):
    """Post"""
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    title = db.Column(db.Text,
                      nullable=False,
                      unique=True)
    
    content = db.Column(db.Text,
                        nullable=False)

    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default = datetime.datetime.now)
    
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id'), 
                        nullable=False)

    @property
    def friendly_date(self):
        """Return formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


class Tag(db.Model):
    """Tags for posts"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Text, nullable=False)
    
    # direct navigation: tag -> posttag & back
    posts = db.relationship('Post', secondary='posts_tags', backref='tags')


class PostTag(db.Model):
    """Posts and their respective tags"""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
   
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

