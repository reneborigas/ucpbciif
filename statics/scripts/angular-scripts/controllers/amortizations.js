define(function () {
    'use strict';

    var app = angular.module('app');

    app.controller(
        'AmortizationListController',
        function AmortizationListController($http, $filter, $scope, $state, $timeout, toastr, appFactory, NgTableParams, $window, blockUI) {
            $scope.searchTermAuto = {
                keyword: '',
            };

            var amortizationListBlockUI = blockUI.instances.get('amortizationListBlockUI');

            $scope.loadAmortizations = function () {
                amortizationListBlockUI.start('Loading Amortizations...');
                $scope.tableAmortization = new NgTableParams(
                    {
                        page: 1,
                        count: 20,
                    },
                    {
                        counts: [10, 20, 30, 50, 100],
                        getData: function (params) {
                            return $http.get('/api/loans/amortizationitems/', { params: $scope.params }).then(
                                function (response) {
                                    console.log(response.data);
                                    var filteredData = params.filter() ? $filter('filter')(response.data, params.filter()) : response.data;
                                    var orderedData = params.sorting() ? $filter('orderBy')(filteredData, params.orderBy()) : filteredData;
                                    var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                    params.total(response.data.length);

                                    var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                    amortizationListBlockUI.stop();
                                    return page;
                                },
                                function (error) {
                                    amortizationListBlockUI.stop();
                                    toastr.error(
                                        'Error ' + error.status + ' ' + error.statusText,
                                        'Could not load Amortization Lists. Please contact System Administrator.'
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
                    $scope.tableAmortization.filter({ $: newTerm });
                },
                true
            );

            $scope.loadAmortizations();

            appFactory.getAmortizationStatus().then(function (data) {
                $scope.amortizationStatuses = data;
            });

            $scope.params = {};

            $scope.filters = [
                {
                    name: 'Schedule Date Range',
                    showFilter: false,
                    filterFormat: "date : 'mediumDate'",
                    params: {
                        param1: 'scheduleDateFrom',
                        param2: 'scheduleDateTo',
                    },
                },
                {
                    name: 'Number of Days Range',
                    showFilter: false,
                    filterFormat: 'uppercase',
                    params: {
                        param1: 'numberofDaysFrom',
                        param2: 'numberofDaysTo',
                    },
                },
                {
                    name: 'Principal Range',
                    showFilter: false,
                    filterFormat: "currency :'₱'",
                    params: {
                        param1: 'principalFrom',
                        param2: 'principalTo',
                    },
                },
                {
                    name: 'Interest Range',
                    showFilter: false,
                    filterFormat: "currency :'₱'",
                    params: {
                        param1: 'interestFrom',
                        param2: 'interestTo',
                    },
                },
                {
                    name: 'Accrued Interest Range',
                    showFilter: false,
                    filterFormat: "currency :'₱'",
                    params: {
                        param1: 'interestFrom',
                        param2: 'interestTo',
                    },
                },
                {
                    name: 'Penalty Amount Range',
                    showFilter: false,
                    filterFormat: "currency :'₱'",
                    params: {
                        param1: 'penaltyFrom',
                        param2: 'penaltyTo',
                    },
                },
                {
                    name: 'Amortization Range',
                    showFilter: false,
                    filterFormat: "currency :'₱'",
                    params: {
                        param1: 'amortizationFrom',
                        param2: 'amortizationTo',
                    },
                },
                {
                    name: 'Principal Balance Range',
                    showFilter: false,
                    filterFormat: "currency :'₱'",
                    params: {
                        param1: 'principalBalanceFrom',
                        param2: 'principalBalanceTo',
                    },
                },
                {
                    name: 'Status',
                    showFilter: false,
                    filterFormat: 'uppercase',
                    params: {
                        param1: 'status',
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
                console.log($scope.params);
                $scope.loadAmortizations();
            };

            $scope.resetFilter = function () {
                angular.forEach($scope.filters, function (filter) {
                    filter.showFilter = false;
                });
                $scope.showFilterButton = false;
                $scope.params = {};
                $scope.loadAmortizations();
            };

            $scope.view = function (loanId) {
                $state.go('app.loans.info', { loanId: loanId });
            };

            $scope.retrieveHeaders = function () {
                var headers = [];
                var ngTable = document.getElementById('tableAmortization');
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
                var ngTable = document.getElementById('tableAmortization');
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
                var $popup = $window.open('/print/amortizations', '_blank', 'directories=0,width=800,height=800');
                $popup.title = 'Amortization List';
                $popup.dateToday = new Date();
                $popup.user = $scope.loadCurrentUserInfo();
                $popup.filters = filters;
                $popup.headers = $scope.retrieveHeaders();
                $popup.cellValues = $scope.retrieveCellValues();
            };
        }
    );

    app.controller(
        'MaturingAmortizationListController',
        function MaturingAmortizationListController($http, $filter, $scope, $state, $timeout, toastr, appFactory, NgTableParams, $window, blockUI) {
            $scope.searchTermAuto = {
                keyword: '',
            };

            var maturingAmortizationListBlockUI = blockUI.instances.get('maturingAmortizationListBlockUI');

            $scope.loadMaturingAmortizations = function () {
                maturingAmortizationListBlockUI.start('Loading Maturing Amortizations...');
                $scope.tableMaturingAmortization = new NgTableParams(
                    {
                        page: 1,
                        count: 20,
                    },
                    {
                        counts: [10, 20, 30, 50, 100],
                        getData: function (params) {
                            return $http.get('/api/loans/amortizationitems/', { params: $scope.params }).then(
                                function (response) {
                                    console.log(response.data);
                                    var filteredData = params.filter() ? $filter('filter')(response.data, params.filter()) : response.data;
                                    var orderedData = params.sorting() ? $filter('orderBy')(filteredData, params.orderBy()) : filteredData;
                                    var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                    params.total(response.data.length);

                                    var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                    maturingAmortizationListBlockUI.stop();
                                    return page;
                                },
                                function (error) {
                                    toastr.error(
                                        'Error ' + error.status + ' ' + error.statusText,
                                        'Could not load Maturing Amortization Lists. Please contact System Administrator.'
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
                    $scope.tableMaturingAmortization.filter({ $: newTerm });
                },
                true
            );

            $scope.loadMaturingAmortizations();

            appFactory.getAmortizationStatus().then(function (data) {
                $scope.amortizationStatuses = data;
            });

            $scope.params = {
                maturing: 'TRUE',
            };

            $scope.filters = [
                {
                    name: 'Schedule Date Range',
                    showFilter: false,
                    filterFormat: "date : 'mediumDate'",
                    params: {
                        param1: 'scheduleDateFrom',
                        param2: 'scheduleDateTo',
                    },
                },
                {
                    name: 'Number of Days Range',
                    showFilter: false,
                    filterFormat: 'uppercase',
                    params: {
                        param1: 'numberofDaysFrom',
                        param2: 'numberofDaysTo',
                    },
                },
                {
                    name: 'Principal Range',
                    showFilter: false,
                    filterFormat: "currency :'₱'",
                    params: {
                        param1: 'principalFrom',
                        param2: 'principalTo',
                    },
                },
                {
                    name: 'Interest Range',
                    showFilter: false,
                    filterFormat: "currency :'₱'",
                    params: {
                        param1: 'interestFrom',
                        param2: 'interestTo',
                    },
                },
                {
                    name: 'Accrued Interest Range',
                    showFilter: false,
                    filterFormat: "currency :'₱'",
                    params: {
                        param1: 'accruedInterestFrom',
                        param2: 'accruedInterestTo',
                    },
                },
                {
                    name: 'Penalty Amount Range',
                    showFilter: false,
                    filterFormat: "currency :'₱'",
                    params: {
                        param1: 'penaltyFrom',
                        param2: 'penaltyTo',
                    },
                },
                {
                    name: 'Amortization Range',
                    showFilter: false,
                    filterFormat: "currency :'₱'",
                    params: {
                        param1: 'amortizationFrom',
                        param2: 'amortizationTo',
                    },
                },
                {
                    name: 'Principal Balance Range',
                    showFilter: false,
                    filterFormat: "currency :'₱'",
                    params: {
                        param1: 'principalBalanceFrom',
                        param2: 'principalBalanceTo',
                    },
                },
                {
                    name: 'Status',
                    showFilter: false,
                    filterFormat: 'uppercase',
                    params: {
                        param1: 'status',
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
                $scope.loadMaturingAmortizations();
            };

            $scope.resetFilter = function () {
                angular.forEach($scope.filters, function (filter) {
                    filter.showFilter = false;
                });
                $scope.showFilterButton = false;
                $scope.params = {
                    maturing: 'TRUE',
                };
                $scope.loadMaturingAmortizations();
            };

            $scope.view = function (loanId) {
                $state.go('app.payments.new', { loanId: loanId });
            };

            $scope.retrieveHeaders = function () {
                var headers = [];
                var ngTable = document.getElementById('tableMaturingAmortization');
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
                var ngTable = document.getElementById('tableMaturingAmortization');
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
                var $popup = $window.open('/print/maturingamortizations', '_blank', 'directories=0,width=800,height=800');
                $popup.title = 'Maturing Amortization List';
                $popup.dateToday = new Date();
                $popup.user = $scope.loadCurrentUserInfo();
                $popup.filters = filters;
                $popup.headers = $scope.retrieveHeaders();
                $popup.cellValues = $scope.retrieveCellValues();
            };
        }
    );
});
