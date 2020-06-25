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
});
