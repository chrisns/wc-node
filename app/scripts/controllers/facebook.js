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
    .controller('FacebookCtrl', function ($scope, Facebook) {
      // Define user empty data :/
      $scope.user = {};

      /**
       * Watch for Facebook to be ready.
       * There's also the event that could be used
       */
      $scope.$watch(
        function () {
          return Facebook.isReady();
        },
        function (newVal) {
//          if (newVal)
          $scope.facebookReady = true;
          Facebook.getLoginStatus(function (response) {
            if (response.status === 'connected') {
              $scope.me();
              $scope.updateAccessToken();
            }
          });
        }
      );

      /**
       * Login
       */
      $scope.login = function () {
        Facebook.login(function (response) {
          if (response.status === 'connected') {
            $scope.me();
            $scope.updateAccessToken();
          }
        });
      };


      $scope.updateAccessToken = function () {
        Facebook.getLoginStatus(function (response) {
          $scope.$apply(function () {
            $scope.authResponse = response.authResponse;
          });
        });
      };

      /**
       * me
       */
      $scope.me = function () {
        Facebook.api('/me', function (response) {
          $scope.$apply(function () {
            $scope.user = response;
          });
        });
      };

      /**
       * Logout
       */
      $scope.logout = function () {
        Facebook.logout(function () {
          $scope.$apply(function () {
            $scope.user = {};
            $scope.logged = false;
          });
        });
      };
      $scope.awesomeThings = [
        'HTML5 Boilerplate',
        'AngularJS',
        'Karma'
      ];
    });
});
