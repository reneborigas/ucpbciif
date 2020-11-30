define(function () {
    'use strict';

    var app = angular.module('app');

    app.controller(
        'ChecksListController',
        function ChecksListController($http, $filter, $scope, $state, $timeout, toastr, appFactory, NgTableParams, blockUI) {
            $scope.searchTermAuto = {
                keyword: '',
            };

            var checksListBlockUI = blockUI.instances.get('checksListBlockUI');

            $scope.loadChecks = function () {
                checksListBlockUI.start('Loading Postdated Checks...');
                $scope.tableChecks = new NgTableParams(
                    {
                        page: 1,
                        count: 20,
                    },
                    {
                        counts: [10, 20, 30, 50, 100],
                        getData: function (params) {
                            return $http.get('/api/payments/checks/', { params: $scope.params }).then(
                                function (response) {
                                    var filteredData = params.filter() ? $filter('filter')(response.data, params.filter()) : response.data;
                                    var orderedData = params.sorting() ? $filter('orderBy')(filteredData, params.orderBy()) : filteredData;
                                    var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                    params.total(response.data.length);

                                    var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                    checksListBlockUI.stop();
                                    return page;
                                },
                                function (error) {
                                    checksListBlockUI.stop();
                                    toastr.error(
                                        'Error ' + error.status + ' ' + error.statusText,
                                        'Could not load Postdated Check List. Please contact System Administrator.'
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
                    $scope.tableChecks.filter({ $: newTerm });
                },
                true
            );

            $scope.loadChecks();

            appFactory.getCheckStatuses().then(function (data) {
                $scope.checkstatus = data;
            });

            $scope.params = {};

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
                    name: 'Date Received',
                    showFilter: false,
                    filterFormat: "date : 'mediumDate'",
                    params: {
                        param1: 'dateReceivedFrom',
                        param2: 'dateReceivedTo',
                    },
                },
                {
                    name: 'PN No.',
                    showFilter: false,
                    filterFormat: 'uppercase',
                    params: {
                        param1: 'pnNo',
                    },
                },
                {
                    name: 'Bank/Branch',
                    showFilter: false,
                    filterFormat: 'uppercase',
                    params: {
                        param1: 'bankBranch',
                    },
                },
                {
                    name: 'Check No.',
                    showFilter: false,
                    filterFormat: 'uppercase',
                    params: {
                        param1: 'checkNo',
                    },
                },
                {
                    name: 'Account No.',
                    showFilter: false,
                    filterFormat: 'uppercase',
                    params: {
                        param1: 'accountNo',
                    },
                },
                {
                    name: 'Check Date',
                    showFilter: false,
                    filterFormat: "date : 'mediumDate'",
                    params: {
                        param1: 'checkDateFrom',
                        param2: 'checkDateTo',
                    },
                },
                {
                    name: 'Amount',
                    showFilter: false,
                    filterFormat: "currency :'₱'",
                    params: {
                        param1: 'amountFrom',
                        param2: 'amountTo',
                    },
                },
                {
                    name: 'Status',
                    showFilter: false,
                    filterFormat: 'uppercase',
                    params: {
                        param1: 'checkStatus',
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
                $scope.loadChecks();
            };

            $scope.resetFilter = function () {
                angular.forEach($scope.filters, function (filter) {
                    filter.showFilter = false;
                });
                $scope.showFilterButton = false;
                $scope.params = {};
                $scope.loadChecks();
            };

            // $scope.view = function (creditLineId) {
            //     $state.go('app.creditline.info', { creditLineId: creditLineId });
            // };

            $scope.retrieveHeaders = function () {
                var headers = [];
                var ngTable = document.getElementById('tableChecks');
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
                var ngTable = document.getElementById('tableChecks');
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
                $popup.title = 'Postdated Checks List';
                $popup.dateToday = new Date();
                $popup.user = $scope.loadCurrentUserInfo();
                $popup.filters = filters;
                $popup.headers = $scope.retrieveHeaders();
                $popup.cellValues = $scope.retrieveCellValues();
            };
        }
    );
});
