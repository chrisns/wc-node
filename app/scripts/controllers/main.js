/* globals angular */
define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc function
   * @name wcApp.controller:MainCtrl
   * @description
   * # MainCtrl
   * Controller of the wcApp
   */
  angular.module('wcApp.controllers.MainCtrl', [])
    .controller('MainCtrl', function ($scope) {
      $scope.awesomeThings = [
        'HTML5 Boilerplate',
        'AngularJS',
        'Karma'
      ];
    });
});
