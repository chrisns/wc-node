/*jshint unused: vars */
define(['angular', 'angular-mocks', 'app'], function(angular, mocks, app) {
  'use strict';

  describe('Service: wcapi', function () {

    // load the service's module
    beforeEach(module('wcApp.services.Wcapi'));

    // instantiate service
    var wcapi;
    beforeEach(inject(function (_wcapi_) {
      wcapi = _wcapi_;
    }));

    it('should do something', function () {
      expect(!!wcapi).toBe(true);
    });

  });
});
