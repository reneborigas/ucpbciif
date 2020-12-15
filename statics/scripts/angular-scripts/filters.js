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

    app.filter('splitCamelCase', [
        function () {
            return function (input) {
                if (typeof input !== 'string') {
                    return input;
                }

                return input.replace(/([A-Z])/g, (match) => ` ${match}`).replace(/^./, (match) => match.toUpperCase());
            };
        },
    ]);

    app.filter('normalizeString', [
        function () {
            return function (input) {
                if (typeof input !== 'string') {
                    return input;
                }

                return input
                    .replace(/([A-Z])/g, function ($1) {
                        return ' ' + $1.toUpperCase();
                    })
                    .replace(/([_])/g, function ($1) {
                        return ' ';
                    })
                    .replace(/\s[a-z]/g, function ($1) {
                        return $1.toUpperCase();
                    })
                    .replace(/^./, function (str) {
                        return str.toUpperCase();
                    });
            };
        },
    ]);

    app.filter('dateCompare', [
        function () {
            return function (object, dateFrom, dateTo) {
                console.log(dateFrom);
                console.log(dateTo);
                return object;
            };
        },
    ]);
});
