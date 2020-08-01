define(function () {
    'use strict';

    var app = angular.module('app');

    app.controller('DynamicPrintController', function DynamicPrintController(
        $http,
        $filter,
        $scope,
        toastr,
        NgTableParams,
        $state,
        $timeout,
        appFactory,
        $window
    ) {
        $scope.filters = $window.filters;
        $scope.title = $window.title;
        $scope.user = $window.user;
        $scope.headers = $window.headers;
        $scope.cellValues = $window.cellValues;
        angular.forEach($scope.cellValues, function (cellValue) {
            $scope.colspan = cellValue.length;
        });
        console.log($scope.filters);
    });
});
