/* global define */
define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc function
   * @name wcApp.controller:FacebookCtrl
   * @description
   * # FacebookCtrl
   * Controller of the wcApp
   */
  angular.module('wcApp.controllers.FacebookCtrl', ['facebook'])
//    .service('Facebook', facebook)
    .config(['FacebookProvider', function (FacebookProvider) {
      FacebookProvider.init('665447500158300');
    }])
    .controller('FacebookCtrl', function ($rootScope, $scope, Facebook) {
      // Define user empty data :/
      $rootScope.user = {};
      $scope.facebookReady = Facebook.isReady;

      /**
       * Watch for Facebook to be ready.
       * There's also the event that could be used
       */
      $scope.$on('Facebook:authResponseChange', function(event, response) {
        if ('connected' === response.status) {
          Facebook.api('/me', function (response) {
            $rootScope.user = response;
          });
        }
        else {
          $rootScope.user = {};
        }
      });

      /**
       * Login
       */
      $scope.login = Facebook.login;

      /**
       * Logout
       */
      $scope.logout = Facebook.logout;
    });
});
