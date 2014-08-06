/*jshint unused: vars */
//noinspection OverlyComplexFunctionJS
define(['angular', 'controllers/main', 'controllers/about', 'controllers/facebook', 'controllers/list_executions', 'services/wcapi']/*deps*/, function (angular, MainCtrl, AboutCtrl, FacebookCtrl, ListExecutionsCtrl, WcapiProvider)/*invoke*/ {
  'use strict';

  /**
   * @ngdoc overview
   * @name wcApp
   * @description
   * # wcApp
   *
   * Main module of the application.
   */
  return angular
    .module('wcApp', ['wcApp.controllers.MainCtrl',
'wcApp.controllers.AboutCtrl',
'wcApp.controllers.FacebookCtrl',
'wcApp.controllers.ListExecutionsCtrl',
'wcApp.services.Wcapi',
/*angJSDeps*/
    'ngCookies',
    'ngResource',
    'ngSanitize',
    'ngRoute'
  ])
    .config(function ($routeProvider) {
      $routeProvider
        .when('/', {
          templateUrl: 'views/main.html',
          controller: 'MainCtrl'
        })
        .when('/about', {
          templateUrl: 'views/about.html',
          controller: 'AboutCtrl'
        })
        .when('/my-history', {
          templateUrl: 'views/list_executions.html',
          controller: 'ListExecutionsCtrl'
        })
        .otherwise({
          redirectTo: '/'
        });
    });
});
