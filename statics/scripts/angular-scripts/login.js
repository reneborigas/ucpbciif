define(function() {
	'use strict';

	var login = angular.module('login', [ 'ui.router', 'auth', 'toastr' ]);

	login.factory('loginService', function($http, toastr) {
		return {
			getContentTypeId: function(model) {
				return $http.get('/api/users/contenttype/', { params: { model: model } }).then(
					function(response) {
						return response.data[0].id;
					},
					function(error) {
						toastr.error(
							'Error ' + error.status + error.statusText,
							'Could not retrieve Content Type Id. Please contact System Administrator.'
						);
					}
				);
			}
		};
	});

	login.config(function($locationProvider) {
		$locationProvider.html5Mode({
			enabled: true,
			requireBase: false
		});
	});

	login.run([
		'$http',
		function run($http) {
			$http.defaults.xsrfHeaderName = 'X-CSRFToken';
			$http.defaults.xsrfCookieName = 'csrftoken';
		}
	]);

	login.controller('LoginController', function LoginController($scope, Login, toastr, $http, loginService) {

		$scope.login = function() {
			Login.login($scope.user).then(
				function() {
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
								action: 'Logged in by ' + now
							}
						]
					};
					return loginService.getContentTypeId('customuser').then(function(data) {
						userLogs.content_type = data;
						return $http.post('/api/users/userlogs/', userLogs).then(
							function() {
								toastr.success('Success', 'Logging in');
								window.location.href = '/dashboard';
							},
							function(error) {
								toastr.error(
									'Error ' + error.status + ' ' + error.statusText,
									'Could not record logs.  Please contact System Administrator'
								);
							}
						);
					});
				},
				function(error) {
					toastr.error(error.data.message, 'Error ' + error.status + ' ' + error.statusText);
				}
			);
		};

		if (Login.isLoggedIn()) {
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
