from flask_app import app # import the app so the app will run

#import controllers and templates
from flask_app.controllers import users, rides, messages

if __name__ == '__main__': # run the app
    app.run(debug = True, port = 5001)