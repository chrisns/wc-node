/*jshint unused: vars */
//noinspection OverlyComplexFunctionJS
define([
  'angular',
  'ui-router',
  'controllers/main',
  'controllers/execution',
  'controllers/about',
  'controllers/facebook',
  'controllers/list_executions',
  'services/wcapi'],
  /*deps*/
   function (
     angular,
     MainCtrl,
     AboutCtrl,
     FacebookCtrl,
     ListExecutionsCtrl,
     WcapiProvider
     , ExecutionCtrl)/*invoke*/ {
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
    'wcApp.controllers.ExecutionCtrl',
/*angJSDeps*/
    'ngCookies',
    'ngResource',
    'ngSanitize',
    'ui.router'
  ])
  .config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/');
    $stateProvider.state('index',{
      url: '/',
      templateUrl: 'views/main.html',
      controller:'MainCtrl'
    })
    .state('history',{
      url: '/my-history',
      templateUrl: 'views/list_executions.html',
      controller: 'ListExecutionsCtrl'
    })
    .state('executionview', {
      url: "/my-history/:execution_id",
      templateUrl: 'views/execution.html',
      controller: 'ExecutionCtrl'
    });
  });
});
