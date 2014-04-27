define([
  'controllers/main',
  // 'services/login-service',
  'config/router',
  // 'config/gapi-config'
], function (
  MainCtrl,
  LoginService,
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
  // .service('loginService', LoginService)
  .controller('MainCtrl', MainCtrl)
  .config(Router)
  .config(['FacebookProvider', function(FacebookProvider) {
     FacebookProvider.init('665447500158300');
  }]);

  return module;

});