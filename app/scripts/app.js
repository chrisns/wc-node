define([
  'controllers/main',
  'config/router',
  // 'config/gapi-config'
], function (
  MainCtrl,
  Router
) {
  'use strict';

  var module = angular.module('wcApp', [
    'ngRoute',
    'builder',
    'builder.components',
    'validator',
  ])
  .controller('MainCtrl', MainCtrl)
  .config(Router);

  return module;

});