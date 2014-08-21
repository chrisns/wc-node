#!flask/bin/python
# coding=utf-8
"""`main` is the top level module for your Flask application."""

import types

from SpiffWorkflow.bpmn.BpmnWorkflow import BpmnWorkflow
from flask import Flask
from flask import url_for
from flask import jsonify
from flask import redirect
from flask.ext.marshmallow import Marshmallow
from google.appengine.ext import ndb
import jsonschema
from WorkflowGenerate import BpmnHelper

from py_utils.NDBBPMNSerializer import NDBBPMNSerializer
from models.Execution import Execution
from py_utils.bpmn_helpers import UserTask
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
                'queries': {
                    'description': 'List of queries',
                    'href': url_for('queries_list')
                },
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
def handle_invalid_usage(error):  # pragma: no cover
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
    serialized = ExecutionCollectionMarshal(executions)
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

@app.route('/api/queries')
def queries_list():
    """
    list of available queries and lookups
    @param user_id:
    @return: response
    """
    response = {
        "collection": {
            "version": 1.0,
            "href": url_for('queries_list'),
            "items": {
                'companies' : {
                    'description': 'Lookup of companies',
                    'href' : url_for('queries_companies')
                }
            },
        }
    }
    return jsonify(response)

@app.route('/api/queries/companies')
def queries_companies():
    """
    list of company stats
    @param user_id:
    @return: response
    """
    # print StoredValues.query(StoredValues.k == 'company').fetch(20)
    # executions = Execution.query( projection=[Execution.values.v]).fetch(20)
    # executions = ndb.gql('SELECT distinct values.v FROM Execution where values.k = \'company\'').fetch(20)
    # print executions
    # response = {}
    response = {
        "collection": {
            "version": 1.0,
            "href": url_for('queries_list'),
            "items": {
                'companies' : {
                    'description': 'Lookup of companies',
                    'href' : url_for('queries_companies')
                }
            },
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
    spec = get_workflow_spec()
    execution = NDBBPMNSerializer().deserialize_workflow(s_state=execution_object.data, wf_spec=spec)
    execution.complete_all()
    response = {
        "execution": {
            "version": 1.0,
            "execution_id": execution_object.execution_id,
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
    spec = get_workflow_spec()
    execution = NDBBPMNSerializer().deserialize_workflow(s_state=execution_object.data, wf_spec=spec)
    execution.complete_all()
    data = json.loads(request.data)
    schema = get_filtered_schema(execution)
    try:
        jsonschema.Draft4Validator(schema).validate(data)
    except Exception:
        raise Exception('schema/input mismatch')

    parse_data = dict()
    # noinspection PyProtectedMember
    for waiting_task in execution._get_waiting_tasks():
        if isinstance(waiting_task.task_spec, UserTask):
            for key in data.keys():
                if key in waiting_task.task_spec.args:
                    try:
                        for value in data[key]:
                            # todo: handle multiple value responses
                            waiting_task.set_data(**{key: data[key]})
                            parse_data.update(**{key: data[key]})
                    except TypeError, te:
                        parse_data.update(**{key: data[key]})
                        waiting_task.set_data(**{key: data[key]})
                        pass

    execution.complete_all()
    update_execution_index(schema, execution_object, parse_data)
    execution_object.data = execution.serialize(NDBBPMNSerializer())
    execution_object.put()
    return redirect(url_for('execution_get', execution_id=execution_object.key.urlsafe()))


def update_execution_index(schema, execution_object, parse_data):
    """
   Update the execution's key value index that is used for search ability
   this only works if the item in the execution in the schema is marked as 'indexed': true
   @param schema: jsonschema
   @param execution_object:
   @param parse_data: data that has been validated to be correct
   @return:
   """
    for k, v in parse_data.items():
        if schema['properties'][k].has_key('indexed'):
            execution_object.__setattr__(name = k, value=v)


# noinspection PyTypeChecker
@app.route('/api/executions/create', methods=['POST'])
@get_user_id
def execution_new(user_id):
    """
    create a new exception and redirect to it
    @param user_id:
    @return: flask.redirect
    """
    execution_object = Execution(owner=user_id)
    spec = get_workflow_spec()
    execution = BpmnWorkflow(spec)
    execution.complete_all()
    execution_object.data = execution.serialize(NDBBPMNSerializer())
    execution_id = execution_object.put().urlsafe()
    return redirect(url_for('.execution_get', execution_id=execution_id, _external=False))


class ExecutionCollectionMarshal:

    def __init__(self, executions):
        self.data = self.serialize_executions(executions)

    def serialize_executions(self, executions):
        data = []
        for execution in executions:
            data.append(self.serialize_execution(execution))
        return data
    def serialize_execution(self, execution):
        data = dict()
        data['execution_id'] = execution.key.urlsafe()
        data['type'] = execution.__class__.__name__
        data['href'] = url_for('execution_get', execution_id=execution.key.urlsafe())
        data['created'] = execution.created
        # data['values'] = self.serialize_values(values=execution.values)
        return data

    def serialize_values(self, values):
        vals = dict()
        for value in values:
            vals[value.k] = value.v
        return vals


def get_workflow_spec():
    """
    Get the workflow spec
    @return: workflow spec
    """
    # spec_file = open("WorkflowSpecs/Workflow-0.1.json").read()
    # spec = JSONSerializer().deserialize_workflow_spec(spec_file)
    spec = BpmnHelper().load_workflow_spec('WorkflowSpecs/Workflow-0.1.bpmn', 'workflow')
    return spec


def get_filtered_schema(execution):
    """
    returns required inputs given an execution
    @param execution:
    """
    inputs_required = dict()
    inputs_matrix = get_schema()['properties']
    # noinspection PyProtectedMember
    for waiting_task in execution._get_waiting_tasks():
        if isinstance(waiting_task.task_spec, UserTask):
            for input_required in waiting_task.task_spec.args:
                if input_required in inputs_matrix:
                    inputs_required[
                        input_required] = inputs_matrix[input_required]
                else:
                    raise Exception('Unmapped input ' + input_required)
    return {
        "$schema": "http://json-schema.org/schema#",
        "type": "object",
        "properties": inputs_required,
    }


def get_schema():
    """ get the json schema """
    return json.loads(open("schema.json").read())