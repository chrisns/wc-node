#!flask/bin/python
# coding=utf-8
"""`main` is the top level module for your Flask application."""

from flask import Flask
from flask import jsonify
from flask import request
from marshmallow import fields
from flask.ext.marshmallow import Marshmallow
from models.Execution import Execution
from google.appengine.ext import ndb

from py_utils.facebook_auth import *


app = Flask(__name__, static_url_path="")
ma = Marshmallow(app)


@app.route('/api')
def hello():
    """Return a friendly HTTP greeting."""
    print get_user_id(request)
    return jsonify({'tasks': get_user_id(request)})


@app.errorhandler(404)
def page_not_found(event):
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


@app.route('/api/executions/')
def executions():
    executions = Execution.query(Execution.owner == 1234).fetch(20)
    serialized = ExecutionMarshal(executions , many=True)
    return serialized.json


@app.route('/api/executions/<execution_id>')
def execution_detail(execution_id):
    execution = ndb.Key(urlsafe=execution_id).get()
    serialized = ExecutionMarshal(execution)
    return serialized.json



class ExecutionMarshal(ma.Serializer):
    execution_id = fields.Method('get_url_safe_key')

    class Meta:
        # Fields to expose
        fields = ['execution_id', '_links']




    def get_url_safe_key(self, obj):
        return obj.key.urlsafe()
    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URL('execution_detail', execution_id='<execution_id>'),
        'collection': ma.URL('executions')
    })
