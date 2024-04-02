## This file makes the folder 'website' a python package. ##

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from os import path

# Initialize our database object.
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "ourkey"
    # Tell flask what database we're using and where it's located.
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # Initialize the database with the app.
    db.init_app(app)
    # Import the blueprints.
    from .views import views
    from .auth import auth
    # Register the blueprints.
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    # BTW, '.' is a relative import.  We're importing the models here,
    # not because we're going to use them in this file, but because in
    # order to import them, they need to be created first (and we want 
    # them to be created first before we create our database.)
    from .models import User, Note
    # Call function to create database.
    create_database(app)
    
    return app

# Creates the database if it doesn't already exist.
def create_database(app):
    # Check if the path: website/database.db doesn't already exist.
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("Database created successfully.")