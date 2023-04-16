from flask_app import app # import app to run routes
from flask import render_template, redirect, session, request, flash # flask modules for routes to work
from flask_app.models import user # import models
from flask_bcrypt import Bcrypt # import bcrypt to hash and encrypt passwords

bcrypt = Bcrypt(app) # create an object called bcrypt using app as the argument

@app.route('/') # loads default registration/login page
def load_login_page():
    if 'user_id' not in session: # if session hasn't been set, load the login page
        return render_template('login.html')
    return redirect('/dashboard') # otherwise go to the user's dashboard page

@app.route('/register', methods=['POST'])
def register_user():
    if not user.User.validate_registration(request.form): # validate user input to match required criteria
        session['form_in_progress'] = request.form # save progress so user can start where they left off if there are errors
        return redirect('/')
    if 'form_in_progress' in session:
        session.pop('form_in_progress')
    pw_hash = bcrypt.generate_password_hash(request.form['password']) # create a password hash
    data = {
        'fname': request.form['fname'],
        'lname': request.form['lname'],
        'email': request.form['email'],
        'password' : pw_hash # store password hash rather than the actual password
    }
    session['user_id'] = user.User.add_user(data) # set user id to what is returned from query
    return redirect('/dashboard')
@app.route('/login', methods=['POST'])
def login():
    user_in_db = user.User.get_user_by_email({'email': request.form['email']})
    if not user_in_db:
        flash('Invalid email/password', 'login')
        return redirect('/')
    # compare hash of entered password to hash saved in database
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid email/password', 'login')
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')
@app.route('/logout') # log out user by clearing session and redirecting to /
def logout():
    session.clear()
    return redirect('/')

