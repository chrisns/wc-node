define(['angular'], function () {
  'use strict';

  return function MainCtrl($scope, $builder, $validator) {
    var formjson = [
      {
        component: 'textInput',
        label: 'Name',
        placeholder: 'Your name',
        description: '',
      },
      {
        component: 'textInput',
        label: 'Face',
        placeholder: 'Your face',
        description: 'faces',
        required: true,
      },
      {
        component: 'radio',
        label: 'Nose',
        description: 'How many noses do you have?',
        options: ['1', '2']
      },
      {
        component: 'checkbox',
        label: 'Pets',
        description: 'Do you have any pets?',
        options: ['Dog', 'Cat']
      }
    ];

    formjson.forEach(function(formElement) {
      $builder.addFormObject('capture', formElement);
    });

    $scope.removeFormEntry = function(entry) {
      $builder.removeFormObject('capture', entry.index);
    };
      // console.log(gapiConfig);
    $scope.signin = function() {
      FB.login(null, {scope: 'email'});
      // gapi.auth.authorize({client_id: 'aa', scope: 'ff', immediate: false});
    };
    FB.Event.subscribe('auth.statusChange', function() {
      FB.getLoginStatus(function(response) {
        $scope.authenticated = response.status;
      });
    });
    $scope.authenticated = FB.getLoginStatus();

    $scope.submit = function() {
      return $validator.validate($scope, 'capture').success(function() {

        // @TODO:submit it 

        // on success of submit empty the form and get the next one
        for (var i = ($builder.forms.capture.length - 1); i >= 0; i--) {
          $builder.removeFormObject('capture', $builder.forms.capture[i].index);
        }
        return true;
      }).error(function() {
        // display validation errors
        return false;
      });
    };
  };
});