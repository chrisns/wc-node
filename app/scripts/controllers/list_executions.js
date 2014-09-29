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
      $http({method: 'GET', url: '/api/executions?fields=company'})
        .success(function (data) {
          $scope.executions = data.collection.items;
        });

      $scope.delete = function(execution) {
        $http({method: 'delete', url: execution.href})
          .success(function (data) {
            $scope.executions.splice($scope.executions.indexOf(execution), 1);
          });
      };
    });
});
