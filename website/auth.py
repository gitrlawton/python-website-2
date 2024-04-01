from flask import Blueprint

from flask import render_template, request

from flask import flash

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
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        # Check if data sent with POST request (ie. the form input data)
        # is valid.
        if len(email) < 4:
            flash('Email must be longer than 3 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash("Paswords don't match.", category='error')
        elif len(password1) < 7:
            flash('Password must be longer than 6 characters.', category='error')
        else:
            flash('Account created.', category='success')
    return render_template("sign_up.html")