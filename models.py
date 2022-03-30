"""Models for Blogly."""

from inspect import classify_class_attrs
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.init = app
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
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
           