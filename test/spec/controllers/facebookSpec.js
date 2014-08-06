/*jshint unused: vars */
define(['angular', 'angular-mocks', 'app', 'facebook'], function(angular, mocks, app, Facebook) {
  'use strict';

  describe('Controller: FacebookCtrl', function () {

    // load the controller's module
    beforeEach(module('wcApp.controllers.FacebookCtrl'));

    var FacebookCtrl,
      scope;

    // Initialize the controller and a mock scope
    beforeEach(inject(function ($controller, $rootScope) {
      scope = $rootScope.$new();
      FacebookCtrl = $controller('FacebookCtrl', {
        $scope: scope
      });
    }));
    console.error(Facebook);
    it('should attach a list of awesomeThings to the scope', function () {
      expect(scope.awesomeThings.length).toBe(3);
    });
  });
});
