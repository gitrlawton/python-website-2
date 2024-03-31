## This file makes the folder 'website' a python package. ##

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "ourkey"
    # Import the blueprints.
    from .views import views
    from .auth import auth
    # Register the blueprints.
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    return app