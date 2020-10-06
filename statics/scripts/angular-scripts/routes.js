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
                        stateTitle: 'Main Menu',
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
                                        name: 'Scheduler Styles',
                                        files: ['/statics/libs/fullcalendar/fullcalendar.min.css'],
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
                .state('app.unauthorized', {
                    url: '/unauthorized',
                    templateUrl: '/statics/partials/pages/dashboard/unauthorized.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Unauthorized Access',
                        stateTitle: 'Unauthorized',
                    },
                    ncyBreadcrumb: {
                        label: 'Unauthorized Access',
                    },
                    resolve: {
                        previousState: function ($state) {
                            var currentStateData = {
                                name: $state.current.name,
                                params: $state.params,
                                url: $state.href($state.current.name, $state.params),
                            };
                            return currentStateData;
                        },
                    },
                    controller: function (previousState, $scope) {
                        $scope.previousState = previousState;
                    },
                })
                .state('app.404', {
                    url: '/404',
                    templateUrl: '/statics/partials/pages/dashboard/404.html',
                    data: {
                        pageTitle: 'UCPB CIIF | 404 Not Found',
                        stateTitle: '404 Not Found',
                    },
                    ncyBreadcrumb: {
                        label: '404 Not Found',
                    },
                    resolve: {
                        previousState: function ($state) {
                            var currentStateData = {
                                name: $state.current.name,
                                params: $state.params,
                                url: $state.href($state.current.name, $state.params),
                            };
                            return currentStateData;
                        },
                    },
                    controller: function (previousState, $scope) {
                        $scope.previousState = previousState;
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
                    resolve: {
                        loadController: [
                            '$ocLazyLoad',
                            function ($ocLazyLoad) {
                                return $ocLazyLoad.load({
                                    files: ['/statics/scripts/angular-scripts/controllers/dashboard.js'],
                                });
                            },
                        ],
                    },
                })

                // Loan Management
                .state('app.borrowers', {
                    url: '/borrowers',
                    template: '<ui-view></ui-view>',
                    abstract: true,
                    ncyBreadcrumb: {
                        label: 'Borrowers',
                        skip: true,
                    },
                    resolve: {
                        fetchRouteAppPermission: function ($http, $q, appFactory) {
                            return appFactory.getCurrentUserAppPermission('Loan Management System').then(function (data) {
                                if (data.length == 0) {
                                    var appInfo = {
                                        name: '',
                                        navBar: '',
                                    };
                                    localStorage.selectedApp = JSON.stringify(appInfo);
                                    return $q.reject('Not Found');
                                } else {
                                    var appInfo = {
                                        name: data[0].name,
                                        navBar: data[0].navDirectory,
                                    };
                                    return (localStorage.selectedApp = JSON.stringify(appInfo));
                                }
                            });
                        },
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
                    resolve: {
                        fetchBorrower: function ($http, $q, $stateParams) {
                            return $http
                                .get('/api/borrowers/borrowers/', { params: { borrowerId: $stateParams.borrowerId } })
                                .then(function (response) {
                                    if (response.data.length == 0) {
                                        return $q.reject('Not Found');
                                    }
                                });
                        },
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
                    resolve: {
                        fetchBorrower: function ($http, $q, $stateParams) {
                            return $http
                                .get('/api/borrowers/borrowers/', { params: { borrowerId: $stateParams.borrowerId } })
                                .then(function (response) {
                                    if (response.data.length == 0) {
                                        return $q.reject('Not Found');
                                    }
                                });
                        },
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.borrowerId = $stateParams.borrowerId;
                        appFactory.getBorrowerName($scope.borrowerId).then(function (data) {
                            $scope.borrowerName = data;
                        });
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
                    resolve: {
                        fetchBorrower: function ($http, $q, $stateParams) {
                            return $http
                                .get('/api/borrowers/borrowers/', { params: { borrowerId: $stateParams.borrowerId } })
                                .then(function (response) {
                                    if (response.data.length == 0) {
                                        return $q.reject('Not Found');
                                    }
                                });
                        },
                        fetchSubProcess: function ($http, $q, $stateParams) {
                            return $http
                                .get('/api/processes/subprocesses/', {
                                    params: { subProcessId: $stateParams.subProcessId },
                                })
                                .then(function (response) {
                                    if (response.data.length == 0) {
                                        return $q.reject('Not Found');
                                    }
                                });
                        },
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
                        fetchBorrower: function ($http, $q, $stateParams) {
                            return $http
                                .get('/api/borrowers/borrowers/', { params: { borrowerId: $stateParams.borrowerId } })
                                .then(function (response) {
                                    if (response.data.length == 0) {
                                        return $q.reject('Not Found');
                                    }
                                });
                        },
                        fetchCreditLine: function ($http, $q, $stateParams) {
                            return $http
                                .get('/api/loans/creditlines/', {
                                    params: { creditLineId: $stateParams.creditLineId },
                                })
                                .then(function (response) {
                                    if (response.data.length == 0) {
                                        return $q.reject('Not Found');
                                    }
                                });
                        },
                        fetchSubProcess: function ($stateParams, appFactory) {
                            return appFactory.getSubProcessByName('Loan Availment').then(function (data) {
                                return data;
                            });
                        },
                    },
                    controller: function ($scope, fetchSubProcess, appFactory, $stateParams) {
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
                .state('app.borrowers.create_loan_release', {
                    url: '/:borrowerId/new-loan-release/:loanId',
                    templateUrl: '/statics/partials/pages/borrowers/borrowers-new-loan-application.html',
                    data: {
                        pageTitle: 'UCPB CIIF | New Loan Release',
                    },
                    ncyBreadcrumb: {
                        label: 'New {{subProcess.name}} File',
                        parent: 'app.borrowers.info',
                    },
                    resolve: {
                        fetchBorrower: function ($http, $q, $stateParams) {
                            return $http
                                .get('/api/borrowers/borrowers/', { params: { borrowerId: $stateParams.borrowerId } })
                                .then(function (response) {
                                    if (response.data.length == 0) {
                                        return $q.reject('Not Found');
                                    }
                                });
                        },
                        fetchLoan: function ($http, $q, $stateParams) {
                            return $http.get('/api/loans/loans/', { params: { loanId: $stateParams.loanId } }).then(function (response) {
                                if (response.data.length == 0) {
                                    return $q.reject('Not Found');
                                }
                            });
                        },
                        fetchSubProcess: function ($stateParams, appFactory) {
                            return appFactory.getSubProcessByName('Loan Release').then(function (data) {
                                return data;
                            });
                        },
                    },
                    controller: function ($scope, fetchSubProcess, appFactory, $stateParams) {
                        console.log(fetchSubProcess);
                        $scope.borrowerId = $stateParams.borrowerId;
                        $scope.subProcessId = fetchSubProcess.id;
                        $scope.loanId = $stateParams.loanId;
                        console.log($scope.subProcessId);

                        appFactory.getBorrowerName($scope.borrowerId).then(function (data) {
                            $scope.borrowerName = data;
                        });

                        appFactory.getSubProcess($scope.subProcessId).then(function (data) {
                            $scope.subProcess = data;
                        });
                        console.log($stateParams.borrowerId);
                        console.log($stateParams);
                        appFactory.getLoan($scope.loanId).then(function (data) {
                            $scope.loan = data;
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
                        fetchRouteAppPermission: function ($http, $q, appFactory) {
                            return appFactory.getCurrentUserAppPermission('Loan Management System').then(function (data) {
                                if (data.length == 0) {
                                    var appInfo = {
                                        name: '',
                                        navBar: '',
                                    };
                                    localStorage.selectedApp = JSON.stringify(appInfo);
                                    return $q.reject('Not Found');
                                } else {
                                    var appInfo = {
                                        name: data[0].name,
                                        navBar: data[0].navDirectory,
                                    };
                                    return (localStorage.selectedApp = JSON.stringify(appInfo));
                                }
                            });
                        },
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
                        pageTitle: 'UCPB CIIF | Credit Management',
                    },
                    ncyBreadcrumb: {
                        label: '{{subProcessName}}',
                    },
                    resolve: {
                        fetchSubProcess: function ($q, $stateParams, appFactory) {
                            return appFactory.getSubProcessByName(appFactory.unSlugify($stateParams.subProcessName)).then(function (data) {
                                if (!data) {
                                    return $q.reject('Not Found');
                                }
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
                    resolve: {
                        fetchDocumentFound: function ($http, $q, $stateParams) {
                            return $http
                                .get('/api/documents/documents/', { params: { documentId: $stateParams.documentId } })
                                .then(function (response) {
                                    if (response.data.length == 0) {
                                        return $q.reject('Not Found');
                                    }
                                });
                        },
                        fetchSubProcess: function ($q, $stateParams, appFactory) {
                            return appFactory.getSubProcessByName(appFactory.unSlugify($stateParams.subProcessName)).then(function (data) {
                                if (!data) {
                                    return $q.reject('Not Found');
                                }
                                return data;
                            });
                        },
                        fetchPermission: function (fetchSubProcess, appFactory, $q, $state) {
                            return appFactory.checkPermissions(fetchSubProcess.id).then(function (data) {
                                if (!data.permission) {
                                    return $q.reject('Unauthorized');
                                }
                            });
                        },
                    },
                    controller: function ($scope, $stateParams, appFactory, fetchSubProcess, fetchPermission, $state) {
                        $scope.subProcessName = fetchSubProcess.name;
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
                        fetchRouteAppPermission: function ($http, $q, appFactory) {
                            return appFactory.getCurrentUserAppPermission('Loan Management System').then(function (data) {
                                if (data.length == 0) {
                                    var appInfo = {
                                        name: '',
                                        navBar: '',
                                    };
                                    localStorage.selectedApp = JSON.stringify(appInfo);
                                    return $q.reject('Not Found');
                                } else {
                                    var appInfo = {
                                        name: data[0].name,
                                        navBar: data[0].navDirectory,
                                    };
                                    return (localStorage.selectedApp = JSON.stringify(appInfo));
                                }
                            });
                        },
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
                    resolve: {
                        fetchLoan: function ($http, $q, $stateParams) {
                            return $http.get('/api/loans/loans/', { params: { loanId: $stateParams.loanId } }).then(function (response) {
                                if (response.data.length == 0) {
                                    return $q.reject('Not Found');
                                }
                            });
                        },
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.loanId = $stateParams.loanId;
                    },
                })
                .state('app.loans.restructeamortization', {
                    url: '/:loanId/amortization/restructure',
                    templateUrl: '/statics/partials/pages/loans/loans-amortization-restructure.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Restructure Amortization Schedule',
                    },
                    ncyBreadcrumb: {
                        label: 'Restructure Amortization Schedule',
                        parent: 'app.loans.info',
                    },
                    resolve: {
                        fetchLoan: function ($http, $q, $stateParams) {
                            return $http.get('/api/loans/loans/', { params: { loanId: $stateParams.loanId } }).then(function (response) {
                                if (response.data.length == 0) {
                                    return $q.reject('Not Found');
                                }
                            });
                        },
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
                        fetchRouteAppPermission: function ($http, $q, appFactory) {
                            return appFactory.getCurrentUserAppPermission('Loan Management System').then(function (data) {
                                if (data.length == 0) {
                                    var appInfo = {
                                        name: '',
                                        navBar: '',
                                    };
                                    localStorage.selectedApp = JSON.stringify(appInfo);
                                    return $q.reject('Not Found');
                                } else {
                                    var appInfo = {
                                        name: data[0].name,
                                        navBar: data[0].navDirectory,
                                    };
                                    return (localStorage.selectedApp = JSON.stringify(appInfo));
                                }
                            });
                        },
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
                    resolve: {
                        fetchLoan: function ($http, $q, $stateParams) {
                            return $http.get('/api/loans/loans/', { params: { loanId: $stateParams.loanId } }).then(function (response) {
                                if (response.data.length == 0) {
                                    return $q.reject('Not Found');
                                }
                            });
                        },
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.loanId = $stateParams.loanId;
                    },
                })
                .state('app.payments.add', {
                    url: '/new',
                    templateUrl: '/statics/partials/pages/payments/payments-add.html',
                    data: {
                        pageTitle: 'UCPB CIIF | New Payment',
                    },
                    ncyBreadcrumb: {
                        label: 'Add Payment',
                        parent: 'app.payments.list',
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.loanId = $stateParams.loanId;
                    },
                })
                .state('app.creditline', {
                    url: '/credit-line',
                    template: '<ui-view></ui-view>',
                    abstract: true,
                    ncyBreadcrumb: {
                        label: 'Credit Line',
                        skip: true,
                    },
                    resolve: {
                        fetchRouteAppPermission: function ($http, $q, appFactory) {
                            return appFactory.getCurrentUserAppPermission('Loan Management System').then(function (data) {
                                if (data.length == 0) {
                                    var appInfo = {
                                        name: '',
                                        navBar: '',
                                    };
                                    localStorage.selectedApp = JSON.stringify(appInfo);
                                    return $q.reject('Not Found');
                                } else {
                                    var appInfo = {
                                        name: data[0].name,
                                        navBar: data[0].navDirectory,
                                    };
                                    return (localStorage.selectedApp = JSON.stringify(appInfo));
                                }
                            });
                        },
                        loadController: [
                            '$ocLazyLoad',
                            function ($ocLazyLoad) {
                                return $ocLazyLoad.load({
                                    files: ['/statics/scripts/angular-scripts/controllers/creditline.js'],
                                });
                            },
                        ],
                    },
                })
                .state('app.creditline.list', {
                    url: '',
                    templateUrl: '/statics/partials/pages/creditline/creditline-list.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Credit Line List',
                        stateTitle: 'Credit Line',
                    },
                    ncyBreadcrumb: {
                        label: 'Credit Line',
                    },
                })
                .state('app.creditline.info', {
                    url: '/:creditLineId',
                    templateUrl: '/statics/partials/pages/creditline/creditline-info.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Credit Line Info',
                    },
                    ncyBreadcrumb: {
                        label: 'Credit Line No. {{creditLineId}}',
                        parent: 'app.creditline.list',
                    },
                    resolve: {
                        fetchLoan: function ($http, $q, $stateParams) {
                            return $http
                                .get('/api/loans/creditlines/', { params: { creditLineId: $stateParams.creditLineId } })
                                .then(function (response) {
                                    if (response.data.length == 0) {
                                        return $q.reject('Not Found');
                                    }
                                });
                        },
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.creditLineId = $stateParams.creditLineId;
                    },
                })
                .state('app.amortizations', {
                    url: '/amortizations',
                    template: '<ui-view></ui-view>',
                    abstract: true,
                    ncyBreadcrumb: {
                        label: 'Amortizations',
                        skip: true,
                    },
                    resolve: {
                        fetchRouteAppPermission: function ($http, $q, appFactory) {
                            return appFactory.getCurrentUserAppPermission('Loan Management System').then(function (data) {
                                if (data.length == 0) {
                                    var appInfo = {
                                        name: '',
                                        navBar: '',
                                    };
                                    localStorage.selectedApp = JSON.stringify(appInfo);
                                    return $q.reject('Not Found');
                                } else {
                                    var appInfo = {
                                        name: data[0].name,
                                        navBar: data[0].navDirectory,
                                    };
                                    return (localStorage.selectedApp = JSON.stringify(appInfo));
                                }
                            });
                        },
                        loadController: [
                            '$ocLazyLoad',
                            function ($ocLazyLoad) {
                                return $ocLazyLoad.load({
                                    files: ['/statics/scripts/angular-scripts/controllers/amortizations.js'],
                                });
                            },
                        ],
                    },
                })
                .state('app.amortizations.maturing', {
                    url: '/maturing',
                    templateUrl: '/statics/partials/pages/amortizations/amortizations-maturing-list.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Maturing Amortization List',
                        stateTitle: 'Amortization',
                    },
                    ncyBreadcrumb: {
                        label: 'Maturing Amortizations',
                    },
                })
                .state('app.amortizations.list', {
                    url: '',
                    templateUrl: '/statics/partials/pages/amortizations/amortizations-list.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Amortization Schedule',
                        stateTitle: 'Amortization',
                    },
                    ncyBreadcrumb: {
                        label: 'Amortizations',
                    },
                })
                .state('app.lms-reports', {
                    url: '/loan-reports',
                    template: '<ui-view></ui-view>',
                    abstract: true,
                    ncyBreadcrumb: {
                        label: 'Reports',
                        skip: true,
                    },
                    resolve: {
                        fetchRouteAppPermission: function ($http, $q, appFactory) {
                            return appFactory.getCurrentUserAppPermission('Loan Management System').then(function (data) {
                                if (data.length == 0) {
                                    var appInfo = {
                                        name: '',
                                        navBar: '',
                                    };
                                    localStorage.selectedApp = JSON.stringify(appInfo);
                                    return $q.reject('Not Found');
                                } else {
                                    var appInfo = {
                                        name: data[0].name,
                                        navBar: data[0].navDirectory,
                                    };
                                    return (localStorage.selectedApp = JSON.stringify(appInfo));
                                }
                            });
                        },
                        loadController: [
                            '$ocLazyLoad',
                            function ($ocLazyLoad) {
                                return $ocLazyLoad.load({
                                    files: ['/statics/scripts/angular-scripts/controllers/reports.js'],
                                });
                            },
                        ],
                    },
                })
                .state('app.lms-reports.list', {
                    url: '',
                    templateUrl: '/statics/partials/pages/reports/lms/reports-list.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Loan Reports',
                        stateTitle: 'Loan Reports',
                    },
                    ncyBreadcrumb: {
                        label: 'Loan Reports',
                    },
                })

                //Accounting
                .state('app.invoices', {
                    url: '/invoices',
                    template: '<ui-view></ui-view>',
                    abstract: true,
                    ncyBreadcrumb: {
                        label: 'Invoices',
                        skip: true,
                    },
                    resolve: {
                        fetchRouteAppPermission: function ($http, $q, appFactory) {
                            return appFactory.getCurrentUserAppPermission('Accounting System').then(function (data) {
                                if (data.length == 0) {
                                    var appInfo = {
                                        name: '',
                                        navBar: '',
                                    };
                                    localStorage.selectedApp = JSON.stringify(appInfo);
                                    return $q.reject('Not Found');
                                } else {
                                    var appInfo = {
                                        name: data[0].name,
                                        navBar: data[0].navDirectory,
                                    };
                                    return (localStorage.selectedApp = JSON.stringify(appInfo));
                                }
                            });
                        },
                        loadController: [
                            '$ocLazyLoad',
                            function ($ocLazyLoad) {
                                return $ocLazyLoad.load({
                                    files: ['/statics/scripts/angular-scripts/controllers/transactions.js'],
                                });
                            },
                        ],
                    },
                })
                .state('app.invoices.list', {
                    url: '',
                    templateUrl: '/statics/partials/pages/sales/invoices-list.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Invoices List',
                        stateTitle: 'Invoices',
                    },
                    ncyBreadcrumb: {
                        label: 'Invoices',
                    },
                })
                .state('app.invoices.info', {
                    url: '/:transactionId',
                    templateUrl: '/statics/partials/pages/sales/invoices-info.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Borrower Info',
                    },
                    ncyBreadcrumb: {
                        label: '{{ transactionNumber }}',
                        parent: 'app.invoices.list',
                    },
                    resolve: {
                        fetchTransaction: function ($http, $q, $stateParams) {
                            return $http
                                .get('/api/borrowers/borrowers/', { params: { borrowerId: $stateParams.borrowerId } })
                                .then(function (response) {
                                    if (response.data.length == 0) {
                                        return $q.reject('Not Found');
                                    }
                                });
                        },
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.borrowerId = $stateParams.borrowerId;
                        appFactory.getBorrowerName($scope.borrowerId).then(function (data) {
                            $scope.borrowerName = data;
                        });
                    },
                })

                // Settings
                .state('app.terms', {
                    url: '/terms',
                    template: '<ui-view></ui-view>',
                    abstract: true,
                    ncyBreadcrumb: {
                        label: 'Terms',
                        skip: true,
                    },
                    resolve: {
                        fetchRouteAppPermission: function ($http, $q, appFactory) {
                            return appFactory.getCurrentUserAppPermission('Settings').then(function (data) {
                                if (data.length == 0) {
                                    var appInfo = {
                                        name: '',
                                        navBar: '',
                                    };
                                    localStorage.selectedApp = JSON.stringify(appInfo);
                                    return $q.reject('Not Found');
                                } else {
                                    var appInfo = {
                                        name: data[0].name,
                                        navBar: data[0].navDirectory,
                                    };
                                    return (localStorage.selectedApp = JSON.stringify(appInfo));
                                }
                            });
                        },
                        loadController: [
                            '$ocLazyLoad',
                            function ($ocLazyLoad) {
                                return $ocLazyLoad.load({
                                    files: ['/statics/scripts/angular-scripts/controllers/terms.js'],
                                });
                            },
                        ],
                    },
                })
                .state('app.terms.list', {
                    url: '',
                    templateUrl: '/statics/partials/pages/terms/terms-list.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Terms List',
                        stateTitle: 'Terms',
                    },
                    ncyBreadcrumb: {
                        label: 'Terms',
                    },
                })
                .state('app.terms.add', {
                    url: '/add',
                    templateUrl: '/statics/partials/pages/terms/terms-add.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Add Terms',
                    },
                    ncyBreadcrumb: {
                        label: 'Add',
                        parent: 'app.terms.list',
                    },
                })
                .state('app.terms.info', {
                    url: '/:termId',
                    templateUrl: '/statics/partials/pages/terms/terms-info.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Terms Info',
                    },
                    ncyBreadcrumb: {
                        label: '{{ termName }}',
                        parent: 'app.terms.list',
                    },
                    resolve: {
                        fetchTerm: function ($http, $q, $stateParams) {
                            return $http.get('/api/loans/terms/', { params: { termId: $stateParams.termId } }).then(function (response) {
                                if (response.data.length == 0) {
                                    return $q.reject('Not Found');
                                }
                            });
                        },
                    },
                    controller: function ($scope, $stateParams, appFactory) {
                        $scope.termId = $stateParams.termId;
                        appFactory.getTermName($scope.termId).then(function (data) {
                            $scope.termName = data;
                        });
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
                        fetchRouteAppPermission: function ($http, $q, appFactory) {
                            return appFactory.getCurrentUserAppPermission('Settings').then(function (data) {
                                if (data.length == 0) {
                                    var appInfo = {
                                        name: '',
                                        navBar: '',
                                    };
                                    localStorage.selectedApp = JSON.stringify(appInfo);
                                    return $q.reject('Not Found');
                                } else {
                                    var appInfo = {
                                        name: data[0].name,
                                        navBar: data[0].navDirectory,
                                    };
                                    return (localStorage.selectedApp = JSON.stringify(appInfo));
                                }
                            });
                        },
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
                        pageTitle: 'UCPB CIIF | Offices List',
                        stateTitle: 'Offices',
                    },
                    ncyBreadcrumb: {
                        label: 'Offices',
                    },
                })
                .state('app.committees.add_office', {
                    url: '/add',
                    templateUrl: '/statics/partials/pages/committees/committees-offices-add.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Offices Add',
                        stateTitle: 'Offices Add',
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
                        pageTitle: 'UCPB CIIF | Offices Info',
                    },
                    ncyBreadcrumb: {
                        label: '{{ officeName }}',
                        parent: 'app.committees.offices',
                    },
                    resolve: {
                        fetchOfficeName: function ($http, $q, $stateParams, appFactory) {
                            return $http
                                .get('/api/committees/offices/', {
                                    params: { officeName: appFactory.unSlugify($stateParams.officeName) },
                                })
                                .then(function (response) {
                                    if (response.data.length == 0) {
                                        return $q.reject('Not Found');
                                    }
                                });
                        },
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
                    resolve: {
                        fetchOfficeName: function ($http, $q, $stateParams, appFactory) {
                            return $http
                                .get('/api/committees/offices/', {
                                    params: { officeName: appFactory.unSlugify($stateParams.officeName) },
                                })
                                .then(function (response) {
                                    if (response.data.length == 0) {
                                        return $q.reject('Not Found');
                                    }
                                });
                        },
                        fetchCommitteeId: function ($http, $q, $stateParams, appFactory) {
                            return $http
                                .get('/api/committees/committees/', {
                                    params: { committeeId: $stateParams.committeeId },
                                })
                                .then(function (response) {
                                    if (response.data.length == 0) {
                                        return $q.reject('Not Found');
                                    }
                                });
                        },
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
                })
                .state('print.documents.datatable', {
                    url: '/:state',
                    templateUrl: '/statics/partials/pages/print/datatable-dynamic-print.html',
                    data: {
                        pageTitle: 'UCPB CIIF | Print',
                    },
                    params: {
                        headers: '',
                        cellValues: '',
                    },
                    controller: function ($scope, $stateParams, appFactory, $state) {},
                    resolve: {
                        loadController: [
                            '$ocLazyLoad',
                            function ($ocLazyLoad) {
                                return $ocLazyLoad.load({
                                    files: ['/statics/scripts/angular-scripts/controllers/print.js'],
                                });
                            },
                        ],
                    },
                });

            $urlRouterProvider.otherwise('/');
        },
    ]);
});
