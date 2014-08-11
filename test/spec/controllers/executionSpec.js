/*jshint unused: vars */
define(['angular', 'angular-mocks', 'app'], function(angular, mocks, app) {
  'use strict';

  describe('Controller: ExecutionCtrl', function () {

    // load the controller's module
    beforeEach(module('wcApp.controllers.ExecutionCtrl'));

    var ExecutionCtrl,
      scope;

    // Initialize the controller and a mock scope
    beforeEach(inject(function ($controller, $rootScope) {
      scope = $rootScope.$new();
      ExecutionCtrl = $controller('ExecutionCtrl', {
        $scope: scope
      });
    }));


  });
});
