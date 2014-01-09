/** wc global namespace for wc projects. */
var wc = wc || {};

/**
 * Client ID of the application (from the APIs Console).
 * @type {string}
 */
wc.CLIENT_ID =
    '84086224013-u450n6r4dkgr51v3pom39cqgsefrnm83.apps.googleusercontent.com';

/**
 * Scopes used by the application.
 * @type {string}
 */
wc.SCOPES =
    'https://www.googleapis.com/auth/userinfo.email';

/**
 * Whether or not the user is signed in.
 * @type {boolean}
 */
wc.signedIn = false;

/**
 * Loads the application UI after the user has completed auth.
 */
wc.userAuthed = function() {
  var request = gapi.client.oauth2.userinfo.get().execute(function(resp) {
    if (!resp.code) {
      wc.signedIn = true;
      document.getElementById('signinButton').innerHTML = 'Sign out';
      document.getElementById('authedGreeting').disabled = false;
    }
  });
};

/**
 * Handles the auth flow, with the given value for immediate mode.
 * @param {boolean} mode Whether or not to use immediate mode.
 * @param {Function} callback Callback to call on completion.
 */
wc.signin = function(mode, callback) {
  gapi.auth.authorize({client_id: wc.CLIENT_ID,
      scope: wc.SCOPES, immediate: mode},
      callback);
};

/**
 * Presents the user with the authorization popup.
 */
wc.auth = function() {
  if (!wc.signedIn) {
    wc.signin(false,
        wc.userAuthed);
  } else {
    wc.signedIn = false;
    document.getElementById('signinButton').innerHTML = 'Sign in';
    document.getElementById('authedGreeting').disabled = true;
  }
};

/**
 * Prints a greeting to the greeting log.
 * param {Object} greeting Greeting to print.
 */
wc.print = function(greeting) {
  var element = document.createElement('div');
  element.classList.add('row');
  element.innerHTML = greeting.message;
  document.getElementById('outputLog').appendChild(element);
};

/**
 * Gets a numbered greeting via the API.
 * @param {string} id ID of the greeting.
 */
wc.getGreeting = function(id) {
  gapi.client.wc.greetings.getGreeting({'id': id}).execute(
      function(resp) {
        if (!resp.code) {
          wc.print(resp);
        }
      });
};

/**
 * Lists greetings via the API.
 */
wc.listGreeting = function() {
  gapi.client.wc.greetings.listGreeting().execute(
      function(resp) {
        if (!resp.code) {
          resp.items = resp.items || [];
          for (var i = 0; i < resp.items.length; i++) {
            wc.print(resp.items[i]);
          }
        }
      });
};

/**
 * Greets the current user via the API.
 */
wc.authedGreeting = function(id) {
  gapi.client.wc.greetings.authed().execute(
      function(resp) {
        wc.print(resp);
      });
};

/**
 * Enables the button callbacks in the UI.
 */
wc.enableButtons = function() {
  document.getElementById('getGreeting').onclick = function() {
    wc.getGreeting(
        document.getElementById('id').value);
  };

  document.getElementById('listGreeting').onclick = function() {
    wc.listGreeting();
  };

  document.getElementById('authedGreeting').onclick = function() {
    wc.authedGreeting();
  };
  
  document.getElementById('signinButton').onclick = function() {
    wc.auth();
  };
};
 
/**
 * Initializes the application.
 * @param {string} apiRoot Root of the API's path.
 */
wc.init = function(apiRoot) {
  apiRoot = '//' + window.location.host + '/_ah/api';
  // Loads the OAuth and wc APIs asynchronously, and triggers login
  // when they have completed.
  var apisToLoad;
  var callback = function() {
    if (--apisToLoad === 0) {
      wc.enableButtons();
      wc.signin(true,
          wc.userAuthed);
    }
  };

  apisToLoad = 2; // must match number of calls to gapi.client.load()
  gapi.client.load('wc', 'v1', callback, apiRoot);
  gapi.client.load('oauth2', 'v2', callback);
};

function wcinit() {
  wc.init();
}


App = Ember.Application.create();

App.Router.map(function() {
  // put your routes here
});

App.IndexRoute = Ember.Route.extend({
  model: function() {
    return ['red', 'yellow', 'blue'];
  }
});
