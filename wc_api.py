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
from protorpc import messages
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
# class PostMessage(messages.Message):
#     title = messages.StringField(1, required=True)
#     body = messages.StringField(2)

# class Request(messages.Message):
#     userID = messages.StringField(required=True)
#     token = messages.StringField(required=True)
#     execution_id = messages.StringField(required=True)
#     data = messages.StringField(1, required=True)

class Response(messages.Message):
    """ API Response data class """
    execution_id = messages.StringField(36, repeated=True, required=False)
    workflow_step = messages.StringField(20, repeated=True, required=True)
    user_message = messages.StringField(2048, repeated=True, required=False)
    input_required = messages.StringField(20, repeated=True, required=False)


def check_authentication(request):
    """ check authentication of incoming request against facebook oauth entry point """
    if (json.load(urllib2.urlopen('https://graph.facebook.com/me?fields=id&access_token=' + request.token))['id']) != request.userID:
        raise endpoints.UnauthorizedException('Invalid user_id or access_token')
    if hasattr(request, 'execution_id'):
        if ndb.Key(urlsafe=request.execution_id).get().owner != request.userID:
            raise endpoints.UnauthorizedException('Incorrect Owner')



@endpoints.api(name='wc',
            version='v1',
            allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID, IOS_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
            audiences=[WEB_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID])
class WCApi(remote.Service):
    """ API definition """

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


    @endpoints.method(message_types.VoidMessage, Response,
                    name='execution.resume', path='execution', http_method='POST',)
    def execution_resume(self, request):
        """ Resume a workflow execution """
        if not hasattr(request, 'execution_id'):
            spec_file = open("Workflow.json", "r").read()
            spec = JSONSerializer().deserialize_workflow_spec(spec_file)
            execution_object = Execution(owner=request.userID)
            execution = Workflow(spec)
            urlsafe_key = None
        else:
            execution_object = ndb.Key(urlsafe=request.execution_id).get()
            execution = DictionarySerializer().deserialize_workflow(execution_object.data)
            execution.complete_all()
            for waiting_task in execution._get_waiting_tasks():
                if isinstance(waiting_task.task_spec, UserInput):
                    for input_required in waiting_task.task_spec.args:
                        if hasattr(request, input_required):
                            waiting_task.set_data(**{input_required : getattr(request, input_required)})
            
            execution.complete_all()

            execution_object.data = execution.serialize(DictionarySerializer())
            urlsafe_key = execution_object.put().urlsafe()

        # get the next set of inputs required to be populated
        inputs_required = []
        for waiting_task in execution._get_waiting_tasks():
            if isinstance(waiting_task.task_spec, UserInput):
                for input_required in waiting_task.task_spec.args:
                    inputs_required = inputs_required + waiting_task.task_spec.args



        return Response(inputs_required=inputs_required, execution_id=urlsafe_key)


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
