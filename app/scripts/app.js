define([
  'scripts/controllers/main',
  'scripts/config/router'
], function (
  MainCtrl,
  Router
) {
  'use strict';

  var module = angular.module('wcApp', [
    'ngCookies',
    'ngResource',
    'ngSanitize',
    'ngRoute',
    'angular-form-builder',
    'angular-validator',
    'angular-validator-rules'
  ])
  .controller('MainCtrl', MainCtrl)
  .config(Router);


  return module;

});