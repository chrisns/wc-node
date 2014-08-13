/* globals angular */
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
    .controller('ListExecutionsCtrl', function ($scope, $http) {
      $http({method: 'GET', url: '/api/executions'}).
        success(function(data, status, headers, config) {
          $scope.executions = data.collection.items;
        });
    });
});
