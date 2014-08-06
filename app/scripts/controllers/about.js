/* globals define */
define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc function
   * @name wcApp.controller:AboutCtrl
   * @description
   * # AboutCtrl
   * Controller of the wcApp
   */
  angular.module('wcApp.controllers.AboutCtrl', [])
    .controller('AboutCtrl', function ($scope) {
      $scope.awesomeThings = [
        'HTML5 Boilerplate',
        'AngularJS',
        'Karma'
      ];
    });
});
