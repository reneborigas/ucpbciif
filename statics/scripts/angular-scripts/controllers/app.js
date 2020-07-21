define(function () {
    'use strict';

    var app = angular.module('app');

    app.controller('NavBarController', function NavBarController($scope, appFactory, appLoginService, $state) {
        appFactory.getCurrentUserInfo().then(function (data) {
            $scope.user = data;
        });
        $scope.gotToMetro = function () {
            $state.go('main.menu');
        };
        $scope.logout = appLoginService.logout;
        $scope.showHeader = false;
        $scope.showHeader = appLoginService.isLoggedIn();
    });

    app.controller('FooterController', function FooterController($scope) {
        $scope.date = new Date();
    });

    app.controller('SideBarController', function SideBarController(
        $http,
        $scope,
        toastr,
        $state,
        $timeout,
        appFactory
    ) {
        $http.get('/api/processes/subprocesses/').then(
            function (response) {
                $scope.subProcesses = response.data;
                $scope.subProcessSlugs = [];
                angular.forEach($scope.subProcesses, function (subProcess) {
                    $scope.subProcessSlugs.push({
                        name: subProcess.name,
                        slug: appFactory.slugify(subProcess.name),
                    });
                });
            },
            function (error) {
                toastr.error(
                    'Error ' + error.status + error.statusText,
                    'Could not retrieve Sub Processes. Please contact System Administrator.'
                );
            }
        );
    });

    app.controller('MetroController', function MetroController($scope, $state) {
        $scope.goToLMS = function () {
            $state.go('app.dashboard');
        };
    });
});
