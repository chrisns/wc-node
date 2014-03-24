define(['angular'], function () {
  'use strict';

  return function MainCtrl($scope, $ngRoute, $builder, $validator) {
    console.log('MainCtrl had loaded');
    console.log($scope);
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
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