/*jshint unused: vars */
define(['angular', 'facebook'], function (angular) {
  'use strict';
  describe('Controller: FacebookCtrl', function () {

    // load the controller's module
    beforeEach(module('wcApp.controllers.FacebookCtrl'));
    beforeEach(module('facebook'));

    var FacebookCtrl,
      mockFb,
      fbready,
      fbloginstatus,
      scope;

    // Initialize the controller and a mock scope
    beforeEach(inject(function ($controller, Facebook, $rootScope) {
      scope = $rootScope.$new();
      mockFb = Facebook;
      FacebookCtrl = $controller('FacebookCtrl', {
        $scope: scope,
        Facebook: mockFb
      });
    }));

    it('should initially say facebook is not ready', function () {
      // Arrange
      spyOn(mockFb, 'isReady').andReturn(false);
      // Act
      scope.$apply();
      // Assert
      expect(scope.facebookReady()).toBe(false);
    });


    it('should start with an empty user', function () {
      // Assert
     expect(scope.user).toEqual({});
    });

    it('should delegate login to Facebook', function () {
      // Assert
      expect(scope.login).toBe(mockFb.login);
    });

    it('should delegate logout to Facebook', function () {
      // Assert
      expect(scope.logout).toBe(mockFb.logout);
    });

    it('should delegate facebookReady to Facebook', function () {
      // Assert
      expect(scope.facebookReady).toBe(mockFb.isReady);
    });


    it('should update $user if response changes to connected', function(){
      // Arrange
      var expectedUser = {
        id: "12354",
        first_name: "John",
        last_name: "Smith",
        name: "John Smith",
      };
      spyOn(mockFb, 'api').andCallFake(function(param, callback) {
        return callback(expectedUser);
      });

      // Act
      scope.$broadcast('Facebook:authResponseChange', {status: 'connected'});
      scope.$apply();
      expect(scope.user).toEqual(expectedUser);
      expect(mockFb.api).toHaveBeenCalled();
    });

    it('should update $user if response changes to NOT connected', function () {
      // Arrange
      spyOn(mockFb, 'api');

      // Act
      scope.$broadcast('Facebook:authResponseChange', {status: 'notconnected'});
      scope.$apply();

      // Assert
      expect(scope.user).toEqual({});
      expect(mockFb.api).not.toHaveBeenCalled();
    });

  });
});
