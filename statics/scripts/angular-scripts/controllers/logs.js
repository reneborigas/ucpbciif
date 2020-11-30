define(function () {
    'use strict';

    var app = angular.module('app');

    app.controller(
        'LogAccessListController',
        function LogAccessListController($http, $filter, $scope, $state, $timeout, toastr, appFactory, NgTableParams, blockUI) {
            $scope.searchTermAuto = {
                keyword: '',
            };

            var logListBlockUI = blockUI.instances.get('logListBlockUI');

            $scope.loadLogs = function () {
                logListBlockUI.start('Loading User Access History ...');
                $scope.tableLogs = new NgTableParams(
                    {
                        page: 1,
                        count: 20,
                    },
                    {
                        counts: [10, 20, 30, 50, 100],
                        getData: function (params) {
                            return $http.get('/api/users/userlogs/', { params: $scope.params }).then(
                                function (response) {
                                    var filteredData = params.filter() ? $filter('filter')(response.data, params.filter()) : response.data;
                                    var orderedData = params.sorting() ? $filter('orderBy')(filteredData, params.orderBy()) : filteredData;
                                    var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                    params.total(response.data.length);
                                    var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                    logListBlockUI.stop();
                                    return page;
                                },
                                function (error) {
                                    logListBlockUI.stop();
                                    toastr.error(
                                        'Error ' + error.status + ' ' + error.statusText,
                                        'Could not load User Access History. Please contact System Administrator.'
                                    );
                                }
                            );
                        },
                    }
                );
            };

            $scope.$watch(
                'searchTermAuto.keyword',
                function (newTerm, oldTerm) {
                    $scope.tableLogs.filter({ $: newTerm });
                },
                true
            );

            $scope.loadLogs();

            $scope.params = {
                action_type: 'Logged',
            };

            $scope.filters = [
                {
                    name: 'Borrower',
                    showFilter: false,
                    filterFormat: 'uppercase',
                    params: {
                        param1: 'borrowerId',
                    },
                },
                {
                    name: 'Date',
                    showFilter: false,
                    filterFormat: "date : 'mediumDate'",
                    params: {
                        param1: 'dateReceivedFrom',
                        param2: 'dateReceivedTo',
                    },
                },
            ];

            $scope.showFilterButton = false;

            $scope.showFilter = function (filter) {
                if (filter.showFilter) {
                    filter.showFilter = false;
                } else {
                    filter.showFilter = true;
                }

                for (var i = 0; i < $scope.filters.length; i++) {
                    if ($scope.filters[i].showFilter == true) {
                        $scope.showFilterButton = true;
                        break;
                    } else {
                        $scope.showFilterButton = false;
                    }
                }
            };

            $scope.applyFilter = function () {
                angular.forEach($scope.filters, function (filter) {
                    if (!filter.showFilter) {
                        angular.forEach(filter.params, function (value, key) {
                            delete $scope.params[value];
                        });
                    }
                });
                $scope.loadLogs();
            };

            $scope.resetFilter = function () {
                angular.forEach($scope.filters, function (filter) {
                    filter.showFilter = false;
                });
                $scope.showFilterButton = false;
                $scope.params = {
                    action_type: 'Logged',
                };
                $scope.loadLogs();
            };

            // $scope.view = function (creditLineId) {
            //     $state.go('app.creditline.info', { creditLineId: creditLineId });
            // };

            $scope.retrieveHeaders = function () {
                var headers = [];
                var ngTable = document.getElementById('tableLogs');
                var rowLength = ngTable.rows.length;

                for (var i = 0; i < rowLength; i++) {
                    var ngCells = ngTable.rows.item(i).cells;
                    var cellLength = ngCells.length;

                    for (var j = 0; j < cellLength; j++) {
                        var cellTitle = ngCells.item(j).getAttribute('data-title');
                        if (cellTitle && cellTitle != "'ACTIONS'") {
                            cellTitle = cellTitle.slice(1, -1);
                            if (!headers.includes(cellTitle)) {
                                headers.push(cellTitle);
                            }
                        }
                    }
                }
                return headers;
            };

            $scope.retrieveCellValues = function () {
                var values = [];
                var ngTable = document.getElementById('tableLogs');
                var rowLength = ngTable.rows.length;

                for (var i = 2; i < rowLength; i++) {
                    var exclude = ngTable.rows.item(i).getAttribute('print-exclude');
                    if (!exclude) {
                        var ngCells = ngTable.rows.item(i).cells;
                        var cellLength = ngCells.length;
                        var cells = [];
                        for (var j = 0; j < cellLength; j++) {
                            if (ngCells.item(j).innerText) {
                                cells.push(ngCells.item(j).innerText);
                            }
                        }
                        values.push(cells);
                    }
                }
                return values;
            };

            $scope.loadCurrentUserInfo = function () {
                var user = {};
                appFactory.getCurrentUserInfo().then(function (data) {
                    user['name'] = data.fullName;
                    user['position'] = data.committeePosition;
                });
                return user;
            };

            $scope.printDataTable = function () {
                var filters = [];
                angular.forEach($scope.filters, function (filter) {
                    if (filter.showFilter) {
                        var parameters = {};
                        angular.forEach(filter.params, function (param) {
                            parameters[param] = $scope.params[param];
                        });
                        filters.push({
                            name: filter.name,
                            filterFormat: filter.filterFormat,
                            params: parameters,
                        });
                    }
                });
                if ($scope.searchTermAuto.keyword) {
                    filters.push({
                        name: 'Search',
                        filterFormat: 'uppercase',
                        params: { input: $scope.searchTermAuto.keyword },
                    });
                }
                var $popup = $window.open('/print/credit-line', '_blank', 'directories=0,width=800,height=800');
                $popup.title = 'User Access History';
                $popup.dateToday = new Date();
                $popup.user = $scope.loadCurrentUserInfo();
                $popup.filters = filters;
                $popup.headers = $scope.retrieveHeaders();
                $popup.cellValues = $scope.retrieveCellValues();
            };
        }
    );

    app.controller(
        'LogCreateListController',
        function LogCreateListController($http, $filter, $scope, $state, $timeout, toastr, appFactory, NgTableParams, blockUI, $q) {
            $scope.searchTermAuto = {
                keyword: '',
            };

            var logListBlockUI = blockUI.instances.get('logListBlockUI');
            var promises = [];

            $scope.loadLogs = function () {
                logListBlockUI.start('Loading User Create History ...');
                $scope.tableLogs = new NgTableParams(
                    {
                        page: 1,
                        count: 20,
                    },
                    {
                        counts: [10, 20, 30, 50, 100],
                        getData: function (params) {
                            return $http.get('/api/users/userlogs/', { params: $scope.params }).then(
                                function (response) {
                                    $scope.data = response.data;
                                    angular.forEach($scope.data, function (val) {
                                        promises.push($scope.returnObject(val));
                                    });
                                    return $q.all(promises).then(function (response) {
                                        if (response) {
                                            var filteredData = params.filter() ? $filter('filter')($scope.data, params.filter()) : $scope.data;
                                            var orderedData = params.sorting() ? $filter('orderBy')(filteredData, params.orderBy()) : filteredData;
                                            var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                            params.total($scope.data.length);
                                            var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                            logListBlockUI.stop();
                                            return page;
                                        }
                                    });
                                },
                                function (error) {
                                    logListBlockUI.stop();
                                    toastr.error(
                                        'Error ' + error.status + ' ' + error.statusText,
                                        'Could not load User Create History. Please contact System Administrator.'
                                    );
                                }
                            );
                        },
                    }
                );
            };

            $scope.returnObject = function (data) {
                var defer = $q.defer();
                $http({
                    url: data.apiLink + '/' + data.object_id,
                    method: 'GET',
                }).then(
                    function (response) {
                        if (response.data[data.valueToDisplay]) {
                            data.action_type =
                                data.action_type + ' ' + appFactory.normalizeString(data.content_typeText) + ' ' + response.data[data.valueToDisplay];
                        }
                        defer.resolve(data);
                    },
                    function (error) {
                        data.action_type = data.action_type + ' ' + appFactory.normalizeString(data.content_typeText) + ' ' + error.statusText;
                        defer.resolve(data);
                    }
                );
                return defer.promise;
            };

            $scope.$watch(
                'searchTermAuto.keyword',
                function (newTerm, oldTerm) {
                    $scope.tableLogs.filter({ $: newTerm });
                },
                true
            );

            $scope.loadLogs();

            $scope.params = {
                action_type: 'Create',
            };

            $scope.filters = [
                {
                    name: 'Borrower',
                    showFilter: false,
                    filterFormat: 'uppercase',
                    params: {
                        param1: 'borrowerId',
                    },
                },
                {
                    name: 'Date',
                    showFilter: false,
                    filterFormat: "date : 'mediumDate'",
                    params: {
                        param1: 'dateReceivedFrom',
                        param2: 'dateReceivedTo',
                    },
                },
            ];

            $scope.showFilterButton = false;

            $scope.showFilter = function (filter) {
                if (filter.showFilter) {
                    filter.showFilter = false;
                } else {
                    filter.showFilter = true;
                }

                for (var i = 0; i < $scope.filters.length; i++) {
                    if ($scope.filters[i].showFilter == true) {
                        $scope.showFilterButton = true;
                        break;
                    } else {
                        $scope.showFilterButton = false;
                    }
                }
            };

            $scope.applyFilter = function () {
                angular.forEach($scope.filters, function (filter) {
                    if (!filter.showFilter) {
                        angular.forEach(filter.params, function (value, key) {
                            delete $scope.params[value];
                        });
                    }
                });
                $scope.loadLogs();
            };

            $scope.resetFilter = function () {
                angular.forEach($scope.filters, function (filter) {
                    filter.showFilter = false;
                });
                $scope.showFilterButton = false;
                $scope.params = {
                    action_type: 'Create',
                };
                $scope.loadLogs();
            };

            $scope.retrieveHeaders = function () {
                var headers = [];
                var ngTable = document.getElementById('tableLogs');
                var rowLength = ngTable.rows.length;

                for (var i = 0; i < rowLength; i++) {
                    var ngCells = ngTable.rows.item(i).cells;
                    var cellLength = ngCells.length;

                    for (var j = 0; j < cellLength; j++) {
                        var cellTitle = ngCells.item(j).getAttribute('data-title');
                        if (cellTitle && cellTitle != "'ACTIONS'") {
                            cellTitle = cellTitle.slice(1, -1);
                            if (!headers.includes(cellTitle)) {
                                headers.push(cellTitle);
                            }
                        }
                    }
                }
                return headers;
            };

            $scope.retrieveCellValues = function () {
                var values = [];
                var ngTable = document.getElementById('tableLogs');
                var rowLength = ngTable.rows.length;

                for (var i = 2; i < rowLength; i++) {
                    var exclude = ngTable.rows.item(i).getAttribute('print-exclude');
                    if (!exclude) {
                        var ngCells = ngTable.rows.item(i).cells;
                        var cellLength = ngCells.length;
                        var cells = [];
                        for (var j = 0; j < cellLength; j++) {
                            if (ngCells.item(j).innerText) {
                                cells.push(ngCells.item(j).innerText);
                            }
                        }
                        values.push(cells);
                    }
                }
                return values;
            };

            $scope.loadCurrentUserInfo = function () {
                var user = {};
                appFactory.getCurrentUserInfo().then(function (data) {
                    user['name'] = data.fullName;
                    user['position'] = data.committeePosition;
                });
                return user;
            };

            $scope.printDataTable = function () {
                var filters = [];
                angular.forEach($scope.filters, function (filter) {
                    if (filter.showFilter) {
                        var parameters = {};
                        angular.forEach(filter.params, function (param) {
                            parameters[param] = $scope.params[param];
                        });
                        filters.push({
                            name: filter.name,
                            filterFormat: filter.filterFormat,
                            params: parameters,
                        });
                    }
                });
                if ($scope.searchTermAuto.keyword) {
                    filters.push({
                        name: 'Search',
                        filterFormat: 'uppercase',
                        params: { input: $scope.searchTermAuto.keyword },
                    });
                }
                var $popup = $window.open('/print/credit-line', '_blank', 'directories=0,width=800,height=800');
                $popup.title = 'User Create History';
                $popup.dateToday = new Date();
                $popup.user = $scope.loadCurrentUserInfo();
                $popup.filters = filters;
                $popup.headers = $scope.retrieveHeaders();
                $popup.cellValues = $scope.retrieveCellValues();
            };
        }
    );

    app.controller(
        'LogEditListController',
        function LogEditListController($http, $filter, $scope, $state, $timeout, toastr, appFactory, NgTableParams, blockUI, $q) {
            $scope.searchTermAuto = {
                keyword: '',
            };

            var logListBlockUI = blockUI.instances.get('logListBlockUI');
            var promises = [];

            $scope.loadLogs = function () {
                logListBlockUI.start('Loading User Edit History ...');
                $scope.tableLogs = new NgTableParams(
                    {
                        page: 1,
                        count: 20,
                    },
                    {
                        counts: [10, 20, 30, 50, 100],
                        getData: function (params) {
                            return $http.get('/api/users/userlogs/', { params: $scope.params }).then(
                                function (response) {
                                    $scope.data = response.data;
                                    angular.forEach($scope.data, function (val) {
                                        promises.push($scope.returnObject(val));
                                    });
                                    return $q.all(promises).then(function (response) {
                                        if (response) {
                                            var filteredData = params.filter() ? $filter('filter')($scope.data, params.filter()) : $scope.data;
                                            var orderedData = params.sorting() ? $filter('orderBy')(filteredData, params.orderBy()) : filteredData;
                                            var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                            params.total($scope.data.length);
                                            var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                            logListBlockUI.stop();
                                            return page;
                                        }
                                    });
                                },
                                function (error) {
                                    logListBlockUI.stop();
                                    toastr.error(
                                        'Error ' + error.status + ' ' + error.statusText,
                                        'Could not load User Edit History. Please contact System Administrator.'
                                    );
                                }
                            );
                        },
                    }
                );
            };

            $scope.returnObject = function (data) {
                var defer = $q.defer();
                $http({
                    url: data.apiLink + '/' + data.object_id,
                    method: 'GET',
                }).then(
                    function (response) {
                        if (response.data[data.valueToDisplay]) {
                            data.action_type =
                                data.action_type + ' ' + appFactory.normalizeString(data.content_typeText) + ' ' + response.data[data.valueToDisplay];
                        }
                        defer.resolve(data);
                    },
                    function (error) {
                        data.action_type = data.action_type + ' ' + appFactory.normalizeString(data.content_typeText) + ' ' + error.statusText;
                        defer.resolve(data);
                    }
                );
                return defer.promise;
            };

            $scope.getObject = function (object) {
                var defer = $q.defer();
                angular.forEach(object, function (data) {
                    $http({
                        url: data.apiLink + '/' + data.object_id,
                        method: 'GET',
                    }).then(
                        function (response) {
                            if (response.data[data.valueToDisplay]) {
                                data.action_type =
                                    data.action_type +
                                    ' ' +
                                    appFactory.normalizeString(data.content_typeText) +
                                    ' ' +
                                    response.data[data.valueToDisplay];
                                defer.resolve(data.action_type);
                            }
                        },
                        function (error) {
                            data.action_type = data.action_type + ' ' + appFactory.normalizeString(data.content_typeText) + ' ' + error.statusText;
                            defer.resolve(data.action_type);
                        }
                    );
                });
                return defer.promise;
            };

            $scope.$watch(
                'searchTermAuto.keyword',
                function (newTerm, oldTerm) {
                    $scope.tableLogs.filter({ $: newTerm });
                },
                true
            );

            $scope.loadLogs();

            $scope.params = {
                action_type: 'Edit',
            };

            $scope.filters = [
                {
                    name: 'Borrower',
                    showFilter: false,
                    filterFormat: 'uppercase',
                    params: {
                        param1: 'borrowerId',
                    },
                },
                {
                    name: 'Date',
                    showFilter: false,
                    filterFormat: "date : 'mediumDate'",
                    params: {
                        param1: 'dateReceivedFrom',
                        param2: 'dateReceivedTo',
                    },
                },
            ];

            $scope.showFilterButton = false;

            $scope.showFilter = function (filter) {
                if (filter.showFilter) {
                    filter.showFilter = false;
                } else {
                    filter.showFilter = true;
                }

                for (var i = 0; i < $scope.filters.length; i++) {
                    if ($scope.filters[i].showFilter == true) {
                        $scope.showFilterButton = true;
                        break;
                    } else {
                        $scope.showFilterButton = false;
                    }
                }
            };

            $scope.applyFilter = function () {
                angular.forEach($scope.filters, function (filter) {
                    if (!filter.showFilter) {
                        angular.forEach(filter.params, function (value, key) {
                            delete $scope.params[value];
                        });
                    }
                });
                $scope.loadLogs();
            };

            $scope.resetFilter = function () {
                angular.forEach($scope.filters, function (filter) {
                    filter.showFilter = false;
                });
                $scope.showFilterButton = false;
                $scope.params = {
                    action_type: 'Edit',
                };
                $scope.loadLogs();
            };

            // $scope.view = function (creditLineId) {
            //     $state.go('app.creditline.info', { creditLineId: creditLineId });
            // };

            $scope.retrieveHeaders = function () {
                var headers = [];
                var ngTable = document.getElementById('tableLogs');
                var rowLength = ngTable.rows.length;

                for (var i = 0; i < rowLength; i++) {
                    var ngCells = ngTable.rows.item(i).cells;
                    var cellLength = ngCells.length;

                    for (var j = 0; j < cellLength; j++) {
                        var cellTitle = ngCells.item(j).getAttribute('data-title');
                        if (cellTitle && cellTitle != "'ACTIONS'") {
                            cellTitle = cellTitle.slice(1, -1);
                            if (!headers.includes(cellTitle)) {
                                headers.push(cellTitle);
                            }
                        }
                    }
                }
                return headers;
            };

            $scope.retrieveCellValues = function () {
                var values = [];
                var ngTable = document.getElementById('tableLogs');
                var rowLength = ngTable.rows.length;

                for (var i = 2; i < rowLength; i++) {
                    var exclude = ngTable.rows.item(i).getAttribute('print-exclude');
                    if (!exclude) {
                        var ngCells = ngTable.rows.item(i).cells;
                        var cellLength = ngCells.length;
                        var cells = [];
                        for (var j = 0; j < cellLength; j++) {
                            if (ngCells.item(j).innerText) {
                                cells.push(ngCells.item(j).innerText);
                            }
                        }
                        values.push(cells);
                    }
                }
                return values;
            };

            $scope.loadCurrentUserInfo = function () {
                var user = {};
                appFactory.getCurrentUserInfo().then(function (data) {
                    user['name'] = data.fullName;
                    user['position'] = data.committeePosition;
                });
                return user;
            };

            $scope.printDataTable = function () {
                var filters = [];
                angular.forEach($scope.filters, function (filter) {
                    if (filter.showFilter) {
                        var parameters = {};
                        angular.forEach(filter.params, function (param) {
                            parameters[param] = $scope.params[param];
                        });
                        filters.push({
                            name: filter.name,
                            filterFormat: filter.filterFormat,
                            params: parameters,
                        });
                    }
                });
                if ($scope.searchTermAuto.keyword) {
                    filters.push({
                        name: 'Search',
                        filterFormat: 'uppercase',
                        params: { input: $scope.searchTermAuto.keyword },
                    });
                }
                var $popup = $window.open('/print/credit-line', '_blank', 'directories=0,width=800,height=800');
                $popup.title = 'User Edit History';
                $popup.dateToday = new Date();
                $popup.user = $scope.loadCurrentUserInfo();
                $popup.filters = filters;
                $popup.headers = $scope.retrieveHeaders();
                $popup.cellValues = $scope.retrieveCellValues();
            };
        }
    );

    app.controller(
        'LogDeleteListController',
        function LogDeleteListController($http, $filter, $scope, $state, $timeout, toastr, appFactory, NgTableParams, blockUI, $q) {
            $scope.searchTermAuto = {
                keyword: '',
            };

            var logListBlockUI = blockUI.instances.get('logListBlockUI');
            var promises = [];

            $scope.loadLogs = function () {
                logListBlockUI.start('Loading User Delete History ...');
                $scope.tableLogs = new NgTableParams(
                    {
                        page: 1,
                        count: 20,
                    },
                    {
                        counts: [10, 20, 30, 50, 100],
                        getData: function (params) {
                            return $http.get('/api/users/userlogs/', { params: $scope.params }).then(
                                function (response) {
                                    $scope.data = response.data;
                                    angular.forEach($scope.data, function (val) {
                                        promises.push($scope.returnObject(val));
                                    });
                                    return $q.all(promises).then(function (response) {
                                        if (response) {
                                            var filteredData = params.filter() ? $filter('filter')($scope.data, params.filter()) : $scope.data;
                                            var orderedData = params.sorting() ? $filter('orderBy')(filteredData, params.orderBy()) : filteredData;
                                            var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                            params.total($scope.data.length);
                                            var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                            logListBlockUI.stop();
                                            return page;
                                        }
                                    });
                                },
                                function (error) {
                                    logListBlockUI.stop();
                                    toastr.error(
                                        'Error ' + error.status + ' ' + error.statusText,
                                        'Could not load User Delete History. Please contact System Administrator.'
                                    );
                                }
                            );
                        },
                    }
                );
            };

            $scope.returnObject = function (data) {
                var defer = $q.defer();
                $http({
                    url: data.apiLink + '/' + data.object_id,
                    method: 'GET',
                }).then(
                    function (response) {
                        if (response.data[data.valueToDisplay]) {
                            data.action_type =
                                data.action_type + ' ' + appFactory.normalizeString(data.content_typeText) + ' ' + response.data[data.valueToDisplay];
                        }
                        defer.resolve(data);
                    },
                    function (error) {
                        data.action_type = data.action_type + ' ' + appFactory.normalizeString(data.content_typeText) + ' ' + error.statusText;
                        defer.resolve(data);
                    }
                );
                return defer.promise;
            };

            $scope.getObject = function (object) {
                var defer = $q.defer();
                angular.forEach(object, function (data) {
                    $http({
                        url: data.apiLink + '/' + data.object_id,
                        method: 'GET',
                    }).then(
                        function (response) {
                            if (response.data[data.valueToDisplay]) {
                                data.action_type =
                                    data.action_type +
                                    ' ' +
                                    appFactory.normalizeString(data.content_typeText) +
                                    ' ' +
                                    response.data[data.valueToDisplay];
                                defer.resolve(data.action_type);
                            }
                        },
                        function (error) {
                            data.action_type = data.action_type + ' ' + appFactory.normalizeString(data.content_typeText) + ' ' + error.statusText;
                            defer.resolve(data.action_type);
                        }
                    );
                });
                return defer.promise;
            };

            $scope.$watch(
                'searchTermAuto.keyword',
                function (newTerm, oldTerm) {
                    $scope.tableLogs.filter({ $: newTerm });
                },
                true
            );

            $scope.loadLogs();

            $scope.params = {
                action_type: 'Delete',
            };

            $scope.filters = [
                {
                    name: 'Borrower',
                    showFilter: false,
                    filterFormat: 'uppercase',
                    params: {
                        param1: 'borrowerId',
                    },
                },
                {
                    name: 'Date',
                    showFilter: false,
                    filterFormat: "date : 'mediumDate'",
                    params: {
                        param1: 'dateReceivedFrom',
                        param2: 'dateReceivedTo',
                    },
                },
            ];

            $scope.showFilterButton = false;

            $scope.showFilter = function (filter) {
                if (filter.showFilter) {
                    filter.showFilter = false;
                } else {
                    filter.showFilter = true;
                }

                for (var i = 0; i < $scope.filters.length; i++) {
                    if ($scope.filters[i].showFilter == true) {
                        $scope.showFilterButton = true;
                        break;
                    } else {
                        $scope.showFilterButton = false;
                    }
                }
            };

            $scope.applyFilter = function () {
                angular.forEach($scope.filters, function (filter) {
                    if (!filter.showFilter) {
                        angular.forEach(filter.params, function (value, key) {
                            delete $scope.params[value];
                        });
                    }
                });
                $scope.loadLogs();
            };

            $scope.resetFilter = function () {
                angular.forEach($scope.filters, function (filter) {
                    filter.showFilter = false;
                });
                $scope.showFilterButton = false;
                $scope.params = {
                    action_type: 'Delete',
                };
                $scope.loadLogs();
            };

            // $scope.view = function (creditLineId) {
            //     $state.go('app.creditline.info', { creditLineId: creditLineId });
            // };

            $scope.retrieveHeaders = function () {
                var headers = [];
                var ngTable = document.getElementById('tableLogs');
                var rowLength = ngTable.rows.length;

                for (var i = 0; i < rowLength; i++) {
                    var ngCells = ngTable.rows.item(i).cells;
                    var cellLength = ngCells.length;

                    for (var j = 0; j < cellLength; j++) {
                        var cellTitle = ngCells.item(j).getAttribute('data-title');
                        if (cellTitle && cellTitle != "'ACTIONS'") {
                            cellTitle = cellTitle.slice(1, -1);
                            if (!headers.includes(cellTitle)) {
                                headers.push(cellTitle);
                            }
                        }
                    }
                }
                return headers;
            };

            $scope.retrieveCellValues = function () {
                var values = [];
                var ngTable = document.getElementById('tableLogs');
                var rowLength = ngTable.rows.length;

                for (var i = 2; i < rowLength; i++) {
                    var exclude = ngTable.rows.item(i).getAttribute('print-exclude');
                    if (!exclude) {
                        var ngCells = ngTable.rows.item(i).cells;
                        var cellLength = ngCells.length;
                        var cells = [];
                        for (var j = 0; j < cellLength; j++) {
                            if (ngCells.item(j).innerText) {
                                cells.push(ngCells.item(j).innerText);
                            }
                        }
                        values.push(cells);
                    }
                }
                return values;
            };

            $scope.loadCurrentUserInfo = function () {
                var user = {};
                appFactory.getCurrentUserInfo().then(function (data) {
                    user['name'] = data.fullName;
                    user['position'] = data.committeePosition;
                });
                return user;
            };

            $scope.printDataTable = function () {
                var filters = [];
                angular.forEach($scope.filters, function (filter) {
                    if (filter.showFilter) {
                        var parameters = {};
                        angular.forEach(filter.params, function (param) {
                            parameters[param] = $scope.params[param];
                        });
                        filters.push({
                            name: filter.name,
                            filterFormat: filter.filterFormat,
                            params: parameters,
                        });
                    }
                });
                if ($scope.searchTermAuto.keyword) {
                    filters.push({
                        name: 'Search',
                        filterFormat: 'uppercase',
                        params: { input: $scope.searchTermAuto.keyword },
                    });
                }
                var $popup = $window.open('/print/credit-line', '_blank', 'directories=0,width=800,height=800');
                $popup.title = 'User Edit History';
                $popup.dateToday = new Date();
                $popup.user = $scope.loadCurrentUserInfo();
                $popup.filters = filters;
                $popup.headers = $scope.retrieveHeaders();
                $popup.cellValues = $scope.retrieveCellValues();
            };
        }
    );
});
