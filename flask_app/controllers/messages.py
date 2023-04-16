from flask_app import app # import app to run routes
from flask_app.models import message
from flask import redirect, request

@app.route('/messages/send', methods=['POST'])
def post_message():
    print(request.form)
    message.Message.send_message(request.form)
    return redirect(f"/rides/{request.form['ride_id']}")