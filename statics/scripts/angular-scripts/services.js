define(function () {
    'use strict';

    var app = angular.module('app');

    app.service('appLoginService', function appLoginService($http, $location, $window, $timeout, toastr, appFactory, $state, $q) {
        this.login = login;
        this.isLoggedIn = isLoggedIn;
        this.logout = logout;
        this.redirectIfNotLoggedIn = redirectIfNotLoggedIn;
        this.setTitle = setTitle;

        function login(credentials) {
            return $http.post('/api/auth/login/', credentials).then(function (response) {
                localStorage.currentUser = JSON.stringify(response.data);
            });
        }

        function isLoggedIn() {
            if (localStorage.currentUser) {
                return $http.get('/api/auth/checkauth/').then(
                    function (response) {
                        return true;
                    },
                    function (error) {
                        return false;
                    }
                );
            } else {
                return false;
            }
        }

        // function isLoggedIn() {
        //     if (localStorage.currentUser) {
        //         return $http.get('/api/auth/checkauth/').then(
        //             function (response) {
        //                 $q.defer().resolve(response);
        //             },
        //             function (error) {
        //                 $q.defer().reject('Unauthorized');
        //             }
        //         );
        //     } else {
        //         $q.defer().reject('Unauthorized');
        //     }
        //     return $q.defer().promise;
        // }

        function logout() {
            var user = JSON.parse(localStorage.getItem('currentUser'));
            var now = new Date();
            var userLogs = {
                user: user['id'],
                action_type: 'Logged Out',
                content_type: '',
                object_id: user['id'],
                object_type: 'User Account',
                apiLink: '/api/users/users',
                valueToDisplay: 'fullName',
                logDetails: [
                    {
                        action: 'Logged out by ' + now,
                    },
                ],
            };
            return appFactory.getContentTypeId('customuser').then(function (data) {
                userLogs.content_type = data;
                return $http.post('/api/users/userlogs/', userLogs).then(
                    function () {
                        var baseUrl = new $window.URL($location.absUrl()).origin;
                        delete localStorage.currentUser;
                        $http.get(baseUrl + '/api/auth/logout/').then(function () {
                            window.location.href = '/login';
                        });
                    },
                    function (error) {
                        toastr.error('Error ' + error.status + ' ' + error.statusText, 'Could not record logs. Please contact System Administrator');
                    }
                );
            });
        }

        function redirectIfNotLoggedIn() {
            if (!isLoggedIn()) {
                $state.go('simple.login');
            }
        }

        function setTitle(newTitle) {
            $window.document.title = newTitle;
        }
    });
});
