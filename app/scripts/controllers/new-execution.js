define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc function
   * @name wcApp.controller:ExecutionCtrl
   * @description
   * # ExecutionCtrl
   * Controller of the wcApp
   */
  angular.module('wcApp.controllers.NewExecutionCtrl', ['ui.router'])
    .controller('NewExecutionCtrl', function ($scope, $stateParams, $http, $state) {
      $http({method: 'POST', url: '/api/executions/create'}).
        success(function (data, status, headers, config) {
          $state.transitionTo('executionview', {execution_id:data.execution.execution_id});
        });
    });
});
