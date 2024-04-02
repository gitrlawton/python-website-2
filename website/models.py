## This file contains our database models. ##

# . means "From this package," import db.
from . import db
# UserMixin is a convenience class provided to simplify the implementation 
# of user models in Flask applications that use Flask-Login for user 
# authentication and session management. It provides default 
# implementations for common user-related methods and properties, making it 
# easier to work with user objects in Flask applications. For example, 
# properties like is_authenticated and methods like get_id().
from flask_login import UserMixin
# func will sqlalchemy to store the current time for us in the database.
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    # SQLAlchemy will automatically add the current time using func.now()
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # Associating Notes with Users via a foreign key.  
    # The foreign key is stored as a column in the child table (ie. the Note 
    # table.) The value to use as the foreign key is passed as the parameter
    # to db.ForeignKey.  In this case, we're using the 'id' property of the
    # User table ('user' is spelled lowercase because we only use uppercase
    # to define the class, but in practice, we reference it with lowercase.)
    # The reason we're using user.id as the foreign key is because it is the
    # primary key of that table.  Note: For this case, we're establishing a 
    # 'one-to-many' relationship (one user can have many notes.)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # Completes the association of the Notes with it's user.  Every time a
    # note is created, it will append it to its user's 'notes' field (a list).
    # Unlike with the foreign key, the table here is referenced with a
    # capitalized first letter.
    notes = db.relationship('Note')
    