/* globals angular */
define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc service
   * @name wcApp.wcapi
   * @description
   * # wcapi
   * Provider in the wcApp.
   */
  angular.module('wcApp.services.Wcapi', [])
    .provider('wcapi', function () {

      // Private variables
      var salutation = 'Hello';

      // Private constructor
      function Greeter() {
        this.greet = function () {
          return salutation;
        };
      }

      // Public API for configuration
      this.setSalutation = function (s) {
        //noinspection ReuseOfLocalVariableJS
        salutation = s;
      };

      // Method for instantiating
      this.$get = function () {
        return new Greeter();
      };
    });
});
