#!flask/bin/python
# coding=utf-8
"""`main` is the top level module for your Flask application."""

import types

from flask import Flask
from flask import url_for
from flask import jsonify
from flask import redirect
from marshmallow import fields
from flask.ext.marshmallow import Marshmallow
from SpiffWorkflow import *
from SpiffWorkflow.storage import JSONSerializer
from SpiffWorkflow.storage import DictionarySerializer
from google.appengine.ext import ndb

from WorkflowSpecs.UserInput import UserInput
from models.Execution import Execution
from py_utils.facebook_auth import *


app = Flask(__name__, static_url_path="")
app.config['MARSHMALLOW_DATEFORMAT'] = 'iso'
app.config['JSON_SORT_KEYS'] = False
# noinspection PyTypeChecker
ma = Marshmallow(app)


@app.route('/api')
def root():
    """Return a friendly HTTP greeting."""
    routes = {
        'collection': {
            'version': 1.0,
            'items': {
                'executions': {
                    'description': 'List of executions',
                    'authentication_required': True,
                    'href': url_for('executions_list')
                }
            }
        }
    }
    return jsonify(routes)


# noinspection PyUnusedLocal
@app.errorhandler(404)
def page_not_found(event):
    """Return a custom 404 error.
    @param event:
    """
    response = jsonify({
        "error": {
            "version": 1.0,
            "message": 'Sorry, Nothing at this URL.'
        }
    })
    response.status_code = 404
    return response


# noinspection PyUnusedLocal
@app.errorhandler(400)
def auth_required(event):
    """Return a custom 404 error.
    @param event:
    """
    response = jsonify({
        "error": {
            "version": 1.0,
            "message": 'Authentication required'
        }
    })
    response.status_code = 400
    return response


@app.errorhandler(SignedRequestError)
def handle_invalid_usage(error): #pragma: no cover
    """
    error handler for signed request errors
    @type error: py_utils.facebook_auth.SignedRequestError
    @return:
    """
    response = jsonify({
        "error": {
            "version": 1.0,
            "message": error.to_dict()
        }
    })
    response.status_code = error.status_code
    return response


@app.route('/api/executions')
@get_user_id
def executions_list(user_id):
    """
    list of executions
    @param user_id:
    @return: response
    """
    executions = Execution.query(Execution.owner == user_id).fetch(20)
    serialized = ExecutionCollectionMarshal(executions, many=True)
    response = {
        "collection": {
            "version": 1.0,
            "href": url_for('executions_list'),
            "items": serialized.data,
            "_links": {
                'create': {
                    'href': url_for('execution_new'),
                }
            }
        }
    }
    return jsonify(response)


def get_execution_object(f):
    """
    Get the execution object based on the request only if it belongs to the correct user
    @param f:
    """

    @get_user_id
    @wraps(f)
    def decorated_function(user_id, execution_id, *args, **kwargs):
        """
        Decorate function
        @param user_id:
        @param execution_id:
        @param args:
        @param kwargs:
        @return object execution object:
        """
        execution_object = ndb.Key(urlsafe=execution_id).get()

        if user_id != execution_object.owner:
            abort(404)
        return f(execution_object=execution_object, user_id=user_id, *args, **kwargs)

    return decorated_function


# noinspection PyUnresolvedReferences,PyUnusedLocal
@app.route('/api/executions/<execution_id>', methods=['DELETE'])
@get_execution_object
def execution_delete(user_id, execution_object):
    """
    Delete an execution
    @param user_id:
    @param execution_object:
    @return: json
    """
    execution_object.key.delete()
    response = {
        "action": {
            "version": 1.0,
            "status": "success",
        }
    }
    return jsonify(response)


# noinspection PyUnusedLocal,PyUnresolvedReferences
@app.route('/api/executions/<execution_id>', methods=['GET'])
@get_execution_object
def execution_get(user_id, execution_object):
    """
    get the execution detail
    @param user_id:
    @param execution_object:
    @return: json
    """
    execution = DictionarySerializer().deserialize_workflow(execution_object.data)
    execution.complete_all()
    response = {
        "execution": {
            "version": 1.0,
            "schema": get_filtered_schema(execution),
        }
    }
    return jsonify(response)


# noinspection PyUnusedLocal,PyUnresolvedReferences
@app.route('/api/executions/<execution_id>', methods=['POST'])
@get_execution_object
def execution_post(user_id, execution_object):
    """
    submit responses to the execution
    @param user_id:
    @param execution_object:
    @return: flask.redirect
    """
    execution = DictionarySerializer().deserialize_workflow(execution_object.data)
    execution.complete_all()
    data = json.loads(request.data)
    # todo: validate against schema first
    # noinspection PyProtectedMember
    for waiting_task in execution._get_waiting_tasks():
        if isinstance(waiting_task.task_spec, UserInput):
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
    return redirect(url_for('execution_get', execution_id=execution_object.key.urlsafe()))


# noinspection PyTypeChecker
@app.route('/api/executions/create')
@get_user_id
def execution_new(user_id):
    """
    create a new exception and redirect to it
    @param user_id:
    @return: flask.redirect
    """
    execution_object = Execution(owner=user_id)
    spec_file = get_workflow_spec()
    spec = JSONSerializer().deserialize_workflow_spec(spec_file)
    execution = Workflow(spec)
    execution.complete_all()
    execution_object.data = execution.serialize(DictionarySerializer())
    execution_id = execution_object.put().urlsafe()
    return redirect(url_for('execution_get', execution_id=execution_id))


class ExecutionCollectionMarshal(ma.Serializer):
    """
    Serializer for collections of executions
    """
    # noinspection PyUnresolvedReferences
    href = ma.URL('execution_get', execution_id='<execution_id>')
    type = fields.Function(lambda obj: obj.__class__.__name__)

    class Meta:
        """ Meta serializer class """
        additional = ['execution_id', 'created', 'type']


def get_workflow_spec():
    """ get the workflow spec """
    return open("Workflow.json").read()


def get_filtered_schema(execution):
    """ returns required inputs given an execution
    @param execution:
    """
    inputs_required = dict()
    inputs_matrix = get_schema()['properties']
    # noinspection PyProtectedMember
    for waiting_task in execution._get_waiting_tasks():
        if isinstance(waiting_task.task_spec, UserInput):
            for input_required in waiting_task.task_spec.args:
                if input_required in inputs_matrix:
                    inputs_required[
                        input_required] = inputs_matrix[input_required]
                else:
                    raise Exception('Unmapped input')
    return inputs_required


def get_schema():
    """ get the json schema """
    return json.loads(open("schema.json").read())