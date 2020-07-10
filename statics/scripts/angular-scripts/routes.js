define(function () {
    'use strict';

    var app = angular.module('app');

    app.config([
        '$stateProvider',
        '$urlRouterProvider',
        '$ocLazyLoadProvider',
        '$breadcrumbProvider',
        '$locationProvider',
        function ($stateProvider, $urlRouterProvider, $ocLazyLoadProvider, $breadcrumbProvider, $locationProvider) {
            $ocLazyLoadProvider.config({
                debug: true,
            });

            $breadcrumbProvider.setOptions({
                prefixStateName: 'app.main',
                includeAbstract: true,
                // template: '<li class="breadcrumb-item" ng-repeat="step in steps" ng-class="{active: $last}" ng-switch="$last || !!step.abstract"><a ng-switch-when="false" href="{{step.ncyBreadcrumbLink}}">{{step.ncyBreadcrumbLabel}}</a><span ng-switch-when="true">{{step.ncyBreadcrumbLabel}}</span></li>'
                templateUrl: '/statics/partials/components/full/breadcrumb.html',
            });

            $locationProvider.html5Mode({
                enabled: true,
                requireBase: false,
            });

            $stateProvider
                .state('app', {
                    abstract: true,
                    templateUrl: '/statics/partials/layouts/full.html',
                    ncyBreadcrumb: {
                        label: 'Root',
                        skip: true,
                    },
                    resolve: {
                        loadCSS: [
                            '$ocLazyLoad',
                            function ($ocLazyLoad) {
                                return $ocLazyLoad.load([
                                    {
                                        serie: true,
                                        name: 'Font Awesome',
                                        files: ['/statics/assets/fonts/font-awesome/css/fontawesome-all.css'],
                                    },
                                    {
                                        serie: true,
                                        name: 'Simple Line Icons',
                                        files: ['/statics/assets/fonts/simple-line-icons/css/simple-line-icons.css'],
                                    },
                                    {
                                        serie: true,
                                        name: 'App Styles',
                                        files: ['/statics/assets/css/style.css'],
                                    },
                                    {
                                        serie: true,
                                        name: 'Custom Styles',
                                        files: ['/statics/assets/css/custom.css'],
                                    },
                                    {
                                        serie: true,
                                        name: 'Toastr Styles',
                                        files: ['/statics/libs/toastr/dist/css/angular-toastr.min.css'],
                                    },
                                    {
                                        serie: true,
                                        name: 'Sweet Alert Styles',
                                        files: ['/statics/libs/sweetalert/sweetalert.css'],
                                    },
                                    {
                                        serie: true,
                                        name: 'ngTable Styles',
                                        files: ['/statics/libs/ngTable/ng-table.min.css'],
                                    },
                                    {
                                        serie: true,
                                        name: 'ngBlock Styles',
                                        files: ['/statics/libs/ngBlock/angular-block-ui.css'],
                                    },
                                ]);
                            },
                        ],
                        loadController: [
                            '$ocLazyLoad',
                            function ($ocLazyLoad) {
                                return $ocLazyLoad.load({
                                    files: ['/statics/scripts/angular-scripts/controllers/app.js'],
                                });
                            },
                        ],
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
                })
                .state('app.main', {
                    url: '/dashboard',
                    templateUrl: '/statics/partials/pages/dashboard/dashboard.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Dashboard',
                        stateTitle: 'Dashboard',
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
                    controller: function (appLoginService) {
                        appLoginService.setTitle = 'test';
                    },
                })
                .state('app.borrowers', {
                    url: '/borrowers',
                    template: '<ui-view></ui-view>',
                    abstract: true,
                    ncyBreadcrumb: {
                        label: 'Borrowers',
                        skip: true,
                    },
                    resolve: {
                        loadController: [
                            '$ocLazyLoad',
                            function ($ocLazyLoad) {
                                return $ocLazyLoad.load({
                                    files: ['/statics/scripts/angular-scripts/controllers/borrowers.js'],
                                });
                            },
                        ],
                    },
                })
                .state('app.borrowers.list', {
                    url: '',
                    templateUrl: '/statics/partials/pages/borrowers/borrowers-list.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Borrowers List',
                        stateTitle: 'Borrowers',
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
                        pageTitle: 'UCPB CIIF | Add Borrower',
                    },
                    ncyBreadcrumb: {
                        label: 'Add',
                        parent: 'app.borrowers.list',
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
                .state('app.borrowers.create_loan_application', {
                    url: '/:borrowerId/new-file/:subProcessId',
                    templateUrl: '/statics/partials/pages/borrowers/borrowers-new-loan-application.html',
                    data: {
                        pageTitle: 'UCPB CIIF | New Loan Application',
                    },
                    ncyBreadcrumb: {
                        label: 'New {{subProcess.name}} File',
                        parent: 'app.borrowers.info',
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.borrowerId = $stateParams.borrowerId;
                        $scope.subProcessId = $stateParams.subProcessId;
                        console.log($scope.subProcessId);
                        appFactory.getBorrowerName($scope.borrowerId).then(function (data) {
                            $scope.borrowerName = data;
                        });

                        appFactory.getSubProcess($scope.subProcessId).then(function (data) {
                            $scope.subProcess = data;
                        });
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
                        pageTitle: 'UCPB CIIF | Borrower Info',
                    },
                    ncyBreadcrumb: {
                        label: '{{ borrowerName }}',
                        parent: 'app.borrowers.list',
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.borrowerId = $stateParams.borrowerId;
                        appFactory.getBorrowerName($scope.borrowerId).then(function (data) {
                            $scope.borrowerName = data;
                        });
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
                .state('app.borrowers.edit', {
                    url: '/:borrowerId/edit',
                    templateUrl: '/statics/partials/pages/borrowers/borrowers-edit.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Borrower Edit',
                    },
                    ncyBreadcrumb: {
                        label: 'Edit',
                        parent: 'app.borrowers.info',
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.borrowerId = $stateParams.borrowerId;
                        appFactory.getBorrowerName($scope.borrowerId).then(function (data) {
                            $scope.borrowerName = data;
                        });
                    },
                })

                .state('app.loans', {
                    url: '/loans',
                    template: '<ui-view></ui-view>',
                    abstract: true,
                    ncyBreadcrumb: {
                        label: 'Loans',
                        skip: true,
                    },
                    params: { title: 'Loans', subtitle: 'Welcome to ROOT powerfull Bootstrap & AngularJS UI Kit' },
                    resolve: {
                        loadController: [
                            '$ocLazyLoad',
                            function ($ocLazyLoad) {
                                return $ocLazyLoad.load({
                                    files: ['/statics/scripts/angular-scripts/controllers/loans.js'],
                                });
                            },
                        ],
                    },
                })
                .state('app.loans.list', {
                    url: '',
                    templateUrl: '/statics/partials/pages/loans/loans-list.html',
                    ncyBreadcrumb: {
                        label: 'Loans',
                        skip: true,
                    },
                    params: { title: 'Loans', subtitle: 'Welcome to ROOT powerfull Bootstrap & AngularJS UI Kit' },
                    resolve: {
                        loadController: [
                            '$ocLazyLoad',
                            function ($ocLazyLoad) {
                                return $ocLazyLoad.load({
                                    files: ['/statics/scripts/angular-scripts/controllers/loans.js'],
                                });
                            },
                        ],
                    },
                })

                .state('app.documents', {
                    url: '/files',
                    template: '<ui-view></ui-view>',
                    abstract: true,
                    ncyBreadcrumb: {
                        label: 'Files',
                        skip: true,
                    },
                    resolve: {
                        loadController: [
                            '$ocLazyLoad',
                            function ($ocLazyLoad) {
                                return $ocLazyLoad.load({
                                    files: ['/statics/scripts/angular-scripts/controllers/documents.js'],
                                });
                            },
                        ],
                    },
                })
                .state('app.documents.list', {
                    url: '/:subProcessName',
                    templateUrl: '/statics/partials/pages/documents/documents-list.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Loan Applications',
                    },
                    ncyBreadcrumb: {
                        label: 'Files',
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.subProcessName = appFactory.unSlugify($stateParams.subProcessName);
                        appFactory.getSubProcessId($scope.subProcessName).then(function (data) {
                            $scope.subProcessId = data;
                        });
                    },
                })
                .state('app.documents.info', {
                    url: '/:subProcessName/:documentId',
                    templateUrl: '/statics/partials/pages/documents/documents-info.html',
                    data: {
                        pageTitle: 'UCPB CIIF | File Info',
                    },
                    ncyBreadcrumb: {
                        label: '{{ fileName }}',
                        parent: 'app.documents.list',
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.documentId = $stateParams.documentId;
                        appFactory.getDocumentName($scope.documentId).then(function (data) {
                            $scope.fileName = data;
                        });
                    },
                })
                .state('app.loans.add', {
                    url: '/add',
                    templateUrl: '/statics/partials/pages/loans/loans-add.html',
                    ncyBreadcrumb: {
                        label: 'Add',
                        parent: 'app.loans.list',
                    },
                })
                .state('app.committees', {
                    url: '/committees',
                    template: '<ui-view></ui-view>',
                    abstract: true,
                    ncyBreadcrumb: {
                        label: 'Committees',
                        skip: true,
                    },
                    resolve: {
                        loadController: [
                            '$ocLazyLoad',
                            function ($ocLazyLoad) {
                                return $ocLazyLoad.load({
                                    files: ['/statics/scripts/angular-scripts/controllers/committees.js'],
                                });
                            },
                        ],
                    },
                })
                .state('app.committees.offices', {
                    url: '',
                    templateUrl: '/statics/partials/pages/committees/committees-offices.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Committee Offices List',
                        stateTitle: 'Committee Offices',
                    },
                    ncyBreadcrumb: {
                        label: 'Committee Offices',
                    },
                })
                .state('app.committees.add_office', {
                    url: '/add',
                    templateUrl: '/statics/partials/pages/committees/committees-offices-add.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Committee Offices Add',
                        stateTitle: 'Committee Offices Add',
                    },
                    ncyBreadcrumb: {
                        label: 'Add',
                        parent: 'app.committees.offices',
                    },
                })
                .state('app.committees.info', {
                    url: '/:officeName',
                    templateUrl: '/statics/partials/pages/committees/committees-info.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Committee Offices Info',
                    },
                    ncyBreadcrumb: {
                        label: '{{ officeName }}',
                        parent: 'app.committees.offices',
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.officeName = appFactory.unSlugify($stateParams.officeName);
                    },
                })
                .state('app.committees.member', {
                    url: '/:officeName/:committeeId',
                    templateUrl: '/statics/partials/pages/committees/committees-info-member.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Committee Member',
                    },
                    ncyBreadcrumb: {
                        label: '{{ committeeName }}',
                        parent: 'app.committees.info',
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.committeeId = $stateParams.committeeId;
                        appFactory.getCommitteeName($scope.committeeId).then(function (data) {
                            $scope.committeeName = data;
                        });
                        $scope.officeName = appFactory.unSlugify($stateParams.officeName);
                    },
                })

                // Login
                .state('simple', {
                    abstract: true,
                    templateUrl: '/statics/partials/layouts/simple.html',
                    resolve: {
                        loadCSS: [
                            '$ocLazyLoad',
                            function ($ocLazyLoad) {
                                return $ocLazyLoad.load([
                                    {
                                        serie: true,
                                        name: 'Font Awesome',
                                        files: ['/statics/assets/fonts/font-awesome/css/fontawesome-all.css'],
                                    },
                                    {
                                        serie: true,
                                        name: 'Simple Line Icons',
                                        files: ['/statics/assets/fonts/simple-line-icons/css/simple-line-icons.css'],
                                    },
                                    {
                                        serie: true,
                                        name: 'Styles',
                                        files: ['/statics/assets/css/style.css'],
                                    },
                                    {
                                        serie: true,
                                        name: 'Custom Styles',
                                        files: ['/statics/assets/css/custom.css'],
                                    },
                                    {
                                        serie: true,
                                        name: 'Toastr Styles',
                                        files: ['/statics/libs/toastr/dist/css/angular-toastr.min.css'],
                                    },
                                ]);
                            },
                        ],
                    },
                })
                .state('simple.login', {
                    url: '/login',
                    templateUrl: '/statics/partials/components/simple/login.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Loan Management System',
                    },
                    resolve: {
                        loadController: [
                            '$ocLazyLoad',
                            function ($ocLazyLoad) {
                                return $ocLazyLoad.load({
                                    files: ['/statics/scripts/angular-scripts/controllers/login.js'],
                                });
                            },
                        ],
                    },
                })
                .state('simple.register', {
                    url: '/register',
                    templateUrl: '/statics/html/views/pages/register.html',
                })
                .state('simple.404', {
                    url: '/404',
                    templateUrl: '/statics/html/views/pages/404.html',
                })
                .state('simple.500', {
                    url: '/500',
                    templateUrl: '/statics/html/views/pages/500.html',
                })

                //Print
                .state('print', {
                    abstract: true,
                    templateUrl: '/statics/partials/layouts/print.html',
                    resolve: {
                        loadCSS: [
                            '$ocLazyLoad',
                            function ($ocLazyLoad) {
                                return $ocLazyLoad.load([
                                    {
                                        serie: true,
                                        name: 'Font Awesome',
                                        files: ['/statics/assets/fonts/font-awesome/css/fontawesome-all.css'],
                                    },
                                    {
                                        serie: true,
                                        name: 'Simple Line Icons',
                                        files: ['/statics/assets/fonts/simple-line-icons/css/simple-line-icons.css'],
                                    },
                                    {
                                        serie: true,
                                        name: 'Styles',
                                        files: ['/statics/assets/css/style.css'],
                                    },
                                    {
                                        serie: true,
                                        name: 'Custom Styles',
                                        files: ['/statics/assets/css/custom.css'],
                                    },
                                    {
                                        serie: true,
                                        name: 'ngTable Styles',
                                        files: ['/statics/libs/ngTable/ng-table.min.css'],
                                    },
                                    {
                                        serie: true,
                                        name: 'ngBlock Styles',
                                        files: ['/statics/libs/ngBlock/angular-block-ui.css'],
                                    },
                                ]);
                            },
                        ],
                    },
                })
                .state('print.documents', {
                    url: '/print',
                    template: '<ui-view></ui-view>',
                    abstract: true,
                    resolve: {
                        loadController: [
                            '$ocLazyLoad',
                            function ($ocLazyLoad) {
                                return $ocLazyLoad.load({
                                    files: ['/statics/scripts/angular-scripts/controllers/documents.js'],
                                });
                            },
                        ],
                    },
                })
                .state('print.documents.loan_release', {
                    url: '/files/:documentId',
                    templateUrl: '/statics/partials/pages/documents/documents-loan-release.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Loan Release Print',
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.documentId = $stateParams.documentId;
                        appFactory.getDocumentName($scope.documentId).then(function (data) {
                            $scope.fileName = data;
                        });
                    },
                });

            $urlRouterProvider.otherwise('/');
        },
    ]);
});
