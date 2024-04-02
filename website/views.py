## This file contains all the views (url endpoints).  It is a blueprint of our 
# application. ##

from flask import Blueprint
from flask import render_template, request
from . import db
from flask import flash
# Functions to log in our user.
from flask_login import login_required, current_user
from flask import jsonify

from .models import Note
# We need to use json for our delete_note() view.
import json

# Setting up a blueprint for our flask application.
views = Blueprint('views', __name__)

# This function will run whenever a user visits the route.
@views.route('/', methods=['GET', 'POST'])
# Decorator to make sure the user cannot access this page unless they are logged in.
@login_required 
def home():
    if request.method == 'POST':
        # Adding a new note to the database.
        note = request.form.get('note')
        
        if len(note) < 1: 
            flash('Note is too short.', category='error')
        else:
            # Create a new Note object using data=note to assign the new note's
            # data to the textarea submitted via the home page's POST request.
            # Remember, the textarea's name is set to note, and an element's
            # name is how we access the element.  So to save the textarea's
            # input text to the note's data, we reference it by its name.
            new_note = Note(data=note, user_id=current_user.id)
            # Add and commit changes to the database.
            db.session.add(new_note)
            db.session.commit()
            # Alert user that the note was created.
            flash('Note added.', category='success')
    # Pass the current user to the home template so it has access to it.
    return render_template("home.html", user=current_user)

# Now we have this blueprint defined, we need to register the blueprint in
# __init__.py.  (See __init__.py)

# Request will come in, not as a form, but in the data parameter of the request
# object, which means we need to load it as json.
@views.route('/delete-note', methods=['POST'])
def delete_note():
    # The request data is a string.  json.loads() will take the string and loads
    # it as a JSON object (python dictionary), so we can access it.
    note = json.loads(request.data)
    noteId = note['noteId']
    # Search database for a note with that id.
    note = Note.query.get(noteId)
    # If it exists...
    if note:
        # If the note's creator is the current user...
        if note.user_id == current_user.id:
            # Delete the note.
            db.session.delete(note)
            # Update the database.
            db.session.commit()
    # We don't have anything to return, but all views are required to return
    # something. So, return an empty JSON object.
    return jsonify({})