define(function () {
    'use strict';

    var app = angular.module('app');

    app.filter('startFrom', function () {
        return function (input, start) {
            start = +start;
            if (input) {
                return input.slice(start);
            }
        };
    });

    app.filter('trimStringWithExtension', function () {
        return function (string, length) {
            var ext = string.split('.').pop();
            return string.length > length ? string.substring(0, length) + '...' + ext : string;
        };
    });

    app.filter('objectLength', function () {
        return function (object) {
            return Object.keys(object).length;
        };
    });

    app.filter('dynamicFilter', function ($interpolate, $filter) {
        return function (item, name) {
            var result = $interpolate('{{value | ' + arguments[1] + '}}');
            return result({ value: arguments[0] });
        };
    });

    app.filter('staticPercentage', [
        '$filter',
        function ($filter) {
            return function (input, decimals) {
                return $filter('number')(input) + '%';
            };
        },
    ]);

    app.filter('percentage', [
        '$filter',
        function ($filter) {
            return function (input, decimals) {
                return $filter('number')(input * 100, decimals) + '%';
            };
        },
    ]);

    app.filter('trustedHTML', function ($sce) {
        return function (ss) {
            return $sce.trustAsHtml(ss);
        };
    });
});
