## This file contains our database models. ##

# . means "From this package," import db.
from . import db
# A convenience class provided to simplify the implementation of 
# user models in Flask applications that use Flask-Login for user 
# authentication and session management. It provides default 
# implementations for common user-related methods and properties, 
# making it easier to work with user objects in Flask applications.
# For example, properties like is_authenticated and methods like
# get_id().
from flask_login import UserMixin
# func will help us store the time.
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    # SQLAlchemy will automatically add the current time using func.now()
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    