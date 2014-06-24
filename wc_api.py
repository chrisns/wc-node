#!/usr/bin/env python
# coding=utf-8
"""REST api - this is the only python entry point for the app"""


from google.appengine.ext import ndb
import endpoints

from protorpc import message_types
from protorpc import remote
from SpiffWorkflow import *
# import logging
import urllib2
import json
from SpiffWorkflow.operators import *
from SpiffWorkflow.storage import JSONSerializer
from SpiffWorkflow.storage import DictionarySerializer
from SpiffWorkflow.Task import *
from WorkflowSpecs.UserInput import UserInput
from models.Execution import Execution
from models.api_requests_and_responses import *
import random
import string
from jsonschema.validators import Draft4Validator
from jsonschema.exceptions import best_match


WEB_CLIENT_ID = '84086224013-u450n6r4dkgr51v3pom39cqgsefrnm83.apps.googleusercontent.com'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'


def check_authentication(request):
    """ check authentication of incoming request against facebook oauth entry point """
    try:
        if (json.load(urllib2.urlopen('https://graph.facebook.com/me?fields=id&access_token=' + request.token))['id']) != request.user_id:
            raise endpoints.UnauthorizedException(
                'Invalid user_id or access_token')
    except ValueError:
        raise endpoints.UnauthorizedException(
            'Invalid user_id or access_token')
    if hasattr(request, 'execution_id') and request.execution_id is not None:
        if ndb.Key(urlsafe=request.execution_id).get().owner != request.user_id:
            raise endpoints.UnauthorizedException('Incorrect Owner')


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


def get_tasks_required(execution):
    """ returns required tasks given an execution """
    tasks_waiting = []
    for waiting_task in execution._get_waiting_tasks():
        if isinstance(waiting_task.task_spec, UserInput):
            tasks_waiting.append(waiting_task.task_spec.name)
    return tasks_waiting


def get_execution_new():
    """ returns a new execution """
    spec_file = get_workflow_spec_file_handler().read()
    spec = JSONSerializer().deserialize_workflow_spec(spec_file)
    execution = Workflow(spec)
    execution.complete_all()
    return execution


def get_workflow_spec_file_handler():
    """ get the workflow spec """
    return open("Workflow.json", "r")


@endpoints.api(name='wc',
               version='v1',
               allowed_client_ids=[
               WEB_CLIENT_ID, ANDROID_CLIENT_ID, IOS_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
               audiences=[WEB_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID])
class WCApi(remote.Service):

    """ API definition """

    @endpoints.method(execution_list_request, execution_list_response,
                      name='execution.list', path='execution/list', http_method='POST')
    def execution_list(self, request):
        """ List workflow executions """
        check_authentication(request)
        query = Execution.query(Execution.owner == 1234)
        response = execution_list_response()
        for key in query.iter(keys_only=True):
            response.executions.append(
                execution_list_summary_response(execution_id=key.urlsafe()))
        return response

    @endpoints.method(execution_new_request, execution_new_response,
                      name='execution.new', path='execution/new', http_method='POST')
    def execution_new(self, request):
        """ Returns the first inputs required from workflow """
        check_authentication(request)

        execution = get_execution_new()
        inputs_required = get_filtered_schema(execution)
        return execution_new_response(
            inputs_required=json.dumps(inputs_required),
        )

    @endpoints.method(execution_delete_request, message_types.VoidMessage,
                      name='execution.delete', path='execution/delete', http_method='POST')
    def execution_delete(self, request):
        """ Deletes the given execution """
        check_authentication(request)
        ndb.Key(urlsafe=request.execution_id).delete()
        return message_types.VoidMessage()

    @endpoints.method(execution_resume_request, execution_resume_response,
                      name='execution.resume', path='execution/resume', http_method='POST')
    def execution_resume(self, request):
        """ Resume a workflow execution """
        check_authentication(request)
        if request.execution_id is None:
            execution_object = Execution(owner=request.user_id)
            execution = get_execution_new()
        else:
            execution_object = ndb.Key(urlsafe=request.execution_id).get()
            execution = DictionarySerializer().deserialize_workflow(
                execution_object.data)

        execution.complete_all()

        if len(request.data) is not 0:
            for waiting_task in execution._get_waiting_tasks():
                if isinstance(waiting_task.task_spec, UserInput):
                    for response_data in request.data:
                        if response_data.key in waiting_task.task_spec.args:
                            for value in response_data.value:
                                waiting_task.set_data(
                                    **{response_data.key: value})
            execution.complete_all()

        execution_object.data = execution.serialize(DictionarySerializer())
        urlsafe_key = execution_object.put().urlsafe()

        return execution_resume_response(
            workflow_step=get_tasks_required(execution),
            inputs_required=json.dumps(get_filtered_schema(execution)),
            execution_id=urlsafe_key
        )

    @endpoints.method(message_types.VoidMessage, service_status_response,
                      name='service_status', path='service_status', http_method='GET')
    def service_status(self, request):
        """ return service status """
        from collections import namedtuple
        response = service_status_response(ndb=0, fb=0)
        try:
            if ndb.Key("execution", string.join(random.sample(string.digits, 8))).get() is None:
                response.ndb = 1
        except TypeError:  # pragma: no cover
            pass  # pragma: no cover
        except Exception:  # pragma: no cover
            pass  # pragma: no cover
        try:
            dummy_request_structure = namedtuple('MyStruct', 'user_id token')
            dummy_request = dummy_request_structure(user_id=1234, token='lala')
            check_authentication(dummy_request)
        except endpoints.UnauthorizedException:
            response.fb = 1  # pragma: no cover
        except TypeError:
            response.fb = 1
        except Exception:  # pragma: no cover
            pass  # pragma: no cover

        return response

APPLICATION = endpoints.api_server([WCApi], restricted=False)


# API Endpoints
# wfList(GET)
# wfStart(POST)
# wfResume(POST)
# wfGetWaiting(GET)
# messages(GET)
# lookup/%type(POST)
# storage(GET/POST/DELETE)

# WF helpers
# """
# def messages(type, msg):

# Set and retrieve messages to show to user, maintained in session storage
# If no parameters are defined then will return and reset the messages

# @type  type: integer
# @param type: constant of the type (debug/info/notice/warn/error/fatal)
# @type: msg:  string
# @param msg:  message to display to end user
# @rtype:      array
# @return:     de-duped array of messages to show to user

#   return
