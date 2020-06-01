define(function() {
	'use strict';
	
	var app =  angular.module('app');

	app.config(['$stateProvider', '$urlRouterProvider', '$ocLazyLoadProvider', '$breadcrumbProvider','$locationProvider', function ($stateProvider, $urlRouterProvider, $ocLazyLoadProvider, $breadcrumbProvider, $locationProvider) {


			$ocLazyLoadProvider.config({
				debug: true
			});

			$breadcrumbProvider.setOptions({
				prefixStateName: 'app.main',
				includeAbstract: true,
				// template: '<li class="breadcrumb-item" ng-repeat="step in steps" ng-class="{active: $last}" ng-switch="$last || !!step.abstract"><a ng-switch-when="false" href="{{step.ncyBreadcrumbLink}}">{{step.ncyBreadcrumbLabel}}</a><span ng-switch-when="true">{{step.ncyBreadcrumbLabel}}</span></li>'
				templateUrl: '/statics/partials/components/full/breadcrumb.html'
			});

			$locationProvider.html5Mode({
				enabled: true,
				requireBase: false
			});

			$stateProvider
				.state('app', {
					abstract: true,
					templateUrl: '/statics/partials/layouts/full.html',
					ncyBreadcrumb: {
						label: 'Root',
						skip: true
					},
					resolve: {
						loadCSS: ['$ocLazyLoad', function ($ocLazyLoad) {
							// you can lazy load CSS files
							return $ocLazyLoad.load([{
								serie: true,
								name: 'Font Awesome',
								files: ['/statics/assets/fonts/font-awesome/css/fontawesome-all.css']
							}, {
								serie: true,
								name: 'Simple Line Icons',
								files: ['/statics/assets/fonts/simple-line-icons/css/simple-line-icons.css']
							}, {
								serie: true,
								name: 'Bundle Styles',
								files: ['/statics/assets/css/style-bundle.css']
							}, {
								serie: true,
								name: 'Styles',
								files: ['/statics/assets/css/style.css']
							}, {
								serie: true,
								name: 'Custom Styles',
								files: ['/statics/assets/css/custom.css']
							}, {
								serie: true,
								name: 'Toastr Styles',
								files: ['/statics/libs/toastr/dist/css/angular-toastr.min.css']
							}, {
								serie: true,
								name: 'Sweet Alert Styles',
								files: ['/statics/libs/sweetalert/sweetalert.css']
							}, {
								serie: true,
								name: 'ngTable Styles',
								files: ['/statics/libs/ngTable/ng-table.min.css']
							}]);
						}],
						loadController: ['$ocLazyLoad', function ($ocLazyLoad) {
							return $ocLazyLoad.load({
								files: [
									'/statics/scripts/angular-scripts/controllers/app.js'
								]
							});
						}]
						// loadPlugin: ['$ocLazyLoad', function ($ocLazyLoad) {
						// 	// you can lazy load files for an existing module
						// 	return $ocLazyLoad.load([{
						// 		serie: true,
						// 		name: 'chart.js',
						// 		files: [
						// 			'node_modules/chart.js/dist/Chart.min.js',
						// 			'node_modules/angular-chart.js/dist/angular-chart.min.js'
						// 		]
						// 	}]);
						// }],
					},
					// controller: function(appLoginService) {
					// 	appLoginService.redirectIfNotLoggedIn();
					// },
				})
				.state('app.main', {
					url: '/dashboard',
					templateUrl: '/statics/partials/pages/dashboard/dashboard.html',
					data: { 
						pageTitle: 'UCPB CIIF | Dashboard',
						stateTitle: 'Dashboard'
					},
					ncyBreadcrumb: {
						label: 'Home',
					},
					// resolve: {
					// 	loadPlugin: ['$ocLazyLoad', function ($ocLazyLoad) {
					// 		// you can lazy load files for an existing module
					// 		return $ocLazyLoad.load([
					// 			{
					// 				serie: true,
					// 				name: 'chart.js',
					// 				files: [
					// 					'node_modules/chart.js/dist/Chart.min.js',
					// 					'node_modules/angular-chart.js/dist/angular-chart.min.js'
					// 				]
					// 			},
					// 		]);
					// 	}],
					// 	loadMyCtrl: ['$ocLazyLoad', function ($ocLazyLoad) {
					// 		// you can lazy load controllers
					// 		return $ocLazyLoad.load({
					// 			files: ['js/controllers/main.js']
					// 		});
					// 	}]
					// }
					controller: function(appLoginService) {
						appLoginService.setTitle = "test"
					},
				})
				.state('app.borrowers', {
					url: '/borrowers',
					template: '<ui-view></ui-view>',
					abstract: true,
					ncyBreadcrumb: {
						label: 'Borrowers',
						skip:true
					},
					resolve: {
						loadController: ['$ocLazyLoad', function ($ocLazyLoad) {
							return $ocLazyLoad.load({
								files: [
									'/statics/scripts/angular-scripts/controllers/borrowers.js'
								]
							});
						}]
					},
				})
				.state('app.borrowers.list', {
					url: '',
					templateUrl: '/statics/partials/pages/borrowers/borrowers-list.html',
					data: { 
						pageTitle: 'UCPB CIIF | Borrowers List',
						stateTitle: 'Borrowers'
					},
					ncyBreadcrumb: {
						label: 'Borrowers',
					},
					// resolve: {
					// 	loadPlugin: ['$ocLazyLoad', function ($ocLazyLoad) {
					// 		// you can lazy load files for an existing module
					// 		return $ocLazyLoad.load([
					// 			{
					// 				serie: true,
					// 				name: 'chart.js',
					// 				files: [
					// 					'node_modules/chart.js/dist/Chart.min.js',
					// 					'node_modules/angular-chart.js/dist/angular-chart.min.js'
					// 				]
					// 			},
					// 		]);
					// 	}],
					// 	loadMyCtrl: ['$ocLazyLoad', function ($ocLazyLoad) {
					// 		// you can lazy load controllers
					// 		return $ocLazyLoad.load({
					// 			files: ['js/controllers/main.js']
					// 		});
					// 	}]
					// },
				})
				.state('app.borrowers.add', {
					url: '/add',
					templateUrl: '/statics/partials/pages/borrowers/borrowers-add.html',
					data: { 
						pageTitle: 'UCPB CIIF | Add Borrower' 
					},
					ncyBreadcrumb: {
						label: 'Add',
						parent: 'app.borrowers.list'
					},
					// resolve: {
					// 	loadPlugin: ['$ocLazyLoad', function ($ocLazyLoad) {
					// 		// you can lazy load files for an existing module
					// 		return $ocLazyLoad.load([
					// 			{
					// 				serie: true,
					// 				name: 'chart.js',
					// 				files: [
					// 					'node_modules/chart.js/dist/Chart.min.js',
					// 					'node_modules/angular-chart.js/dist/angular-chart.min.js'
					// 				]
					// 			},
					// 		]);
					// 	}],
					// 	loadMyCtrl: ['$ocLazyLoad', function ($ocLazyLoad) {
					// 		// you can lazy load controllers
					// 		return $ocLazyLoad.load({
					// 			files: ['js/controllers/main.js']
					// 		});
					// 	}]
					// },
				})
				.state('app.borrowers.info', {
					url: '/:borrowerId',
					templateUrl: '/statics/partials/pages/borrowers/borrowers-info.html',
					data: { 
						pageTitle: 'UCPB CIIF | Borrower Info' 
					},
					ncyBreadcrumb: {
						label: '{{ borrowerName }}',
						parent: 'app.borrowers.list'
					},
					controller: function($scope,$stateParams,appFactory){
						$scope.borrowerId = $stateParams.borrowerId;
						appFactory.getBorrowerName($scope.borrowerId).then(function(data){
							$scope.borrowerName = data;
						})
					}
					// resolve: {
					// 	loadPlugin: ['$ocLazyLoad', function ($ocLazyLoad) {
					// 		// you can lazy load files for an existing module
					// 		return $ocLazyLoad.load([
					// 			{
					// 				serie: true,
					// 				name: 'chart.js',
					// 				files: [
					// 					'node_modules/chart.js/dist/Chart.min.js',
					// 					'node_modules/angular-chart.js/dist/angular-chart.min.js'
					// 				]
					// 			},
					// 		]);
					// 	}],
					// 	loadMyCtrl: ['$ocLazyLoad', function ($ocLazyLoad) {
					// 		// you can lazy load controllers
					// 		return $ocLazyLoad.load({
					// 			files: ['js/controllers/main.js']
					// 		});
					// 	}]
					// },
				})
				.state('app.borrowers.edit', {
					url: '/:borrowerId/edit',
					templateUrl: '/statics/partials/pages/borrowers/borrowers-edit-test.html',
					data: { 
						pageTitle: 'UCPB CIIF | Borrower Sample' 
					},
					ncyBreadcrumb: {
						label: 'Sample',
						parent: 'app.borrowers.list'
					},
				})


				.state('app.loans', {
					url: '/loans',
					template: '<ui-view></ui-view>',
					abstract: true,
					ncyBreadcrumb: {
						label: 'Loans',
						skip:true
					},
					params: { title:'Loans', subtitle: 'Welcome to ROOT powerfull Bootstrap & AngularJS UI Kit' },
					resolve: {
						loadController: ['$ocLazyLoad', function ($ocLazyLoad) {
							return $ocLazyLoad.load({
								files: [
									'/statics/scripts/angular-scripts/controllers/loans.js'
								]
							});
						}]
					},
				})
				.state('app.loans.list', {
					url: '',
					templateUrl: '/statics/partials/pages/loans/loans-list.html',
					ncyBreadcrumb: {
						label: 'Loans',
						skip:true
					},
					params: { title:'Loans', subtitle: 'Welcome to ROOT powerfull Bootstrap & AngularJS UI Kit' },
					resolve: {
						loadController: ['$ocLazyLoad', function ($ocLazyLoad) {
							return $ocLazyLoad.load({
								files: [
									'/statics/scripts/angular-scripts/controllers/loans.js'
								]
							});
						}]
					},
				})
				
				.state('app.documents', {
					url: '/documents',
					template: '<ui-view></ui-view>',
					abstract: true,
					ncyBreadcrumb: {
						label: 'Documents',
						skip:true
					},
					params: { title:'Documents', subtitle: 'Welcome to ROOT powerfull Bootstrap & AngularJS UI Kit' },
					resolve: {
						loadController: ['$ocLazyLoad', function ($ocLazyLoad) {
							return $ocLazyLoad.load({
								files: [
									'/statics/scripts/angular-scripts/controllers/documents.js'
								]
							});
						}]
					},
				})
				.state('app.documents.list', {
					url: '',
					templateUrl: '/statics/partials/pages/documents/documents-list.html',
					ncyBreadcrumb: {
						label: 'Documents',
						skip:true
					},
					params: { title:'Documents', subtitle: 'Welcome to ROOT powerfull Bootstrap & AngularJS UI Kit' },
					resolve: {
						loadController: ['$ocLazyLoad', function ($ocLazyLoad) {
							return $ocLazyLoad.load({
								files: [
									'/statics/scripts/angular-scripts/controllers/documents.js'
								]
							});
						}]
					},
				})
				.state('app.loans.add', {
					url: '/add',
					templateUrl: '/statics/partials/pages/loans/loans-add.html',
					ncyBreadcrumb: {
						label: 'Add',
						parent: 'app.loans.list'
					},
					// resolve: {
					// 	loadPlugin: ['$ocLazyLoad', function ($ocLazyLoad) {
					// 		// you can lazy load files for an existing module
					// 		return $ocLazyLoad.load([
					// 			{
					// 				serie: true,
					// 				name: 'chart.js',
					// 				files: [
					// 					'node_modules/chart.js/dist/Chart.min.js',
					// 					'node_modules/angular-chart.js/dist/angular-chart.min.js'
					// 				]
					// 			},
					// 		]);
					// 	}],
					// 	loadMyCtrl: ['$ocLazyLoad', function ($ocLazyLoad) {
					// 		// you can lazy load controllers
					// 		return $ocLazyLoad.load({
					// 			files: ['js/controllers/main.js']
					// 		});
					// 	}]
					// },
				})

				.state('simple', {
					abstract: true,
					templateUrl: '/statics/partials/layouts/simple.html',
					resolve: {
						loadCSS: ['$ocLazyLoad', function ($ocLazyLoad) {
							return $ocLazyLoad.load([{
								serie: true,
								name: 'Font Awesome',
								files: ['/statics/assets/fonts/font-awesome/css/fontawesome-all.css']
							}, {
								serie: true,
								name: 'Simple Line Icons',
								files: ['/statics/assets/fonts/simple-line-icons/css/simple-line-icons.css']
							}, {
								serie: true,
								name: 'Styles',
								files: ['/statics/assets/css/style.css']
							}, {
								serie: true,
								name: 'Custom Styles',
								files: ['/statics/assets/css/custom.css']
							}, {
								serie: true,
								name: 'Toastr Styles',
								files: ['/statics/libs/toastr/dist/css/angular-toastr.min.css']
							}]);
						}],
					}
				})
				.state('simple.login', {
					url: '/login',
					templateUrl: '/statics/partials/components/simple/login.html',
					data: { 
						pageTitle: 'UCPB CIIF | Loan Management System' 
					},
					resolve: {
						loadController: ['$ocLazyLoad', function ($ocLazyLoad) {
							return $ocLazyLoad.load({
								files: [
									'/statics/scripts/angular-scripts/controllers/login.js'
								]
							});
						}]
					},
				})
				.state('simple.register', {
					url: '/register',
					templateUrl: '/statics/html/views/pages/register.html'
				})
				.state('simple.404', {
					url: '/404',
					templateUrl: '/statics/html/views/pages/404.html'
				})
				.state('simple.500', {
					url: '/500',
					templateUrl: '/statics/html/views/pages/500.html',
				})

			$urlRouterProvider.otherwise('/');

		}])


});
