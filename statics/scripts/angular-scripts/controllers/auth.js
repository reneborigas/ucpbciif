define(function() {
	'use strict';

	var auth = angular.module('auth', []);

	auth.factory('authService', function($http, toastr) {
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

	auth.service('Login', function Login($http, $location, $window, $timeout, toastr,authService) {
		this.login = login;
		this.isLoggedIn = isLoggedIn;
		this.logout = logout;
		this.redirectIfNotLoggedIn = redirectIfNotLoggedIn;

		function login(credentials) {
			return $http.post('/api/auth/login/', credentials).then(function(response) {
				localStorage.currentUser = JSON.stringify(response.data);
			});
		}

		function isLoggedIn() {
			return !!localStorage.currentUser;
		}

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
						action: 'Logged out by ' + now
					}
				]
			};
			return authService.getContentTypeId('customuser').then(function(data) {
				userLogs.content_type = data;
				return $http.post('/api/users/userlogs/', userLogs).then(
					function() {
						var baseUrl = new $window.URL($location.absUrl()).origin;
						delete localStorage.currentUser;
						$http.get(baseUrl + '/api/auth/logout/').then(function() {
							window.location.href = '/login';
						});
					},
					function(error) {
						toastr.error(
							'Error ' + error.status + ' ' + error.statusText,
							'Could not record logs.  Please contact System Administrator'
						);
					}
				);
			});
		}

		function redirectIfNotLoggedIn() {
			if (!isLoggedIn()) {
				window.location.href = '/login';
			}
		}
	});
});
