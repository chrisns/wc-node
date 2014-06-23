#!flask/bin/python
"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask
from flask import jsonify
from flask import request
from py_utils.facebook_auth import *

app = Flask(__name__, static_url_path="")
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/api')
def hello():
    """Return a friendly HTTP greeting."""
    print get_user_id(request)
    return jsonify({'tasks': get_user_id(request)})
    return 'Hello World!'


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route('/api/todo', methods=['GET'])
def get_tasks():
    # print parse_signed_request(request)
    return jsonify({'tasks': tasks})


@app.errorhandler(SignedRequestError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
