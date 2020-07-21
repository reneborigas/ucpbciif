define(function () {
    'use strict';

    var app = angular.module('app');

    app.controller('LoginController', function LoginController(
        $scope,
        appLoginService,
        toastr,
        $http,
        appFactory,
        $timeout
    ) {
        $scope.login = function () {
            appLoginService.login($scope.user).then(
                function () {
                    var user = JSON.parse(localStorage.getItem('currentUser'));
                    var now = new Date();
                    var userLogs = {
                        user: user['id'],
                        action_type: 'Logged In',
                        content_type: '',
                        object_id: user['id'],
                        object_type: 'User Account',
                        apiLink: '/api/users/users',
                        valueToDisplay: 'fullName',
                        logDetails: [
                            {
                                action: 'Logged in by ' + now,
                            },
                        ],
                    };
                    return appFactory.getContentTypeId('customuser').then(function (data) {
                        userLogs.content_type = data;
                        return $http.post('/api/users/userlogs/', userLogs).then(
                            function () {
                                toastr.success('Success', 'Logging in');
                                $timeout(function () {
                                    window.location.href = '/menu';
                                }, 1000);
                            },
                            function (error) {
                                toastr.error(
                                    'Error ' + error.status + ' ' + error.statusText,
                                    'Could not record logs.  Please contact System Administrator'
                                );
                            }
                        );
                    });
                },
                function (error) {
                    toastr.error(error.data.message, 'Error!');
                }
            );
        };

        $scope.forgotPass = function () {};

        console.log(appLoginService.isLoggedIn());
        if (appLoginService.isLoggedIn()) {
            // var user = JSON.parse(localStorage.getItem('currentUser'));
            // var now = new Date();
            // var userLogs = {
            // 	user: user['id'],
            // 	action_type: 'Logged In',
            // 	content_type: '',
            // 	object_id: user['id'],
            // 	object_type: 'User Account',
            // 	apiLink: '/api/users/users',
            // 	valueToDisplay: 'fullName',
            // 	logDetails: [
            // 		{
            // 			action: 'Logged in by ' + now
            // 		}
            // 	]
            // };
            // return loginService.getContentTypeId('customuser').then(function(data) {
            // 	userLogs.content_type = data;
            // 	return $http.post('/api/users/userlogs/', userLogs).then(
            // 		function() {
            // 			toastr.success('Success', 'Currently Logged in. Granted Access.');
            // 			window.location.href = '/dashboard';
            // 		},
            // 		function(error) {
            // 			toastr.error(
            // 				'Error ' + error.status + ' ' + error.statusText,
            // 				'Could not record logs.  Please contact System Administrator'
            // 			);
            // 		}
            // 	);
            // });
        }
    });
});
