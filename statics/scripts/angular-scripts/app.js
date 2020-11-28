define(function () {
    'use strict';

    var app = angular.module('app', [
        'ui.router',
        'oc.lazyLoad',
        'ncy-angular-breadcrumb',
        'angular-loading-bar',
        'toastr',
        'ngTable',
        'oitozero.ngSweetAlert',
        'blockUI',
        'ngTagsInput',
        'ngAnimate',
        'ngTouch',
        'ui.bootstrap',
        'ngIdle',
        'zingchart-angularjs',
        'angularMoment',
        'daterangepicker',
    ]);

    app.config([
        'cfpLoadingBarProvider',
        'blockUIConfig',
        'IdleProvider',
        'KeepaliveProvider',
        function (cfpLoadingBarProvider, blockUIConfig, IdleProvider, KeepaliveProvider) {
            cfpLoadingBarProvider.includeSpinner = false;
            cfpLoadingBarProvider.latencyThreshold = 1;

            blockUIConfig.autoBlock = false;
            blockUIConfig.templateUrl = 'statics/partials/customs/blockui.html';

            IdleProvider.idle(90000);
            IdleProvider.timeout(30);
            IdleProvider.autoResume('notIdle');
            // KeepaliveProvider.interval(10);
        },
    ]);

    app.run([
        '$rootScope',
        '$state',
        '$stateParams',
        '$http',
        'appLoginService',
        '$transitions',
        '$uibModal',
        '$uibModalStack',
        'Idle',
        '$q',
        function ($rootScope, $state, $stateParams, $http, appLoginService, $transitions, $uibModal, $uibModalStack, Idle, $q) {
            $http.defaults.xsrfHeaderName = 'X-CSRFToken';
            $http.defaults.xsrfCookieName = 'csrftoken';

            $transitions.onBefore({}, function (transition) {
                return appLoginService.isLoggedIn().then(function (data) {
                    if (transition.to().name !== 'simple.login' && !data) {
                        return transition.router.stateService.target('simple.login');
                    }
                    if (transition.to().name == 'simple.login' && data) {
                        return transition.router.stateService.target('main.menu');
                    }
                });
            });

            $transitions.onError({}, function (transition) {
                if (transition.error().detail === 'Unauthenticated') {
                    $state.go('simple.login');
                }
                if (transition.error().detail === 'Unauthorized') {
                    $state.go('app.unauthorized');
                }
                if (transition.error().detail === 'Not Found') {
                    $state.go('app.404');
                }
            });

            Idle.watch();
            var warningInstance;
            var timeoutInstance;

            // The user starts to go idle
            $rootScope.$on('IdleStart', function () {
                warningInstance = $uibModal
                    .open({
                        backdrop: 'static',
                        templateUrl: '/statics/partials/customs/warning-dialog.html',
                        size: 'md',
                        windowClass: 'uib-modal fade show',
                        controller: function ($scope, $uibModalInstance) {
                            $scope.continue = function () {
                                Idle.watch();
                                $uibModalInstance.close();
                            };

                            $scope.logout = function () {
                                $uibModalInstance.dismiss('Logout');
                            };
                        },
                    })
                    .result.then(
                        function () {
                            console.log('Success');
                        },
                        function (response) {
                            console.log(response);
                        }
                    );
            });

            // Follows after IdleStart event.
            $rootScope.$on('IdleWarn', function (e, countdown) {
                $rootScope.startValue = countdown;
                $rootScope.$apply(function () {
                    $rootScope.idleTimeRemaining = countdown;
                });
            });

            // The user has timed out and needs to be logged out
            $rootScope.$on('IdleTimeout', function () {
                $uibModalStack.dismissAll('cancel');
                timeoutInstance = $uibModal
                    .open({
                        backdrop: 'static',
                        templateUrl: '/statics/partials/customs/timeout-dialog.html',
                        size: 'md',
                        windowClass: 'uib-modal fade show',
                        controller: function ($scope, $uibModalInstance) {
                            $scope.relogin = function () {
                                $uibModalInstance.close();
                            };
                        },
                    })
                    .result.then(
                        function () {
                            console.log('Success');
                        },
                        function (response) {
                            console.log(response);
                        }
                    );
            });

            $rootScope.$state = $state;
            return ($rootScope.$stateParams = $stateParams);
        },
    ]);
});
