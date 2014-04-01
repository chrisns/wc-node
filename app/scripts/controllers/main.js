define(['angular'], function () {
  'use strict';

  return function MainCtrl($scope, Facebook, $builder, $validator) {
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
        options: ['1', '4']
      },
      {
        component: 'checkbox',
        label: 'Pets',
        description: 'Do you have any pets?',
        options: ['Dog', 'Hannah']
      }
    ];

    formjson.forEach(function(formElement) {
      $builder.addFormObject('capture', formElement);
    });

    $scope.removeFormEntry = function(entry) {
      $builder.removeFormObject('capture', entry.index);
    };

    // Define user empty data :/
    $scope.user = {};

    /**
     * Watch for Facebook to be ready.
     * There's also the event that could be used
     */
    $scope.$watch(
      function() {
        return Facebook.isReady();
      },
      function(newVal) {
        if (newVal)
          $scope.facebookReady = true;
          Facebook.getLoginStatus(function(response) {
            if (response.status == 'connected') {
              $scope.me();
              $scope.updateAccessToken();
            }
          });
        }
    );

    /**
     * Login
     */
    $scope.login = function() {
      Facebook.login(function(response) {
        if (response.status == 'connected') {
          $scope.me();
          $scope.updateAccessToken();
        }
      });
    };


    $scope.updateAccessToken = function() {
      Facebook.getLoginStatus(function(response) {
        $scope.$apply(function() {
          $scope.authResponse = response.authResponse;
        });
      });
    };
   /**
    * me
    */
    $scope.me = function() {
      Facebook.api('/me', function(response) {
        $scope.$apply(function() {
          $scope.user = response;
        });
      });
    };

    /**
     * Logout
     */
    $scope.logout = function() {
      Facebook.logout(function() {
        $scope.$apply(function() {
          $scope.user   = {};
          $scope.logged = false;
        });
      });
    };




    $scope.submit = function() {
      return $validator.validate($scope, 'capture').success(function() {
        $scope.submitInProgress = true;
        gapi.client.wc.execution.submit({userID:$scope.authResponse.userID, token: $scope.authResponse.accessToken}).execute(function(response){
          $scope.submitInProgress = false;
          $scope.lastServerResponse = response;
          if (response.error != undefined) {
            console.error(response.error.message);
            return false;
          }
          // on success of submit empty the form and get the next one
          for (var i = ($builder.forms.capture.length - 1); i >= 0; i--) {
            $builder.removeFormObject('capture', $builder.forms.capture[i].index);
          }
          // @TODO: build new form

        });
        return true;
      }).error(function() {
        // display validation errors
        return false;
      });
    };
  };
});