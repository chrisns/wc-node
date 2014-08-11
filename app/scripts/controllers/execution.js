define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc function
   * @name wcApp.controller:ExecutionCtrl
   * @description
   * # ExecutionCtrl
   * Controller of the wcApp
   */
  angular.module('wcApp.controllers.ExecutionCtrl', ['ui.router'])
    .controller('ExecutionCtrl', function ($scope, $stateParams) {

      $scope.awesomeThings = [
        $stateParams.execution_id
      ];
    });
});
