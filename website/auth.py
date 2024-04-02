from flask import Blueprint
from flask import render_template, request
from . import db
from flask import redirect, url_for
from flask import flash

from .models import User
# Allows us to secure our passwords and avoid saving them as plain text.
from werkzeug.security import generate_password_hash, check_password_hash

# Setting up a blueprint for our flask application.
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html", text="Testing")

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

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
        # Check if data sent with POST request (ie. the form input data)
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
            # Direct user to the homepage.
            return redirect(url_for('views.home'))
    return render_template("sign_up.html")