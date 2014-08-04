

//define(['controllers/main', 'angular', 'angular-form-builder'], function () {
//    'use strict';
//
//    describe('Controller: MainCtrl', function ($controller, $angular, $builder)) {

//        $controller().MainCtrl();

      // load the controller's module
//      beforeEach(angular.module('wcApp'));
//      beforeEach(angular.module("/views/main.html"));
//      var MainCtrl,
//        scope;

      // Initialize the controller and a mock scope
//      beforeEach(angular.inject(function ($controller, $rootScope) {
//        scope = $rootScope.$new();
//        MainCtrl = $controller('MainCtrl', {
//          $scope: scope
//        });
//      }));

//      it('should attach a list of awesomeThings to the scope', function () {
//        expect(scope.awesomeThings.length).toBe(3);
//      });
//    });
//
//});
define(['angular', 'app', 'jquery', 'facebook', 'angular-form-builder'], function (angular, App, $, facebook, builder) {
//
    describe('just checking', function() {
//        beforeEach(angular.module('wcApp'));
//        beforeEach(module("/views/main"));
//beforeEach(module('/templates/foo.html'));
        it('works for app', function() {
            var el = $('<div></div>');
//            console.log(App);
//            var app = new App();
//            app.render();
            angular.bootstrap(el, ['wcApp'])
            expect(el.text()).toEqual('require.js up and running');
            console.log(el);
        });

    });

});