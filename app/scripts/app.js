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
    'facebook',
    'builder',
    'builder.components',
    'validator'
  ])
  .controller('MainCtrl', MainCtrl)
  .config(Router)
  .config(['FacebookProvider', function(FacebookProvider) {
     FacebookProvider.init('665447500158300');
  }]);

  return module;

});