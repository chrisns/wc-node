(function () {
  'use strict';

  angular.module('app', ['builder', 'builder.components', 'validator.rules', 'jackrabbitsgroup.angular-google-auth']).controller('WcController', function($scope, $builder, $validator, jrgGoogleAuth) {


    var googleClientId = '84086224013-u450n6r4dkgr51v3pom39cqgsefrnm83.apps.googleusercontent.com';
    jrgGoogleAuth.init({'client_id':googleClientId, 'scopeHelp':['login', 'email',]});

    //do actual login
    var evtGoogleLogin = "evtGoogleLogin";
    $scope.googleLogin = function() {
      jrgGoogleAuth.login({'extraInfo':{'emails':true}, 'callback':{'evtName':evtGoogleLogin, 'args':[]} });
    };
/*
    $scope.googleInfo;
    @param {Object} googleInfo
      @param {Object} token Fields directly returned from google, with the most important being access_token (but there are others not documented here - see google's documentation for full list)
        @param {String} access_token
      @param {Object} [extraInfo]
        @param {String} [user_id]
        @param {Array} [emails] Object for each email
          @param {String} value The email address itself
          @param {String?} type ?
          @param {Boolean} primary True if this is the user's primary email address
        @param {String} [emailPrimary] User's primary email address (convenience field extracted from emails array, if exists)

*/
    $scope.$on(evtGoogleLogin, function(evt, googleInfo) {
      $scope.googleInfo = googleInfo;
      console.log($scope.googleInfo.extraInfo.emailPrimary);
    });


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
    }


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


  });
}());