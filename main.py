#!flask/bin/python
"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask
from flask import jsonify
from flask import request

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


import base64
import hashlib
import hmac
import json


def get_user_id(request):
    parsed = parse_signed_request(
        request.cookies.get('fbsr_665447500158300'), '0089bed38bc2aced1cd85020ffc4e527')
    return parsed['user_id']


def urlsafe_b64decode(str):
    """Perform Base 64 decoding for strings with missing padding."""

    l = len(str)
    pl = l % 4
    return base64.urlsafe_b64decode(str.ljust(l + pl, "="))


def parse_signed_request(signed_request, secret):
    """
    Parse signed_request given by Facebook (usually via POST),
    decrypt with app secret.

    Arguments:
    signed_request -- Facebook's signed request given through POST
    secret -- Application's app_secret required to decrpyt signed_request
    """
    try:
        esig, payload = signed_request.split(".")
    except Exception:
        raise SignedRequestError("Malformed signed request", status_code=410)

    sig = urlsafe_b64decode(str(esig))
    data = json.loads(urlsafe_b64decode(str(payload)))

    if not isinstance(data, dict):
        raise SignedRequestError(
            "Payload is not a json string", status_code=410)

    if data["algorithm"].upper() == "HMAC-SHA256" and hmac.new(secret, payload, hashlib.sha256).digest() == sig:
            return data

    else:
        raise SignedRequestError("Not HMAC-SHA256 encrypted!", status_code=410)

    return {}


class SignedRequestError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(SignedRequestError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
