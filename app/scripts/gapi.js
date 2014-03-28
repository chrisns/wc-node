define([
  'app'
], function() {
  'use strict';


  var apiRoot = '//' + window.location.host + '/_ah/api';
  gapi.client.load('wc', 'v1', function () {

    angular.bootstrap(document, ['wcApp']);
    // console.log('app loaded?', arguments );
  }, apiRoot);





   // jQuery("select[name='frequency_period']").selectpicker({style: 'btn-primary', menuStyle: 'dropdown-inverse'});
});



