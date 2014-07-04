#!flask/bin/python
# coding=utf-8
"""`main` is the top level module for your Flask application."""

from flask import Flask
from flask import url_for
from flask import jsonify
from flask import request
from flask import redirect
from marshmallow import fields
from flask.ext.marshmallow import Marshmallow
from SpiffWorkflow import *

from SpiffWorkflow.storage import JSONSerializer
from SpiffWorkflow.storage import DictionarySerializer
from models.Execution import Execution
from google.appengine.ext import ndb
from functools import wraps
from py_utils.facebook_auth import *
import pprint

pprint.PrettyPrinter(indent=2)


app = Flask(__name__, static_url_path="")
app.config['MARSHMALLOW_DATEFORMAT'] = 'iso'
app.config['JSON_SORT_KEYS'] = False
ma = Marshmallow(app)


@app.route('/api')
def root():
    """Return a friendly HTTP greeting."""
    routes = {
        'collection': {
            'version': 1.0,
            'items':{
                'executions': {
                    'description': 'List of executions',
                    'authentication_required': True,
                    'href': url_for('executions')
                }
            }
        }
    }
    return jsonify(routes)


@app.errorhandler(404)
def page_not_found(event):
    """Return a custom 404 error."""
    response = jsonify({"message" : 'Sorry, Nothing at this URL.'})
    response.status_code = 404
    return response

def get_user_id(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = facebook_auth.get_user_id(request)
        if user_id is None:
           raise SignedRequestError(
            "User not authenticated", status_code=400)
        return f(user_id, *args, **kwargs)
    return decorated_function

@app.errorhandler(SignedRequestError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/api/executions')
@get_user_id
def executions(user_id):
    executions = Execution.query(Execution.owner == user_id).fetch(20)
    serialized = ExecutionCollectionMarshal(executions, many=True)
    response = {
        "collection": {
            "version" : 1.0,
            "href": url_for('executions'),
            "items" : serialized.data,
            "_links" : {
                'create' : {
                    'href' : url_for('execution_new'),
                }
            }
        }
    }
    return jsonify(response)


@app.route('/api/executions/<execution_id>')
def execution_detail(execution_id):
    execution_object = ndb.Key(urlsafe=execution_id).get()
    execution = DictionarySerializer().deserialize_workflow(execution_object.data)
    execution.complete_all()
    print execution
    response = {
        "collection": {
            "version" : 1.0,
            "href": url_for('executions'),
            "_links" : {
                'create' : {
                    'href' : url_for('execution_new'),
                }
            }
        }
    }
    return jsonify(response)

@app.route('/api/executions/create')
@get_user_id
def execution_new(user_id):
    execution_object = Execution(owner=user_id)
    spec_file = get_workflow_spec_file_handler().read()
    spec = JSONSerializer().deserialize_workflow_spec(spec_file)
    execution = Workflow(spec)
    execution.complete_all()
    execution_object.data = execution.serialize(DictionarySerializer())
    execution_id = execution_object.put().urlsafe()
    return redirect(url_for('execution_detail', execution_id=execution_id), code=302)



class ExecutionCollectionMarshal(ma.Serializer):
    href = ma.URL('execution_detail', execution_id='<execution_id>')
    type = fields.Function(lambda obj: obj.__class__.__name__)

    class Meta:
        additional = ['execution_id', 'created', 'type']

class ExecutionMarshal(ma.Serializer):
    created = fields.Function(lambda obj: obj.created.isoformat())
    type = fields.Function(lambda obj: obj.__class__.__name__)
    href = ma.URL('execution_detail', execution_id='<execution_id>')
    class Meta:
        additional = ['execution_id', 'created', 'type']

def get_workflow_spec_file_handler():
    """ get the workflow spec """
    return open("Workflow.json", "r")