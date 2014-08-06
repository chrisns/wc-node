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
      var response = {
        collection: {
          items: [
            {
              href: '/api/executions/agx0ZXN0YmVkLXRlc3RyDwsSCUV4ZWN1dGlvbhgBDA',
              type: 'Execution',
              execution_id: 'agx0ZXN0YmVkLXRlc3RyDwsSCUV4ZWN1dGlvbhgBDA',
              created: '2014-08-06T16:31:48.377143+00:00'
            }, {
              href: '/api/executions/agx0ZXN0YmVkLXRlc3RyDwsSCUV4ZWN1dGlvbhgCDA',
              type: 'Execution',
              execution_id: 'agx0ZXN0YmVkLXRlc3RyDwsSCUV4ZWN1dGlvbhgCDA',
              created: '2014-08-06T16:31:48.381122+00:00'
            }, {
              href: '/api/executions/agx0ZXN0YmVkLXRlc3RyDwsSCUV4ZWN1dGlvbhgDDA',
              type: 'Execution',
              execution_id: 'agx0ZXN0YmVkLXRlc3RyDwsSCUV4ZWN1dGlvbhgDDA',
              created: '2014-08-06T16:31:48.384638+00:00'
            }
          ],
          href: '/api/executions',
          _links: {
            create: {
              href: '/api/executions/create'
            }
          },
          version: 1.0
        }
      };

      $scope.executions = response.collection.items;
//      $http({method: 'GET', url: '/api/executions'}).
//        success(function(data, status, headers, config) {
//          $scope.executions = data.collection.items;
//        });
    });
});
