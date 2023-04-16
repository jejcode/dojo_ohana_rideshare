from flask_app import app # import app to run routes
from flask import render_template, redirect, session, request, flash # flask modules for routes to work
from flask_app.models import user,ride # import models

@app.route('/dashboard') # default dashboard
def load_dashboard():
    if 'user_id' not in session: # can't access if not logged in
        return redirect('/')
    all_rides = ride.Ride.get_all_rides()
    if session['user_id'] in all_rides['all_users']:
        this_user = all_rides['all_users'][session['user_id']]
    else:
        this_user = user.User.get_user_by_id({'id': session['user_id']})
    return render_template('dashboard.html', this_user = this_user, rides = all_rides['requests'], claimed = all_rides['claimed'])

@app.route('/rides/new')
def new_ride():
    if 'user_id' not in session: # can't access if not logged in
        return redirect('/')
    return render_template('new_request.html')

@app.route('/rides/request', methods=['POST'])
def request_ride():
    if 'user_id' not in session: # can't access if not logged in
        return redirect('/')
    # form validation
    if not ride.Ride.validate_ride_request(request.form):
        return redirect('/rides/new')
    print(request.form)
    data = {
        'destination': request.form['destination'],
        'pickup_location': request.form['pickup_location'],
        'rideshare_date': request.form['rideshare_date'],
        'details': request.form['details'],
        'rider_id': session['user_id']
    }
    new_request = ride.Ride.add_ride(data)
    return redirect('/dashboard')

@app.route('/rides/delete/<int:id>') # route to delete ride request
def delete_request(id):
    if 'user_id' not in session: # can't access if not logged in
        return redirect('/')
    ride.Ride.delete_request({'id': id})
    return redirect('/dashboard')

@app.route('/rides/claim/<int:id>')
def claim_ride(id):
    if 'user_id' not in session: # can't access if not logged in
        return redirect('/')
    data = {
        'driver_id': session['user_id'],
        'ride_id': id
    }
    ride.Ride.can_drive(data) # add driver id to the db record for this ride
    return redirect('/dashboard')

@app.route('/rides/cancel/<int:id>')
def cancel_rideshare(id):
    if 'user_id' not in session:
        return redirect('/')
    ride.Ride.cancel_rideshare({'id': id}) # deletes driver_id from db record for this ride
    return redirect('/dashboard')

@app.route('/rides/<int:id>') # get class instance of one ride
def show_details(id):
    if 'user_id' not in session: # if not logged in, go away
        return redirect('/')
    this_rideshare = ride.Ride.get_one_ride({'id': id})
    return render_template('details.html', rideshare = this_rideshare)

@app.route('/rides/edit/<int:id>') # gets instance of ride for editing
def edit_ride(id):
    if 'user_id' not in session: # if not logged in, go away
        return redirect('/')
    this_rideshare = ride.Ride.get_one_ride({'id': id})
    return render_template('edit.html', rideshare = this_rideshare)

@app.route('/rides/edit/save', methods = ['POST'])
def save_edits():
    if 'user_id' not in session: # if not logged in, go away
        return redirect('/')
    # TODO validate form
    if not ride.Ride.validate_ride_edit(request.form):
        return redirect(f"/rides/edit/{request.form['ride_id']}")
    saved_edits = ride.Ride.edit_rideshare(request.form)
    return redirect(f"/rides/{request.form['ride_id']}")