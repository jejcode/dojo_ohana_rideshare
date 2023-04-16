from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user, message

class Ride:
    DB = 'ohana_rideshare_schema' # databse name
    def __init__(self, data) -> None:
        self.id = data['id']
        self.destination = data['destination']
        self.pickup_location = data['pickup_location']
        self.rideshare_date = data['rideshare_date']
        self.details = data['details']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.rider = None
        self.driver = None
        self.messages = []
    
    # CRUD
    # CREATE
    @classmethod
    def add_ride(cls, data): # add one record to db table
        query = """ INSERT INTO rides (destination, pickup_location, rideshare_date, details, rider_id)
                VALUES (%(destination)s, %(pickup_location)s, %(rideshare_date)s, %(details)s, %(rider_id)s);
                """
        return connectToMySQL(cls.DB).query_db(query, data)
    # READ
    @classmethod
    def get_one_ride(cls, data): # get record of one by id
        query = """
            SELECT * FROM rides 
            LEFT JOIN users ON rider_id = users.id
            LEFT JOIN users AS drivers ON driver_id = drivers.id 
            LEFT JOIN messages ON rides.id = ride_id
            LEFT JOIN users AS senders ON messages.user_id = senders.id
            WHERE rides.id = %(id)s
            """
        results = connectToMySQL(cls.DB).query_db(query, data) # result will be a list of 1
        # create user instances for rider and if it exists, driver
        this_ride_data = { # dictionary to make an instance
                    'id': results[0]['id'],
                    'destination': results[0]['destination'],
                    'pickup_location': results[0]['pickup_location'],
                    'rideshare_date': results[0]['rideshare_date'],
                    'details': results[0]['details'],
                    'created_at': results[0]['created_at'],
                    'updated_at': results[0]['updated_at'],
                }
        this_ride = cls(this_ride_data) # create an instance of the result
        this_rider_data = {
                        'id': results[0]['users.id'],
                        'first_name': results[0]['first_name'],
                        'last_name': results[0]['last_name'],
                        'email': results[0]['email'],
                        'password': results[0]['password'],
                        'created_at': results[0]['users.created_at'],
                        'updated_at': results[0]['users.updated_at']
                    }
        # create user instance for rider
        #connect rider to ride
        this_ride.rider = user.User(this_rider_data)
        if results[0]['drivers.id']: # if there is a driver, create an instance of them
            this_driver_data = {
                            'id': results[0]['drivers.id'],
                            'first_name': results[0]['drivers.first_name'],
                            'last_name': results[0]['drivers.last_name'],
                            'email': results[0]['drivers.email'],
                            'password': results[0]['drivers.password'],
                            'created_at': results[0]['drivers.created_at'],
                            'updated_at': results[0]['drivers.updated_at']
                        }
            # and link it to the ride class instance
            this_ride.driver = user.User(this_driver_data)
        # if there are messages, make an instnace of each one and append them to self.messages
        for db_row in results:
            if db_row['messages.id']:
                this_row_message = {
                    'id': db_row['id'],
                    'message': db_row['message'],
                    'created_at': db_row['created_at'],
                    'updated_at': db_row['updated_at'],
                }
                # link ride to message
                this_message = message.Message(this_row_message)
                this_message.ride = this_ride
                # link message to ride
                this_ride.messages.append(this_message)
                # create instance of message poster and link it
                this_poster_data = {
                            'id': db_row['senders.id'],
                            'first_name': db_row['senders.first_name'],
                            'last_name': db_row['senders.last_name'],
                            'email': db_row['senders.email'],
                            'password': db_row['senders.password'],
                            'created_at': db_row['senders.created_at'],
                            'updated_at': db_row['senders.updated_at']
                        }
                this_message.user = user.User(this_poster_data)
                
        return this_ride
    @classmethod
    def get_all_rides(cls): # get all records
        query = """
        SELECT * FROM rides
        LEFT JOIN users ON rider_id = users.id
        LEFT JOIN users AS drivers ON driver_id = drivers.id 
        """
        results = connectToMySQL(cls.DB).query_db(query) # results is a list
        if len(results) == 0: # don't try and process an empty list
            return {
                'requests': [],
                'claimed': []
            }
        all_requests = [] # instances without drivers will go here
        all_claimed = [] # instances with driver will go here
        user_hash = {}
        for db_row in results:
            #first figure out if this entry is a request or accepted:
            ride_type = all_requests if not db_row['drivers.id'] else all_claimed
            
            # if an instance has not already been made for this ride, make it
            if len(ride_type) == 0 or ride_type[-1].id != db_row['id']: 
                this_row_request = { # dictionary to make an instance
                    'id': db_row['id'],
                    'destination': db_row['destination'],
                    'pickup_location': db_row['pickup_location'],
                    'rideshare_date': db_row['rideshare_date'],
                    'details': db_row['details'],
                    'created_at': db_row['created_at'],
                    'updated_at': db_row['updated_at'],
                }
                this_request = cls(this_row_request)
                ride_type.append(this_request) # add current ride to the appropriate list

                # create a user instance of rider if it doesn't already exist
                if db_row['users.id'] not in user_hash:
                    this_row_rider = {
                        'id': db_row['users.id'],
                        'first_name': db_row['first_name'],
                        'last_name': db_row['last_name'],
                        'email': db_row['email'],
                        'password': db_row['password'],
                        'created_at': db_row['users.created_at'],
                        'updated_at': db_row['users.updated_at']
                    }
                    user_hash[db_row['users.id']] = user.User(this_row_rider)
                # link this user to their ride
                user_hash[db_row['users.id']].rides.append(this_request)
                this_request.rider = user_hash[db_row['users.id']]
                
                # create instance of driver if it doesn't already exist
                if db_row['drivers.id']:
                    if db_row['drivers.id'] not in user_hash: # if there is a driver, but there is not instance, create one
                        this_row_driver = {
                            'id': db_row['drivers.id'],
                            'first_name': db_row['drivers.first_name'],
                            'last_name': db_row['drivers.last_name'],
                            'email': db_row['drivers.email'],
                            'password': db_row['drivers.password'],
                            'created_at': db_row['drivers.created_at'],
                            'updated_at': db_row['drivers.updated_at']
                        }
                        user_hash[db_row['drivers.id']] = user.User(this_row_driver)
                    # link driver to this drive
                    this_request.driver = user_hash[db_row['drivers.id']]
                    user_hash[db_row['drivers.id']].drives = this_request
        return {
            'all_users': user_hash,
            'requests': all_requests,
            'claimed': all_claimed
        }
    # UPDATE
    @classmethod
    def can_drive(cls, data): # sets driver id on a prexisting db row
        query = """UPDATE rides 
                SET driver_id = %(driver_id)s
                WHERE id = %(ride_id)s"""
        return connectToMySQL(cls.DB).query_db(query, data)
    @classmethod
    def cancel_rideshare(cls, data): # deletes driver Id 
        query = "UPDATE rides SET driver_id = null WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query, data)
    @classmethod
    def edit_rideshare(cls, data): # saves edits made to ride details
        query  = "UPDATE rides SET pickup_location = %(pickup_location)s, details = %(details)s"
        return connectToMySQL(cls.DB).query_db(query, data)
    # DELETE
    @classmethod
    def delete_request(cls, data):
        query = "DELETE FROM rides WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    # Form validations
    @staticmethod
    def validate_ride_request(data): # validate new ride requests
        is_valid = True
        if len(data['destination']) < 3:
            flash('Destination must be at least 3 characters.', 'requests')
            is_valid = False
        if len(data['pickup_location']) < 3:
            flash('Pick-up location must be at least 3 characters.', 'requests')
            is_valid = False
        if len(data['details']) < 10:
            flash('Details must be at least 10 characters.', 'requests')
            is_valid = False
        if not data['rideshare_date']:
            flash('Date must be valid.', 'requests')
            is_valid = False
        return is_valid
    @staticmethod
    def validate_ride_edit(data):
        is_valid = True
        if len(data['pickup_location']) < 3:
            flash('Pick-up location must be at least 3 characters.', 'edits')
            is_valid = False
        if len(data['details']) < 10:
            flash('Details must be at least 10 characters.', 'edits')
            is_valid = False
        return is_valid