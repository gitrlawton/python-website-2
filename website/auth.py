from flask import Blueprint
from flask import render_template, request
from . import db
from flask import redirect, url_for
from flask import flash

from .models import User
# Allows us to secure our passwords and avoid saving them as plain text.
from werkzeug.security import generate_password_hash, check_password_hash
# Functions to log in our user. login_required requires user to be logged in to
# be able to visit certain pages.
from flask_login import login_user, login_required, logout_user, current_user

# Setting up a blueprint for our flask application.
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # If we're signing in (and not just getting the page.) The POST request
    # comes from clicking the login button.  The GET request comes from simply
    # visiting the login page.
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Check if email is a valid email that exists in the database.
        # When you are looking for specific entry in your database and you want
        # to search by a specific column.  Each user should have their own
        # unique email, so there should only be one result to return, hence
        # the use of .first()
        user = User.query.filter_by(email=email).first()
        # If a user match was returned...
        if user:
            # If the password sent via the POST request from the login page
            # matches the user's password in the database...
            if check_password_hash(user.password, password):
                flash('Logged in successfully.', category="success")
                # Log the user in.  Remember that they are logged in.
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            # Otherwise, it doesn't match.
            else:
                flash('Incorrect password.', category='error')
        # Otherwise, no user matching the entered email address was found.
        else:
            flash('Email does not exist.', category='error')
    # Pass the current user to the login template so it has access to it.
    return render_template("login.html", user=current_user)

@auth.route('/logout')
# Decorator to make sure the user cannot access this page unless they are logged in.
@login_required 
def logout():
    # Log the user out.
    logout_user()
    # Direct them to the login page.
    return redirect(url_for('auth.login'))

# When you go to the url, that is a GET reuqest.  When you click the submit
# button on the page, that sends a POST request to the server.
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # Check if request sent to the server via the route was a POST request.
    # If so...
    if request.method == 'POST':
        # Extract the fields from the request object.
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        # Check to make sure email address isn't already associated with an
        # account in the database.
        user = User.query.filter_by(email=email).first()
        # If user already exists with that email...
        if user:
            flash('Email already exists.', category='error')
        # Otherwise...
        else:    
            # Check if data in POST request (ie. the form input data)
            # is valid.
            if len(email) < 4:
                flash('Email must be longer than 3 characters.', category='error')
            elif len(first_name) < 2:
                flash('First name must be greater than 1 character.', category='error')
            elif password1 != password2:
                flash("Paswords don't match.", category='error')
            elif len(password1) < 7:
                flash('Password must be longer than 6 characters.', category='error')
            else:
                # All inputs were valid, thus create a new user.  Note: We don't want
                # to store the user's password as plain text -- like we are with their
                # email and first name.  So we call the generate_password_hash()
                # function to generate an encrypted version of their password, passing
                # it the password plus the method to hash with, and then save that in
                # the user's password field.
                new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
                # Add and commit the changes to the database.
                db.session.add(new_user)
                db.session.commit()
                # Alert user their account was created successfully.
                flash('Account created.', category='success')
                # Log the user in.
                login_user(new_user, remember=True)
                # Direct user to the homepage.
                return redirect(url_for('views.home'))
    # Pass the current user to the sign up template so it has access to it.
    return render_template("sign_up.html", user=current_user)