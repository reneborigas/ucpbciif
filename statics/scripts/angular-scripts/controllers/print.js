define(function () {
    'use strict';

    var app = angular.module('app');

    app.controller(
        'DynamicPrintController',
        function DynamicPrintController($http, $filter, $scope, toastr, NgTableParams, $state, $timeout, appFactory, $window) {
            $scope.filters = $window.filters;
            $scope.title = $window.title;
            $scope.user = $window.user;
            $scope.headers = $window.headers;
            $scope.cellValues = $window.cellValues;
            $scope.dateToday = $window.dateToday;
            angular.forEach($scope.cellValues, function (cellValue) {
                $scope.colspan = cellValue.length;
            });
            console.log($scope.filters);

            $scope.formatCell = function (cell, parentIndex) {
                var field = cell.toString();
                console.log(index);
                return cell;
            };
        }
    );
});
