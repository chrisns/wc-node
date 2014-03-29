requirejs.config({
  paths: {
    'jquery': '/bower_components/jquery/jquery',
    'bootstrap': '/bower_components/sass-bootstrap/dist/js/bootstrap',
    'angular': '/bower_components/angular/angular',
    'angular-resource':'/bower_components/angular-resource/angular-resource',
    'angular-cookies':'/bower_components/angular-cookies/angular-cookies',
    'angular-sanitize':'/bower_components/angular-sanitize/angular-sanitize',
    'angular-route':'/bower_components/angular-route/angular-route',
    'text': '/bower_components/requirejs-plugins/lib/text',
    'angular-form-builder': '/bower_components/angular-form-builder/dist/angular-form-builder',
    'angular-form-builder-components': '/bower_components/angular-form-builder/dist/angular-form-builder-components',
    'angular-validator': '/bower_components/angular-validator/dist/angular-validator',
    'angular-validator-rules': '/bower_components/angular-validator/dist/angular-validator-rules',
    'appengine':'https://apis.google.com/js/client.js?onload=javascript:void(0)',
    'gapi': 'gapi',
    'app': 'app',
    // 'fb': '//connect.facebook.net/en_US/all',
    'facebook': '/bower_components/angular-facebook/lib/angular-facebook',
    // 'gapi-config': 'config/gapi-config',
  },
  shim: {
    'bootstrap' : {
      deps: ['jquery']
    },
    'angular': {
      deps: ['jquery'],
      exports: 'angular'
    },
    'angular-resource': ['angular'],
    'angular-route': ['angular'],
    'angular-cookies': ['angular'],
    'angular-sanitize': ['angular'],
    'angular-validator' : {
      deps: [
        'angular',
        'angular-validator-rules'
      ]
    },
    'facebook' : {
      deps: ['angular'],
      exports: 'fb'
    },
    'gapi' : {
      exports: 'gapi'
    },
    'app' : ['angular', 'appengine', 'angular-resource', 'angular-route', 'bootstrap'],
    'angular-validator-rules' : ['angular'],
    'angular-form-builder-components' : ['angular'],
    'angular-form-builder' : {
      deps: [
        'angular-validator',
        'angular-form-builder-components',
        'angular',
        'jquery',
      ]
    }
  },
  deps : ['gapi'],
});

require([
  'app',
  'jquery',
  'angular-cookies',
  'bootstrap',
  'angular',
  'angular-resource',
  'angular-route',
  'angular-sanitize',
  'angular-form-builder',
  'angular-validator',
  'gapi',
  // 'fb',
  'facebook'
], function(
  ) {
  'use strict';

  // FB.init({
    // appId : '665447500158300',
  // });
  // angular.bootstrap(document, ['wcApp']);
});
