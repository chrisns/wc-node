define(function () {
    'use strict';

    function LoginService($q, Facebook){
        this.$q = $q;
        this.Facebook = Facebook;

        this._loggedIn = false;
        this._authToken = '';
        this._user = {};
    }

    LoginService.prototype = {
        login: function () {
            return this._login()
                .then(function() {

                    return this._fetchCurrentUser();
                }.bind(this))
                .then(function (response) {
                    this._user = response;
                })
                .then(this._getLoginStatus.bind(this))
                .then(function (response) {
                    this._authToken = response.authToken;
                }.bind(this));
        },
        getCurrentUser : function () {
            return this._user;
        },

        getAuthToken: function () {
            return this._authToken;
        },

        _fetchCurrentUser:function () {
            return this.Facebook.api('/me');
        },
        _login: function () {
            return this.Facebook.login();
        },
        _getLoginStatus: function () {
            return this.Facebook.getLoginStatus();
        }
    };

    LoginService.$inject = ['$q'];

    return LoginService;
});