from google.appengine.ext import ndb
import endpoints
sys.path.append("remotes/endpoints-proto-datastore")
from endpoints_proto_datastore.ndb import EndpointsModel
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from google.appengine.api import users
import sys
sys.path.append("remotes/SpiffWorkflow")
from SpiffWorkflow import *
import logging
import httplib
import urllib2
import json

WEB_CLIENT_ID = '84086224013-u450n6r4dkgr51v3pom39cqgsefrnm83.apps.googleusercontent.com'
WEB_CLIENT_ID = '292824132082.apps.googleusercontent.com'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'


class Account(EndpointsModel):
  _message_fields_schema = ('title', 'forename', 'surname')
  owner    = ndb.UserProperty()
  title    = ndb.StringProperty()
  forename = ndb.StringProperty()
  surname  = ndb.StringProperty()
  created  = ndb.DateTimeProperty(auto_now_add=True)
  updated  = ndb.DateTimeProperty(auto_now=True)


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
class PostMessage(messages.Message):
  title = messages.StringField(1, required=True)
  body = messages.StringField(2)

class Request(messages.Message):
  userID = messages.StringField(1, required=True)
  token = messages.StringField(2, required=True)



@endpoints.api(name='wc', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
               audiences=[WEB_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID])
class WCApi(remote.Service):

  def checkAuthentication(self, request):
    if ((json.load(urllib2.urlopen('https://graph.facebook.com/me?fields=id&access_token=' + request.token))['id']) != request.userID):
      raise endpoints.UnauthorizedException('Invalid user_id or access_token')


  @endpoints.method(Request, PostMessage,
                    name='execution.submit', path='execution', http_method='POST',)
  def list_posts(self, request):
    self.checkAuthentication(request)
    return PostMessage(title=request.userID, body="there")
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
""" 
def messages(type, msg):

Set and retrieve messages to show to user, maintained in session storage
If no parameters are defined then will return and reset the messages

@type  type: integer
@param type: constant of the type (debug/info/notice/warn/error/fatal)
@type: msg:  string
@param msg:  message to display to end user
@rtype:      array
@return:     de-duped array of messages to show to user

  return


"""

# new_account = Account(owner=current_user, id=current_user.user_id(), name='Some Name')
# existing_account = Account.get_by_id(current_user.user_id())




  # title = messages.StringField(1, required=True)
  # body = messages.StringField(2)
