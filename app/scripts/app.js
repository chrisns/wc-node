define([
  'scripts/controllers/main',
  'scripts/config/router',
  'gapi'
], function (
  MainCtrl,
  Router,
  ApiManager
) {
  'use strict';

  var module = angular.module('wcApp', [
    'ngRoute',
    'builder',
    'builder.components',
    'validator',
    'gapi'
  ])
  .controller('MainCtrl', MainCtrl)
  .config(Router);


  return module;

});