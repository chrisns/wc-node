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
    'async': 'bower_components/requirejs-plugins/src/async',
    'gapi': 'scripts/gapi',
    'gapi-config': 'scripts/config/gapi-config',
    'propertyParser': 'bower_components/requirejs-plugins/src/propertyParser',
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
    'gae-client': ['angular'],
    'angular-validator' : {
      deps: [
        'angular',
        'angular-validator-rules'
      ]
    },
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
  }
});

require([
  'scripts/app',
  'jquery',
  'angular-cookies',
  'bootstrap',
  'angular',
  'angular-resource',
  'angular-route',
  'angular-sanitize',
  'angular-form-builder',
  'angular-validator',
  'gapi'
], function(
  app) {
  'use strict';
  // console.log(app, 'i have loaded okay');

  angular.bootstrap(document, ['wcApp']);


});
