#!flask/bin/python
# coding=utf-8
"""`main` is the top level module for your Flask application."""

from flask import Flask
from flask import url_for
from flask import jsonify
from flask import request
from flask import abort
from flask import redirect
from marshmallow import fields
from flask.ext.marshmallow import Marshmallow
from SpiffWorkflow import *
from WorkflowSpecs.UserInput import UserInput

from SpiffWorkflow.storage import JSONSerializer
from SpiffWorkflow.storage import DictionarySerializer
from models.Execution import Execution
from google.appengine.ext import ndb
from py_utils.facebook_auth import *
import pprint
import types

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
    response = jsonify({
        "error" : {
            "version": 1.0,
            "message": 'Sorry, Nothing at this URL.'
        }
    })
    response.status_code = 404
    return response

@app.errorhandler(400)
def auth_required(event):
    """Return a custom 404 error."""
    response = jsonify({
        "error" : {
            "version": 1.0,
            "message": 'Authentication required'
        }
    })
    response.status_code = 400
    return response

@app.errorhandler(SignedRequestError)
def handle_invalid_usage(error):
    response = jsonify({
        "error" : {
            "version": 1.0,
            "message": error.to_dict()
        }
    })
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


@app.route('/api/executions/<execution_id>', methods=['GET', 'POST', 'DELETE'])
@get_user_id
def execution_detail(user_id, execution_id):
    execution_object = ndb.Key(urlsafe=execution_id).get()
    if user_id != execution_object.owner:
        abort(404)

    if request.method is 'DELETE':
        ndb.Key(urlsafe=execution_id).delete()
        response = {
            "action": {
                "version" : 1.0,
                "status": "success",
            }
        }
        return jsonify(response)

    execution = DictionarySerializer().deserialize_workflow(execution_object.data)
    execution.complete_all()
    if request.method is 'POST':
        data = json.loads(request.data)
        # todo: validate against schema first
        for waiting_task in execution._get_waiting_tasks():
            if isinstance(waiting_task.task_spec, UserInput):
                # print request.data.keys()
                for key in data.keys():
                    if key in waiting_task.task_spec.args:
                        if isinstance(data[key], types.StringTypes):
                            waiting_task.set_data(**{key: data[key]})
                            pass
                        else:
                            for value in data[key]:
                                # todo: handle multiple value responses
                                waiting_task.set_data(**{key: data[key]})

            execution.complete_all()

        execution_object.data = execution.serialize(DictionarySerializer())
        execution_object.put()

    response = {
        "execution": {
            "version" : 1.0,
            "schema": get_filtered_schema(execution),
        }
    }
    return jsonify(response)

@app.route('/api/executions/create')
@get_user_id
def execution_new(user_id):
    execution_object = Execution(owner=user_id)
    spec_file = get_workflow_spec()
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

def get_workflow_spec():
    """ get the workflow spec """
    return open("Workflow.json", "r").read()

def get_filtered_schema(execution):
    """ returns required inputs given an execution """
    inputs_required = dict()
    inputs_matrix = get_schema()['properties']
    for waiting_task in execution._get_waiting_tasks():
        if isinstance(waiting_task.task_spec, UserInput):
            for input_required in waiting_task.task_spec.args:
                if input_required in inputs_matrix:
                    inputs_required[
                        input_required] = inputs_matrix[input_required]
                else:
                    raise Exception('Unmapped input', input_required)
    return inputs_required

def get_schema():
    """ get the json schema """
    return json.loads(open("schema.json", "r").read())