#!/usr/bin/env python
"""REST api - this is the only python entry point for the app"""
import sys
sys.path.append("/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine")
sys.path.append("/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine/lib/endpoints-1.0")
sys.path.append("remotes/endpoints-proto-datastore")
sys.path.append("remotes/SpiffWorkflow")
sys.path.append("./remotes/gvgen")

from google.appengine.ext import ndb
import endpoints

# from endpoints_proto_datastore.ndb import EndpointsModel
from protorpc import message_types
from protorpc import remote
from SpiffWorkflow import *
# import logging
# import httplib
import urllib2
import json
from SpiffWorkflow.operators import *
from SpiffWorkflow.storage import JSONSerializer
from SpiffWorkflow.storage import DictionarySerializer
from SpiffWorkflow.Task import *
from WorkflowSpecs import *
from models import *
import random, string


WEB_CLIENT_ID = '84086224013-u450n6r4dkgr51v3pom39cqgsefrnm83.apps.googleusercontent.com'
WEB_CLIENT_ID = '292824132082.apps.googleusercontent.com'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'


# class Execution(ndb.Expando):
#     """Models an individual execution"""
#     owner = ndb.IntegerProperty(12, required=True)


# class Account(EndpointsModel):
    # _message_fields_schema = ('title', 'forename', 'surname')
    # owner    = ndb.UserProperty()
    # title    = ndb.StringProperty()
    # forename = ndb.StringProperty()
    # surname  = ndb.StringProperty()
    # created  = ndb.DateTimeProperty(auto_now_add=True)
    # updated  = ndb.DateTimeProperty(auto_now=True)


# class Execution(ndb.Expando):
#     date = ndb.DateTimeProperty(auto_now_add=True)
#     owner = ndb.UserProperty()
#     def to_message(self):
#     #   # Use datastore ID as ID for the Entry-Message
#     #   # Convert date to String for JSON output
#       return ExecutionMessage(
#                    name=self.name,
#                    date=self.date.strftime("%Y-%m-%dT%H:%M:%S"))
#     @classmethod
#     def query_entries(cls):
#         return cls.query()

# class ExecutionMessage(messages.Message):
#     name = messages.StringField(1, required=True)
#     date = messages.DateTimeField(2)

# class ExecutionCollection(messages.Message):
#     items = messages.MessageField(ExecutionMessage, 1, repeated=True)



def check_authentication(request):
    """ check authentication of incoming request against facebook oauth entry point """
    try:
        if (json.load(urllib2.urlopen('https://graph.facebook.com/me?fields=id&access_token=' + request.token))['id']) != request.user_id:
            raise endpoints.UnauthorizedException('Invalid user_id or access_token')
    except ValueError:
        raise endpoints.UnauthorizedException('Invalid user_id or access_token')
    if hasattr(request, 'execution_id') and request.execution_id is not None:
        if ndb.Key(urlsafe=request.execution_id).get().owner != request.user_id:
            raise endpoints.UnauthorizedException('Incorrect Owner')
       
def get_inputs_required(execution):
    """ returns required inputs given an execution """
    inputs_required = []
    inputs_matrix = json.loads(open("inputs.json", "r").read())
    for waiting_task in execution._get_waiting_tasks():
        if isinstance(waiting_task.task_spec, UserInput):
            for input_required in waiting_task.task_spec.args:
                if input_required in inputs_matrix:
                    inputs_required.append(build_from_mapped_obj(input_required, inputs_matrix[input_required]))
                else:
                    raise Exception('Unmapped workflow step')
    return inputs_required

def build_from_mapped_obj(name = None, obj = None):
    return user_input(
        name = name,
        label = obj['label'] if 'label' in obj else None,
        input_type = obj['input_type'] if 'input_type' in obj else None,
        placeholder = obj['placeholder'] if 'placeholder' in obj else None,
        description = obj['description'] if 'description' in obj else None,
        options = obj['options'] if 'options' in obj else [],
        validator = obj['validator'] if 'validator' in obj else None,
        autocomplete_path = obj['autocomplete_path'] if 'autocomplete_path' in obj else None,
        default_value = obj['default_value'] if 'default_value' in obj else None,
    )

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
    return open("Workflow.json", "r")

@endpoints.api(name='wc',
            version='v1',
            allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID, IOS_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
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
            response.executions.append(execution_list_summary_response(execution_id=key.urlsafe()))
        return response

    @endpoints.method(execution_new_request, execution_new_response,
                    name='execution.new', path='execution/new', http_method='POST')
    def execution_new(self, request):
        """ Returns the first inputs required from workflow """
        check_authentication(request)

        execution = get_execution_new()
        inputs_required = get_inputs_required(execution)

        return execution_new_response(
            inputs_required=inputs_required, 
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
            execution = DictionarySerializer().deserialize_workflow(execution_object.data)

        execution.complete_all()

        if len(request.data) is not 0:
            for waiting_task in execution._get_waiting_tasks():
                if isinstance(waiting_task.task_spec, UserInput):
                    for response_data in request.data:
                        if response_data.key in waiting_task.task_spec.args:
                            for value in response_data.value:
                                waiting_task.set_data(**{response_data.key : value})
            execution.complete_all()

        execution_object.data = execution.serialize(DictionarySerializer())
        urlsafe_key = execution_object.put().urlsafe()

        return execution_resume_response(
            workflow_step=get_tasks_required(execution),
            inputs_required=get_inputs_required(execution),
            execution_id=urlsafe_key
        )

    # @endpoints.method(message_types.VoidMessage, Response,
    #                 name='execution.submit', path='execution', http_method='POST',)
    # def execution_response(self, request):
    #     """ restore execution if one exists with given uuid else make one """
    #     # check_authentication(request)
    #     if hasattr(request, 'execution_id'):
    #         restored_data = ndb.Key(urlsafe=request.execution_id).get()
    #         if restored_data in locals():
    #             execution = DictionarySerializer().deserialize_workflow(restored_data.data)
    #     else:
    #         spec_file = open("Workflow.json", "r").read()
    #         spec = JSONSerializer().deserialize_workflow_spec(spec_file)

    #         execution = Workflow(spec)

    #     execution.complete_all()
    #     input_required = []
    #     for waiting_task in execution._get_waiting_tasks():
    #         if isinstance(waiting_task.task_spec, UserInput):
    #             input_required = input_required + waiting_task.task_spec.args
    #         logging.error(waiting_task.task_spec.__class__)
    #     return Response(input_required=input_required)


    # @endpoints.method(Request, PostMessage,
    #                 name='execution.submit', path='execution', http_method='POST',)
    # def list_posts(self, request):
    #     check_authentication(request)
    #     return PostMessage(title=request.userID, body="there")
    # @Account.query_method(user_required=True,
    #                       path='user', name='account.get')
    # def AccountGet(self, query):
    #   return query.filter(Account.owner == endpoints.get_current_user())



    # @endpoints.method(message_types.VoidMessage, Greeting,
    #                   path='hellogreeting/authed', http_method='POST',
    #                   name='greetings.authed')
    # def greeting_authed(self, request):
    #     current_user = endpoints.get_current_user()
    #     email = (current_user.email() if current_user is not None
    #              else 'Anonymous')
    #     # print "hihi"
    #     # print get_current_user().user_id()
    #     # print
    #     # key = ndb.Key("user", email)
    #     # print UserEntity.query_book(ancestor_key=key).fetch(20)
    #     # return Greeting(message=UserEntity.query_book(ancestor_key=key).fetch(1))
    #     # Account(email=endpoints.get_current_user().email(), greeting = STORED_GREETINGS.items[request.id].message).put()
    #     # print Account(id=).get()
    #     # print key('Account', endpoints.get_current_user().email()).get()
    #     # account = Account.get_by_id(id=endpoints.get_current_user().email()).greeting
    #     # print account.greeting
    #     return Greeting(message='hello %s %s' % (email, account,))



    # @endpoints.method(message_types.VoidMessage, ExecutionCollection,
    #                   path='wfList', http_method='GET',
    #                   name='wf.listExecutions')
    # def list_executions(self, unused_request):#
    #     # Account.get_by_id(id=endpoints.get_current_user().email()).greeting
    #     # test  = Execution(owner=endpoints.get_current_user(), name='Some Name')
    #     # test.put()
    #     # print test
    #     # print(Execution.query())
    #     # return ExecutionCollection(Execution.query())
    #     # query = Execution.query().fetch()
    #     # print query

    #     # items = [execution for execution in query.fetch()]
    #     # print items
    #     # items = Execution.query
    #     # print Execution.list()
    #     items = Execution.query_entries()

    #     # items = [entity.to_message() for entity in query.fetch()]
    #     # items = [ExecutionMessage(name=p.name, date=p.date) for p in Execution.query()]
    #     return ExecutionCollection(items=items) 
    #     return STORED_GREETINGS
    @endpoints.method(message_types.VoidMessage, service_status_response,
                    name='service_status', path='service_status', http_method='GET')
    def service_status(self, request):
        """ return service status """
        from collections import namedtuple
        response = service_status_response(ndb=0, fb=0)
        try:
            if ndb.Key("execution", string.join(random.sample(string.digits, 8))).get() is None:
                response.ndb = 1
        except Exception:
            pass
        try:
            dummy_request_structure = namedtuple('MyStruct', 'user_id token')
            dummy_request = dummy_request_structure(user_id=1234, token='lala')
            check_authentication(dummy_request)
        except endpoints.UnauthorizedException:
            response.fb = 1
        except TypeError:
            response.fb = 1            
        except Exception:
            pass

        return response

APPLICATION = endpoints.api_server([WCApi], restricted=False)


## API Endpoints
# wfList(GET)
# wfStart(POST)
# wfResume(POST)
# wfGetWaiting(GET)
# messages(GET)
# lookup/%type(POST)
# storage(GET/POST/DELETE)

## WF helpers
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
