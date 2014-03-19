requirejs.config({
  baseUrl: './',
  paths: {
    'jquery': 'bower_components/jquery/jquery',
    'bootstrap': 'bower_components/sass-bootstrap/dist/js/bootstrap',
    'angular': 'bower_components/angular/angular',
    'angular-resource':'bower_components/angular-resource/angular-resource',
    'angular-cookies':'bower_components/angular-cookies/angular-cookies',
    'angular-sanitize':'bower_components/angular-sanitize/angular-sanitize',
    'angular-route':'bower_components/angular-route/angular-route',
    'text': 'bower_components/requirejs-plugins/lib/text',
    'angular-form-builder': 'bower_components/angular-form-builder/dist/angular-form-builder',
    'angular-form-builder-components': 'bower_components/angular-form-builder/dist/angular-form-builder-components',
    'angular-validator': 'bower_components/angular-validator/dist/angular-validator',
    'angular-validator-rules': 'bower_components/angular-validator/dist/angular-validator-rules',
    'gae-client': '//apis.google.com/js/client.js',
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
      deps: ['angular-form-builder']
    },
    'angular-validator-rules' : {
      deps: ['angular-validator']
    },
    'angular-form-builder-components' : {
      deps: ['angular-form-builder']
    },
    'angular-form-builder' : {
      deps: [
        'angular',
        'jquery',
        'angular-validator'
      ]
    }
  }
});

require([
  'scripts/app',
  'jquery',
  'bootstrap',
  'angular',
  'angular-resource',
  'angular-route',
  'angular-sanitize',
  'angular-cookies'
], function(
  app) {
  'use strict';
  console.log(app, 'i have loaded okay');

  angular.bootstrap(document, ['wcApp']);


});
