## This file makes the folder 'website' a python package. ##

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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
    
    return app