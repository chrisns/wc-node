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
    .controller('ExecutionCtrl', function ($scope, $stateParams, $http) {
      $scope.execution_id = $stateParams.execution_id;
      $http({method: 'GET', url: '/api/executions/' + $scope.execution_id }).
        success(function (data, status, headers, config) {
          $scope.execution_schema= data.execution.schema;
          $scope.execution_schema.format = 'grid';
        });
      $scope.$watch(
        'execution_schema',
        function(newval, oldval) {
          var editor = new JSONEditor(document.getElementById('editor_holder'), {
            theme: 'bootstrap3',
            disable_edit_json: true,
            disable_collapse: true,
            disable_properties: true,
            form_name_root: 'form',
            show_errors: 'alawys',
            iconlib: 'bootstrap3',
            ajax: false,
            schema: newval
          });
        }
      );

//      var editor = new JSONEditor(document.getElementById('editor_holder'), {
//        // Enable fetching schemas via ajax
//        ajax: true,
//
//        // The schema for the editor
//        schema: {
//          $ref: '/api/executions/' + $stateParams.execution_id,
//          format: "grid"
//        },
//
//        // Seed the form with a starting value
////        startval: starting_value
//      });

      // Hook up the submit button to log to the console
//      document.getElementById('submit').addEventListener('click', function () {
//        // Get the value from the editor
//        console.log(editor.getValue());
//      });
      $scope.awesomeThings = [
        $stateParams.execution_id
      ];
    });
});
