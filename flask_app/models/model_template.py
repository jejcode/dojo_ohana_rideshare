from flask_app.config.mysqlconnection import connectToMySQL

class Somename:
    DB = '' # databse name
    def __init__(self, data) -> None:
        self.id = data['id']
    
    # CRUD
    # CREATE
    @classmethod
    def add_one(cls, data): # add one record to db table
        query = """ INSERT INTO table (column_1_name, column_2_name)
                VALUES (%(key1)s, %(key2)s)"""
        return connectToMySQL(cls.DB).query_db(query, data)
    # READ
    @classmethod
    def get_one(cls, data): # get record of one by id
        query = "SELECT * FROM table WHERE id = %(id)s"
        results = connectToMySQL(cls.DB).query_db(query, data) # result will be a list of 1
        return cls(results[0])
    @classmethod
    def get_all(cls, data): # get all records
        query = """
        SELECT * FROM table
        """
        results = connectToMySQL(cls.DB).query_db(query) # results is a list
        list_store = [] # empty list to store instances once they're created
        if len(results) == 0: # don't try and process an empty list
            return 0
        for db_row in results:
            this_row = { # dictionary to make an instance
                'id': db_row['id']
            }
            list_store.append(cls(this_row)) # make an instance and add it to the list to return
        return list_store
    # UPDATE
    @classmethod
    def edit(cls, data):
        query = """UPDATE table_name 
                SET column1 = value1, column2 = value2
                WHERE id = %(id)s"""
        return connectToMySQL(cls.DB).query_db(query, data)
    # DELETE
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM table_name WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query, data)