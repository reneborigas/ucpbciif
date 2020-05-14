define(function() {
	'use strict';

	var lmsApp = angular.module('lmsApp', [
		'ui.router',
		'auth',
		'oc.lazyLoad',
		'toastr',
		'oitozero.ngSweetAlert',
		'ngTable',
		'ngAnimate',
		'ngSanitize',
		'blockUI',
		'ncy-angular-breadcrumb'
	]);

	lmsApp.factory('lmsService', function($http, toastr, $filter) {
		return {
			getBorrowerName: function(borrowerId){
                return $http.get('/api/borrowers/borrowers/', {params:{ borrowerId : borrowerId }}).then(
                    function(response){   
					console.log(response)
                    return response.data[0].borrowerName  
                },
                function(error){
                    toastr.error('Error '+ error.status + error.statusText, 'Could not retrieve Borrower Name. Please contact System Administrator.'); 
                });
            },
			getCurrentUser: function() {
				var values = JSON.parse(localStorage.getItem('currentUser'));
				return values['id'];
			},
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
			},
			getGenders: function(){
                return $http.get('/api/settings/gendertype/').then(
                    function(response){   
                    return response.data;     
                },
                function(error){
                    toastr.error('Error '+ error.status + error.statusText, 'Could not retrieve Gender list. Please contact System Administrator.'); 
                });     
            },
			getTimeRemaining: function(endtime, starttime) {
				var t = Date.parse(endtime) - Date.parse(starttime);
				var seconds = Math.floor((t / 1000) % 60);
				var minutes = Math.floor((t / 1000 / 60) % 60);
				var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
				var days = Math.floor(t / (1000 * 60 * 60 * 24));
				var wholedays = Math.ceil(t / (1000 * 60 * 60 * 24));
				return {
					total: t,
					days: days,
					hours: hours,
					minutes: minutes,
					seconds: seconds,
					wholedays: wholedays
				};
			},
			dateWithoutTime: function(date, format) {
				return $filter('date')(date, format);
			},
			flattenJSON: function(array) {
				var flatten = function(object) {
					var newObj = {};
					for (var key in object) {
						var item = object[key];
						if (typeof item !== 'object') {
							newObj[key] = item;
						} else {
							var flattened = flatten(item);
							for (var k in flattened) {
								newObj[k] = flattened[k];
							}
						}
					}
					return newObj;
				};

				var flattenArray = function(array) {
					var newArray = [];
					array.forEach(function(object) {
						newArray.push(flatten(object));
					});
					return newArray;
				};

				return flattenArray(array);
			},
			convertCamelCase: function(camelCase) {
				return camelCase
					.replace(/([A-Z])/g, function($1) {
						return ' ' + $1.toUpperCase();
					})
					.replace(/^./, function(str) {
						return str.toUpperCase();
					});
			},
			slugify: function(text) {
				var slug = text.toLowerCase().trim();
				slug = slug.replace(/[^a-z0-9\s-]/g, ' ');
				slug = slug.replace(/[\s-]+/g, '-');
				return slug;
			},
			unSlugify: function(text) {
				var unslug = text.toLowerCase();
				unslug = unslug.split('-');
				unslug = unslug.map((i) => i[0].toUpperCase() + i.substr(1));
				unslug = unslug.join(' ');
				return unslug;
			},
			generateUniqueID: function(length, quantity) {
				var charSet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
				var charSetSize = charSet.length;
				var idCount = quantity;
				var charCount = length;
				var generatedIds = [];

				var generateRandomId = function() {
					var id = '';
					for (var i = 1; i <= charCount; i++) {
						var randPos = Math.floor(Math.random() * charSetSize);
						id += charSet[randPos];
					}
					return id;
				};

				while (generatedIds.length < idCount) {
					var id = generateRandomId();
					if ($.inArray(id, generatedIds) == -1) {
						generatedIds.push(id);
					}
				}

				return generatedIds;
			}
		};
	});

	lmsApp.config(function($breadcrumbProvider) {
		$breadcrumbProvider.setOptions({
			templateUrl: '/statics/html/breadcrumb/breadcrumb-template.html'
		});
	});

	lmsApp.config(function($stateProvider, $locationProvider, $ocLazyLoadProvider) {
		$ocLazyLoadProvider.config({
			loadedModules: [ 'lmsApp' ],
			asyncLoader: require,
			debug: true,
			serie: true
		});

		$locationProvider.html5Mode({
			enabled: true,
			requireBase: false
		});

		$stateProvider
			.state('dashboard', {
				url: '/dashboard',
				abstract: true,
				views: {
					sideBar: {
						templateUrl: '/statics/html/sidebar/sidebar.html',
						controller: function($scope) {
							$scope.date = new Date();
						},
						resolve: {
							deps: [
								'$ocLazyLoad',
								function($ocLazyLoad) {
									return $ocLazyLoad.load([
										{
											name: 'lmsApp',
											files: [ '/statics/scripts/angular-scripts/sidebar.js' ]
										}
									]);
								}
							]
						}
					},
					'': {
						templateUrl: '/statics/html/dashboard/dashboard-parent.html',
						controller: function($scope) {
							$scope.date = new Date();
						},
						resolve: {
							deps: [
								'$ocLazyLoad',
								function($ocLazyLoad) {
									return $ocLazyLoad.load([
										{
											name: 'lmsApp',
											files: [ '/statics/scripts/angular-scripts/dashboard.js' ]
										}
									]);
								}
							]
						}
					}
				}
			})
			.state('dashboard.list', {
				url: '',
				templateUrl: '/statics/html/dashboard/dashboard-list.html',
				ncyBreadcrumb: {
					label: 'Dashboard'
				}
			})
			.state('borrowers', {
				url: '/borrowers',
				abstract: true,
				templateUrl: '/statics/html/borrowers/borrowers-parent.html',
				controller: function($scope) {
					$scope.date = new Date();
				},
				resolve: {
					deps: ['$ocLazyLoad', function($ocLazyLoad) {
						return $ocLazyLoad.load([
							{
								name: 'lmsApp',
								files: [ 
									'/statics/libs/bootstrap-datepicker/bootstrap-datepicker.min.js',
									'/statics/scripts/angular-scripts/borrowers.js', 
								]
							}
						]);
					}]
				}
			})
			.state('borrowers.list', {
				url: '',
				templateUrl: '/statics/html/borrowers/borrowers-list.html',
				ncyBreadcrumb: {
					label: 'Borrowers',
					parent: 'dashboard.list'
				},
			})
			.state('borrowers.add', {
				url: '/add',
				templateUrl: '/statics/html/borrowers/borrowers-add.html',
				ncyBreadcrumb: {
					label: 'New Borrower',
					parent: 'borrowers.list'
				},
			})
			.state('borrowers.info', {
				url: '/:borrowerId',
				templateUrl: '/statics/html/borrowers/borrowers-info.html',
				controller: function($scope,$stateParams,$state,lmsService) {
					$scope.borrowerId = $stateParams.borrowerId;
					lmsService.getBorrowerName($scope.borrowerId).then(function(borrower){
                        $scope.borrowerName = borrower
                    });
                },
				ncyBreadcrumb: {
					label: '{{ borrowerName }}',
					parent: 'borrowers.list'
				},
			})
			.state('borrowers.edit', {
				url: '/:borrowerId/edit',
				templateUrl: '/statics/html/borrowers/borrowers-edit.html',
				controller: function($scope,$stateParams,$state,lmsService) {
					$scope.borrowerId = $stateParams.borrowerId;
					lmsService.getBorrowerName($scope.borrowerId).then(function(borrower){
                        $scope.borrowerName = borrower
                    });
                },
				ncyBreadcrumb: {
					label: 'Edit',
					parent: 'borrowers.info'
				},
			})
	});

	lmsApp.run(function run($http, $rootScope, $state) {
		$http.defaults.xsrfHeaderName = 'X-CSRFToken';
		$http.defaults.xsrfCookieName = 'csrftoken';
		$rootScope.$state = $state;
	});

	lmsApp.controller('ProfileController', function ProfileController($scope, Login, lmsService, $rootScope) {
		$scope.logout = Login.logout;
		Login.redirectIfNotLoggedIn();
		$scope.showHeader = false;
		$scope.showHeader = Login.isLoggedIn();
	});

	lmsApp.directive('datePicker', function() {
		return {
			restrict: 'EA',
			link: function(scope, element, attrs) {
				element.datepicker({
					autoclose: true,
					orientation: 'bottom left',
					format: 'yyyy-mm-dd',
				});
			}
		};
	});

	lmsApp.directive('periodPicker', function() {
		return {
			restrict: 'EA',
			link: function(scope, element, attrs) {
				element.datepicker({
					autoclose: true,
					format: 'yyyy-mm-dd',
					startView: 'months',
					minViewMode: 'months'
				});
			}
		};
	});

	lmsApp.filter('amountLowerThan', function() {
		return function(items, lowerThan) {
			items = items.filter(function(item) {
				return item.amount > lowerThan;
			});
			return items;
		};
	});


});
