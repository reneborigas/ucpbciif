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
                prefixStateName: 'app.dashboard',
                includeAbstract: true,
                // template: '<li class="breadcrumb-item" ng-repeat="step in steps" ng-class="{active: $last}" ng-switch="$last || !!step.abstract"><a ng-switch-when="false" href="{{step.ncyBreadcrumbLink}}">{{step.ncyBreadcrumbLabel}}</a><span ng-switch-when="true">{{step.ncyBreadcrumbLabel}}</span></li>'
                templateUrl: '/statics/partials/components/full/breadcrumb.html',
            });

            $locationProvider.html5Mode({
                enabled: true,
                requireBase: false,
            });

            $stateProvider
                .state('main', {
                    abstract: true,
                    templateUrl: '/statics/partials/layouts/metro.html',
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
                                    {
                                        serie: true,
                                        name: 'ngTag Styles',
                                        files: ['/statics/libs/ngTags/ng-tags-input.min.css'],
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
                    },
                })
                .state('main.menu', {
                    url: '/menu',
                    templateUrl: '/statics/partials/components/metro/metro-view.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Metro View',
                        stateTitle: 'Metro View',
                    },
                    ncyBreadcrumb: {
                        label: 'Home',
                    },
                    controller: function (appLoginService) {
                        appLoginService.setTitle = 'test';
                    },
                })
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
                                    {
                                        serie: true,
                                        name: 'ngTag Styles',
                                        files: ['/statics/libs/ngTags/ng-tags-input.min.css'],
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
                .state('app.dashboard', {
                    url: '/dashboard',
                    templateUrl: '/statics/partials/pages/dashboard/dashboard.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Dashboard',
                        stateTitle: 'Dashboard',
                    },
                    ncyBreadcrumb: {
                        label: 'Home',
                    },
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
                })

                .state('app.borrowers.create_loan_availment', {
                    url: '/:borrowerId/new-loan-availment/:creditLineId',
                    templateUrl: '/statics/partials/pages/borrowers/borrowers-new-loan-application.html',
                    data: {
                        pageTitle: 'UCPB CIIF | New Loan Availment',
                    },
                    ncyBreadcrumb: {
                        label: 'New {{subProcess.name}} File',
                        parent: 'app.borrowers.info',
                    },
                    resolve: {
                        fetchSubProcess: function ($stateParams, appFactory) {
                            return appFactory
                                .getSubProcessByName('Loan Availment')
                                .then(function (data) {
                                    
                                    return data;
                                    
                                });
                        },
                    },
                 
                    controller: function ($scope,fetchSubProcess,appFactory,$stateParams) {
                        console.log(fetchSubProcess);
                        $scope.borrowerId = $stateParams.borrowerId;
                        $scope.subProcessId = fetchSubProcess.id;
                        $scope.creditLineId = $stateParams.creditLineId;
                        console.log($scope.subProcessId);

                        appFactory.getBorrowerName($scope.borrowerId).then(function (data) {
                            $scope.borrowerName = data;
                        });

                        appFactory.getSubProcess($scope.subProcessId).then(function (data) {
                            $scope.subProcess = data;
                        });
                        console.log($stateParams.borrowerId);
                        console.log($stateParams);
                        appFactory.getCreditLine($scope.creditLineId).then(function (data) {
                            $scope.creditLine = data;
                        });
                        

                    },
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
                        label: '{{subProcessName}}',
                    },
                    resolve: {
                        fetchSubProcess: function ($stateParams, appFactory) {
                            return appFactory
                                .getSubProcessByName(appFactory.unSlugify($stateParams.subProcessName))
                                .then(function (data) {
                                    return data;
                                });
                        },
                    },
                    controller: function ($scope, fetchSubProcess) {
                        $scope.subProcessId = fetchSubProcess.id;
                        $scope.subProcessName = fetchSubProcess.name;
                        
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
                .state('app.loans', {
                    url: '/loans',
                    template: '<ui-view></ui-view>',
                    abstract: true,
                    ncyBreadcrumb: {
                        label: 'Loans',
                        skip: true,
                    },
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
                    data: {
                        pageTitle: 'UCPB CIIF | Loans List',
                        stateTitle: 'Loans',
                    },
                    ncyBreadcrumb: {
                        label: 'Loans',
                    },
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
                .state('app.loans.info', {
                    url: '/:loanId',
                    templateUrl: '/statics/partials/pages/loans/loans-info.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Loan Info',
                    },
                    ncyBreadcrumb: {
                        label: 'Loan No. {{loanId}}',
                        parent: 'app.loans.list',
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.loanId = $stateParams.loanId;
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
                .state('app.payments', {
                    url: '/payments',
                    template: '<ui-view></ui-view>',
                    abstract: true,
                    ncyBreadcrumb: {
                        label: 'Payments',
                        skip: true,
                    },
                    resolve: {
                        loadController: [
                            '$ocLazyLoad',
                            function ($ocLazyLoad) {
                                return $ocLazyLoad.load({
                                    files: ['/statics/scripts/angular-scripts/controllers/payments.js'],
                                });
                            },
                        ],
                    },
                })
                .state('app.payments.list', {
                    url: '',
                    templateUrl: '/statics/partials/pages/payments/payments-list.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Payments List',
                        stateTitle: 'Payments',
                    },
                    ncyBreadcrumb: {
                        label: 'Payments',
                    },
                })
                .state('app.payments.new', {
                    url: '/:loanId',
                    templateUrl: '/statics/partials/pages/payments/payments-new.html',
                    data: {
                        pageTitle: 'UCPB CIIF | New Payment',
                    },
                    ncyBreadcrumb: {
                        label: 'New Payment',
                        parent: 'app.loans.info',
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.loanId = $stateParams.loanId;
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
                                    {
                                        serie: true,
                                        name: 'ngTag Styles',
                                        files: ['/statics/libs/ngTags/ng-tags-input.min.css'],
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
                                        name: 'ngTable Styles',
                                        files: ['/statics/libs/ngTable/ng-table.min.css'],
                                    },
                                    {
                                        serie: true,
                                        name: 'ngBlock Styles',
                                        files: ['/statics/libs/ngBlock/angular-block-ui.css'],
                                    },
                                    {
                                        serie: true,
                                        name: 'ngTag Styles',
                                        files: ['/statics/libs/ngTags/ng-tags-input.min.css'],
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
                                    files: ['/statics/scripts/angular-scripts/controllers/loans.js'],
                                });
                            },
                        ],
                    },
                })
                .state('print.documents.borrower_outstanding_obligations', {
                    url: '/borrowers/outstanding-obligations/:borrowerId',
                    templateUrl: '/statics/partials/pages/borrowers/print/borrowers-outstanding-obligation.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Borrower Outstanding Obligations Print',
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.borrowerId = $stateParams.borrowerId;
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
                .state('print.documents.borrower_loans', {
                    url: '/borrowers/loans/:borrowerId',
                    templateUrl: '/statics/partials/pages/borrowers/print/borrowers-existing-loans.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Borrower Loans Print',
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.borrowerId = $stateParams.borrowerId;
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
                .state('print.documents.borrower_credit_lines', {
                    url: '/borrowers/creditlines/:borrowerId',
                    templateUrl: '/statics/partials/pages/borrowers/print/borrowers-existing-credit-lines.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Borrower Credit Lines Print',
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.borrowerId = $stateParams.borrowerId;
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
                .state('print.documents.borrower_payment_history', {
                    url: '/borrowers/payment-history/:borrowerId',
                    templateUrl: '/statics/partials/pages/borrowers/print/borrowers-payment-history.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Borrower Payment History Print',
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.borrowerId = $stateParams.borrowerId;
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
                .state('print.documents.loan_release', {
                    url: '/files/:loanId',
                    templateUrl: '/statics/partials/pages/documents/print/documents-loan-release.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Loan Release Print',
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.loanId = $stateParams.loanId;
                        // appFactory.getDocumentName($scope.documentId).then(function (data) {
                        //     $scope.fileName = data;
                        // });
                    },
                })
                .state('print.documents.amortization_schedule', {
                    url: '/files/amortization/:documentId',
                    templateUrl: '/statics/partials/pages/documents/print/documents-amortization-schedule.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Amortization Schedule Print',
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.documentId = $stateParams.documentId;
                        appFactory.getDocumentName($scope.documentId).then(function (data) {
                            $scope.fileName = data;
                        });
                    },
                })
                .state('print.documents.amortization_history', {
                    url: '/loans/amortization-history/:loanId',
                    templateUrl: '/statics/partials/pages/loans/print/loans-amortization-history.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Amortization History Print',
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.loanId = $stateParams.loanId;
                    },
                })
                .state('print.documents.payment_history', {
                    url: '/loans/payment-history/:loanId',
                    templateUrl: '/statics/partials/pages/loans/print/loans-payment-history.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Amortization History Print',
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.loanId = $stateParams.loanId;
                    },
                })
                .state('print.documents.check_release', {
                    url: '/loans/check/:loanId',
                    templateUrl: '/statics/partials/pages/loans/print/loans-check-release.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Check Release Print',
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.loanId = $stateParams.loanId;
                    },
                });

            $urlRouterProvider.otherwise('/');
        },
    ]);
});
