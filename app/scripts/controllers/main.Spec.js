'use strict';

//describe('Controller: MainCtrl', function () {
//
//  // load the controller's module
//  beforeEach(module('wcApp'));
//
//  var MainCtrl,
//    scope;
//
//  // Initialize the controller and a mock scope
//  beforeEach(inject(function ($controller, $rootScope) {
//    scope = $rootScope.$new();
//    MainCtrl = $controller('MainCtrl', {
//      $scope: scope
//    });
//  }));
//
//  it('should attach a list of awesomeThings to the scope', function () {
//    expect(scope.awesomeThings.length).toBe(3);
//  });
//});

define(['app'], function(App, $, _) {

    describe('just checking', function() {
//beforeEach(module('/templates/foo.html'));
        it('works for app', function() {
            var el = $('<div></div>');

            var app = new App(el);
            app.render();

            expect(el.text()).toEqual('require.js up and running');
        });

    });

});