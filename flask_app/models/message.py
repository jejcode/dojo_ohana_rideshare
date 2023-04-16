from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash # use flash to store validation messages

class Message:
    DB = 'ohana_rideshare_schema' # databse name
    def __init__(self, data) -> None:
        self.id = data['id']
        self.message = data['message']
        self.created_at = data['created_at']
        self.updated_at = data['id']
        self.ride = None
        self.user = None
    
    # CRUD
    # CREATE
    @classmethod
    def send_message(cls, data): # add message
        query = """ INSERT INTO messages (message, ride_id, user_id)
                VALUES (%(message)s, %(ride_id)s, %(user_id)s)"""
        return connectToMySQL(cls.DB).query_db(query, data)
    