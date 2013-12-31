import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

from google.appengine.ext import ndb


WEB_CLIENT_ID = '84086224013-u450n6r4dkgr51v3pom39cqgsefrnm83.apps.googleusercontent.com'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'


# package = 'wc'


class Greeting(messages.Message):
    """Greeting that stores a message."""
    message = messages.StringField(1)


class GreetingCollection(messages.Message):
    """Collection of Greetings."""
    items = messages.MessageField(Greeting, 1, repeated=True)


STORED_GREETINGS = GreetingCollection(items=[
    Greeting(message='hello world!'),
    Greeting(message='goodbye world!'),
])


@endpoints.api(name='wc', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID],
               audiences=[WEB_CLIENT_ID])

class WCApi(remote.Service):

    MULTIPLY_METHOD_RESOURCE = endpoints.ResourceContainer(
            Greeting,
            times=messages.IntegerField(2, variant=messages.Variant.INT32,
                                        required=True))

    @endpoints.method(MULTIPLY_METHOD_RESOURCE, Greeting,
                      path='hellogreeting/{times}', http_method='POST',
                      name='greetings.multiply')
    def greetings_multiply(self, request):
        return Greeting(message=request.message * request.times)

    @endpoints.method(message_types.VoidMessage, GreetingCollection,
                      path='hellogreeting', http_method='GET',
                      name='greetings.listGreeting')
    def greetings_list(self, unused_request):
        return STORED_GREETINGS

    ID_RESOURCE = endpoints.ResourceContainer(
            message_types.VoidMessage,
            id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, Greeting,
                      path='hellogreeting/{id}', http_method='GET',
                      name='greetings.getGreeting')
    def greeting_get(self, request):
        print Account(id=endpoints.get_current_user().email(), greeting = STORED_GREETINGS.items[request.id].message).put()
        try:
            return STORED_GREETINGS.items[request.id]
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Greeting %s not found.' %
                                              (request.id,))

    @endpoints.method(message_types.VoidMessage, Greeting,
                      path='hellogreeting/authed', http_method='POST',
                      name='greetings.authed')
    def greeting_authed(self, request):
        current_user = endpoints.get_current_user()
        email = (current_user.email() if current_user is not None
                 else 'Anonymous')
        # print "hihi"
        # print get_current_user().user_id()
        # print 
        # key = ndb.Key("user", email)
        # print UserEntity.query_book(ancestor_key=key).fetch(20)
        # return Greeting(message=UserEntity.query_book(ancestor_key=key).fetch(1))
        # Account(email=endpoints.get_current_user().email(), greeting = STORED_GREETINGS.items[request.id].message).put()
        # print Account(id=).get()
        # print key('Account', endpoints.get_current_user().email()).get()
        account = Account.get_by_id(id=endpoints.get_current_user().email()).greeting
        # print account.greeting
        return Greeting(message='hello %s %s' % (email, account,))


APPLICATION = endpoints.api_server([WCApi])


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

class Account(ndb.Model):
  greeting = ndb.StringProperty() 
  # email = ndb.StringProperty()