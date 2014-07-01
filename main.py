#!flask/bin/python
# coding=utf-8
"""`main` is the top level module for your Flask application."""

from flask import Flask
from flask import url_for
from flask import jsonify
from flask import request
from marshmallow import fields
from flask.ext.marshmallow import Marshmallow
from models.Execution import Execution
from google.appengine.ext import ndb

from py_utils.facebook_auth import *
import pprint

pprint.PrettyPrinter(indent=2)


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
    serialized = ExecutionCollectionMarshal(executions, many=True)
    response = {
        "collection": {
            "version" : 1.0,
            "href": url_for('executions'),
            "items" : serialized.data,
            "_links" : {
                'create' : url_for('execution_new')
            }
        }
    }
    return jsonify(response)


@app.route('/api/executions/<execution_id>')
def execution_detail(execution_id):
    execution = ndb.Key(urlsafe=execution_id).get()
    serialized = ExecutionMarshal(execution)
    return serialized.json

@app.route('/api/executions/create')
def execution_new(execution_id):
    #todo
    return "f"



class ExecutionCollectionMarshal(ma.Serializer):
    created = fields.Function(lambda obj: obj.created.isoformat())
    href = ma.URL('execution_detail', execution_id='<execution_id>')

class ExecutionMarshal(ma.Serializer):
    # todo
    created = fields.Function(lambda obj: obj.created.isoformat())
    href = ma.URL('execution_detail', execution_id='<execution_id>')
