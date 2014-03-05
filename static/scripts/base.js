(function () {
  'use strict';

  angular.module('app', ['builder', 'builder.components', 'validator.rules', 'jackrabbitsgroup.angular-google-auth']).controller('WcController', function($scope, $builder, $validator, jrgGoogleAuth) {


    var googleClientId = '84086224013-u450n6r4dkgr51v3pom39cqgsefrnm83.apps.googleusercontent.com';
    jrgGoogleAuth.init({'client_id':googleClientId, 'scopeHelp':['login', 'email', 'contacts']});

    //do actual login
    var evtGoogleLogin ="evtGoogleLogin";
    $scope.googleLogin =function() {
      jrgGoogleAuth.login({'extraInfo':{'user_id':true, 'emails':true}, 'callback':{'evtName':evtGoogleLogin, 'args':[]} });
    };

    $scope.googleInfo;
    // @param {Object} googleInfo
      // @param {Object} token Fields directly returned from google, with the most important being access_token (but there are others not documented here - see google's documentation for full list)
        // @param {String} access_token
      // @param {Object} [extraInfo]
        // @param {String} [user_id]
        // @param {Array} [emails] Object for each email
          // @param {String} value The email address itself
          // @param {String?} type ?
          // @param {Boolean} primary True if this is the user's primary email address
        // @param {String} [emailPrimary] User's primary email address (convenience field extracted from emails array, if exists)

      $scope.$on(evtGoogleLogin, function(evt, googleInfo) {
        $scope.googleInfo = googleInfo;
        console.log($scope.googleInfo.extraInfo.emailPrimary);
      });

      var checkbox, textbox;
      textbox = $builder.addFormObject('capture', {
        component: 'textInput',
        label: 'Name',
        placeholder: 'Your name',
        // required: true,
      });
      checkbox = $builder.addFormObject('capture', {
        component: 'checkbox',
        label: 'Pets',
        description: 'Do you have any pets?',
        options: ['Dog', 'Cat']
      });
      // $scope.form = $builder.forms.capture;
      return $scope.submit = function() {
        return $validator.validate($scope, 'capture').success(function() {
          // empty the form out
          $builder.forms.capture.forEach(function(entry){

            console.log(entry);
            $builder.removeFormObject('capture');
          });
          // submit it 
          return console.log('succesa');
        }).error(function() {
          // display errors
          return;
        });
      };


  });
}());