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
            IdleProvider.timeout(10);
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
        'Idle',
        function ($rootScope, $state, $stateParams, $http, appLoginService, $transitions, $uibModal, Idle) {
            $http.defaults.xsrfHeaderName = 'X-CSRFToken';
            $http.defaults.xsrfCookieName = 'csrftoken';

            $transitions.onBefore({}, function (transition) {
                if (transition.to().name !== 'simple.login' && !appLoginService.isLoggedIn()) {
                    return transition.router.stateService.target('simple.login');
                }
                if (transition.to().name == 'simple.login' && appLoginService.isLoggedIn()) {
                    return transition.router.stateService.target('main.menu');
                }
            });

            $transitions.onError({}, function (transition) {
                if (transition.error().detail === 'Unauthorized') {
                    $state.go('app.unauthorized');
                }
                if (transition.error().detail === 'Not Found') {
                    $state.go('app.404');
                }
            });

            Idle.watch();
            var warningInstance;
            $rootScope.$on('IdleStart', function (e, countdown) {
                warningInstance = $uibModal
                    .open({
                        animation: true,
                        backdrop: 'static',
                        templateUrl: '/statics/partials/customs/warning-dialog.html',
                        size: 'md',
                        windowClass: 'uib-modal',
                        controller: function ($scope) {
                            $scope.name = 'bottom';
                        },
                    })
                    .closed.then(function () {
                        window.alert('Modal closed');
                    });
            });

            $rootScope.$on('IdleWarn', function (e, countdown) {
                $rootScope.startValue = countdown;
                $rootScope.$apply(function () {
                    $rootScope.idleTimeRemaining = countdown;
                });

                console.log($rootScope.idleTimeRemaining);
            });

            $rootScope.$on('IdleEnd', function () {
                warningInstance.dismiss();
            });

            $rootScope.$on('IdleTimeout', function () {
                /* Logout user */
            });

            $rootScope.$state = $state;
            return ($rootScope.$stateParams = $stateParams);
        },
    ]);
});
