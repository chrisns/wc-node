#!flask/bin/python
# coding=utf-8
"""`main` is the top level module for your Flask application."""

from flask import Flask
from flask import jsonify
from flask import request
from flask.ext.marshmallow import Marshmallow
from models.Execution import Execution
from google.appengine.ext import ndb

from py_utils.facebook_auth import *


app = ndb.toplevel(Flask(__name__, static_url_path=""))
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
    usetestbed()
    executions_list = []
    executions = Execution.query(Execution.owner == 1234).fetch(20)
    for execution in executions:
        executions_list.append({'execution_id': execution.key.urlsafe(), 'owner': execution.owner})
    serialized = ExecutionMarshal(executions_list , many=True)
    return serialized.json


def usetestbed():
    from google.appengine.ext import testbed

    testbed = testbed.Testbed()
    testbed.setup_env(current_version_id='testbed.version')
    testbed.activate()
    testbed.init_datastore_v3_stub()
    Execution(owner=1234, data='mee').put()
    Execution(owner=1234, data='dee').put()
    Execution(owner=1234, data='bee').put()


@app.route('/api/executions/<execution_id>')
def execution_detail(execution_id):
    usetestbed()
    execution = ndb.Key(urlsafe=execution_id).get()
    serialized = ExecutionMarshal(execution)
    return serialized.json



class ExecutionMarshal(ma.Serializer):
    class Meta:
        # Fields to expose
        fields = ('execution_id', 'owner')

    # Smart hyperlinking
    # _links = ma.Hyperlinks({
        # 'self': ma.URL('execution_detail', execution_id='<execution_id>'),
    #     'collection': ma.URL('executions')
    # })
