define(function () {
    'use strict';

    var app = angular.module('app');

    app.controller('CreditLineListController', function CreditLineListController(
        $http,
        $filter,
        $scope,
        $state,
        $timeout,
        toastr,
        appFactory,
        NgTableParams
    ) {
        $scope.tableCreditLine = new NgTableParams(
            {
                page: 1,
                count: 10,
            },
            {
                counts: [10, 20, 30, 50, 100],
                getData: function (params) {
                    return $http.get('/api/loans/creditlines/', { params: $scope.params }).then(
                        function (response) {
                            console.log(response.data);
                            var filteredData = params.filter()
                                ? $filter('filter')(response.data, params.filter())
                                : response.data;
                            var orderedData = params.sorting()
                                ? $filter('orderBy')(filteredData, params.orderBy())
                                : filteredData;
                            var page = orderedData.slice(
                                (params.page() - 1) * params.count(),
                                params.page() * params.count()
                            );
                            params.total(response.data.length);

                            var page = orderedData.slice(
                                (params.page() - 1) * params.count(),
                                params.page() * params.count()
                            );
                            return page;
                        },
                        function (error) {
                            toastr.error(
                                'Error ' + error.status + ' ' + error.statusText,
                                'Could not load Credit Line Lists. Please contact System Administrator.'
                            );
                        }
                    );
                },
            }
        );

        $scope.$watch(
            'searchTermAuto',
            function (newTerm, oldTerm) {
                $scope.tableCreditLine.filter({ $: newTerm });
            },
            true
        );

        $scope.params = {};

        $scope.filters = [
            {
                name: 'Borrower',
                showFilter: false,
                params: {
                    param1: 'borrowerId',
                },
            },
            {
                name: 'Term',
                showFilter: false,
                params: {
                    param1: 'term',
                },
            },
            {
                name: 'Credit Line Amount Range',
                showFilter: false,
                params: {
                    param1: 'creditLineAmountFrom',
                    param2: 'creditLineAmountTo',
                },
            },
            {
                name: 'Total Availment Range',
                showFilter: false,
                params: {
                    param1: 'totalAvailmentFrom',
                    param2: 'totalAvailmentTo',
                },
            },
            {
                name: 'Interest Range',
                showFilter: false,
                params: {
                    param1: 'interestFrom',
                    param2: 'interestTo',
                },
            },
            {
                name: 'Date Approved Range',
                showFilter: false,
                params: {
                    param1: 'dateApprovedFrom',
                    param2: 'dateApprovedTo',
                },
            },
            {
                name: 'Expiry Date Range',
                showFilter: false,
                params: {
                    param1: 'expiryDateFrom',
                    param2: 'expiryDateTo',
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
            $scope.tableCreditLine.reload();
        };

        $scope.resetFilter = function () {
            angular.forEach($scope.filters, function (filter) {
                filter.showFilter = false;
            });
            $scope.showFilterButton = false;
            $scope.params = {};
            $scope.tableCreditLine.reload();
        };

        $scope.view = function (officeName) {
            var officeNameSlug = appFactory.slugify(officeName);
            $state.go('app.committees.info', { officeName: officeNameSlug });
        };
    });
});
