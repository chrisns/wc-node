define([
  'text!views/main.html',
  'angular'
], function(
  templateHTML
) {
  "use strict";

  function router ($routeProvider) {
    $routeProvider
      .when('/', {
        template: templateHTML,
        controller: 'MainCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
    }

  router.inject = ['$routeProvider'];

  return router;

});