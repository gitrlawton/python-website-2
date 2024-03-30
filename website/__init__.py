## This file makes the folder 'website' a python package. ##

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "ourkey"
    
    return app