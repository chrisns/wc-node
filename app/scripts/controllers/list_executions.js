define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc function
   * @name wcApp.controller:ListExecutionsCtrl
   * @description
   * # ListExecutionsCtrl
   * Controller of the wcApp
   */
  angular.module('wcApp.controllers.ListExecutionsCtrl', [])
    .controller('ListExecutionsCtrl', function ($scope) {
      $scope.awesomeThings = [
        'HTML5 Boilerplate',
        'AngularJS',
        'Karma'
      ];
    });
});
