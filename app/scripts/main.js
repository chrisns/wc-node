/*jshint unused: vars */
require.config({
  paths: {
    angular: '../../bower_components/angular/angular',
    'angular-cookies': '../../bower_components/angular-cookies/angular-cookies',
    'angular-mocks': '../../bower_components/angular-mocks/angular-mocks',
    'angular-resource': '../../bower_components/angular-resource/angular-resource',
    'ui-router': '../../bower_components/angular-ui-router/release/angular-ui-router',
    'angular-sanitize': '../../bower_components/angular-sanitize/angular-sanitize',
    'angular-scenario': '../../bower_components/angular-scenario/angular-scenario',
    affix: '../../bower_components/bootstrap-sass-official/assets/javascripts/bootstrap/affix',
    alert: '../../bower_components/bootstrap-sass-official/assets/javascripts/bootstrap/alert',
    button: '../../bower_components/bootstrap-sass-official/assets/javascripts/bootstrap/button',
    carousel: '../../bower_components/bootstrap-sass-official/assets/javascripts/bootstrap/carousel',
    collapse: '../../bower_components/bootstrap-sass-official/assets/javascripts/bootstrap/collapse',
    dropdown: '../../bower_components/bootstrap-sass-official/assets/javascripts/bootstrap/dropdown',
    tab: '../../bower_components/bootstrap-sass-official/assets/javascripts/bootstrap/tab',
    transition: '../../bower_components/bootstrap-sass-official/assets/javascripts/bootstrap/transition',
    scrollspy: '../../bower_components/bootstrap-sass-official/assets/javascripts/bootstrap/scrollspy',
    modal: '../../bower_components/bootstrap-sass-official/assets/javascripts/bootstrap/modal',
    tooltip: '../../bower_components/bootstrap-sass-official/assets/javascripts/bootstrap/tooltip',
    popover: '../../bower_components/bootstrap-sass-official/assets/javascripts/bootstrap/popover',
    'angular-facebook': '../../bower_components/angular-facebook/lib/angular-facebook',
    'json-editor': '../../bower_components/json-editor/dist/jsoneditor',
    async: '../../bower_components/requirejs-plugins/src/async',
    depend: '../../bower_components/requirejs-plugins/src/depend',
    font: '../../bower_components/requirejs-plugins/src/font',
    goog: '../../bower_components/requirejs-plugins/src/goog',
    image: '../../bower_components/requirejs-plugins/src/image',
    json: '../../bower_components/requirejs-plugins/src/json',
    mdown: '../../bower_components/requirejs-plugins/src/mdown',
    noext: '../../bower_components/requirejs-plugins/src/noext',
    propertyParser: '../../bower_components/requirejs-plugins/src/propertyParser',
    'Markdown.Converter': '../../bower_components/requirejs-plugins/lib/Markdown.Converter',
    text: '../../bower_components/requirejs-plugins/lib/text',
    'sass-bootstrap': '../../bower_components/sass-bootstrap/dist/js/bootstrap',
    facebook: '../../bower_components/angular-facebook/lib/angular-facebook',
    jQuery: '../../bower_components/jquery/dist/jquery',
    'angular-route': '../../bower_components/angular-route/angular-route',
    'angular-ui-router': '../../bower_components/angular-ui-router/release/angular-ui-router',
    jquery: '../../bower_components/jquery/dist/jquery',
    'angular-form-builder': '../../bower_components/angular-form-builder/dist/angular-form-builder',
    'angular-form-builder-components': '../../bower_components/angular-form-builder/dist/angular-form-builder-components',
    'angular-validator': '../../bower_components/angular-validator/dist/angular-validator',
    angulartics: '../../bower_components/angulartics/src/angulartics',
    'angulartics.google.analytics': '../../bower_components/angulartics/src/angulartics-ga',
    'angulartics-adobe': '../../bower_components/angulartics/src/angulartics-adobe',
    'angulartics-chartbeat': '../../bower_components/angulartics/src/angulartics-chartbeat',
    'angulartics-flurry': '../../bower_components/angulartics/src/angulartics-flurry',
    'angulartics-ga-cordova': '../../bower_components/angulartics/src/angulartics-ga-cordova',
    'angulartics-ga': '../../bower_components/angulartics/src/angulartics-ga',
    'angulartics-gtm': '../../bower_components/angulartics/src/angulartics-gtm',
    'angulartics-kissmetrics': '../../bower_components/angulartics/src/angulartics-kissmetrics',
    'angulartics-mixpanel': '../../bower_components/angulartics/src/angulartics-mixpanel',
    'angulartics-piwik': '../../bower_components/angulartics/src/angulartics-piwik',
    'angulartics-scroll': '../../bower_components/angulartics/src/angulartics-scroll',
    'angulartics-segmentio': '../../bower_components/angulartics/src/angulartics-segmentio',
    'angulartics-splunk': '../../bower_components/angulartics/src/angulartics-splunk',
    'angulartics-woopra': '../../bower_components/angulartics/src/angulartics-woopra'
  },
  shim: {
    angular: {
      exports: 'angular'
    },
    angulartics: [
      'angular'
    ],
    'angulartics.google.analytics': [
      'angulartics',
      'angular'
    ],
    'ui-router': [
      'angular'
    ],
    'angular-cookies': [
      'angular'
    ],
    'angular-sanitize': [
      'angular'
    ],
    'angular-resource': [
      'angular'
    ],
    'angular-mocks': {
      deps: [
        'angular'
      ],
      exports: 'angular.mock'
    },
    'sass-bootstrap': [
      'jQuery'
    ],
    app: {
      deps: [
        'sass-bootstrap'
      ]
    },
    facebook: {
      deps: [
        'angular'
      ],
      exports: 'fb'
    }
  },
  priority: [
    'angular'
  ],
  packages: [

  ]
});

//http://code.angularjs.org/1.2.1/docs/guide/bootstrap#overview_deferred-bootstrap
window.name = 'NG_DEFER_BOOTSTRAP!';

//noinspection OverlyComplexFunctionJS
require([
  'angular',
  'app',
  'ui-router',
  'angular-cookies',
  'angular-sanitize',
  'angular-resource',
  'facebook',
  'json-editor',
  'angulartics',
  'angulartics.google.analytics'
], function(angular, app, uiRouter, ngCookies, ngSanitize, ngResource, Facebook) {
  'use strict';
  /* jshint ignore:start */
  var $html = angular.element(document.getElementsByTagName('html')[0]);
  /* jshint ignore:end */
  angular.element().ready(function() {
    angular.resumeBootstrap([app.name]);
  });
});
