## This file contains all the views (url endpoints). ##
## This file is a blueprint of our application. ##

from flask import Blueprint

from flask import render_template

# Setting up a blueprint for our flask application.
views = Blueprint('views', __name__)

# This function will run whenever a user visits the route.
@views.route('/')
def home():
    return render_template("home.html")

# Now we have this blueprint defined, we need to register the blueprint in
# __init__.py.  (See __init__.py)