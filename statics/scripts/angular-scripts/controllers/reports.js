define(function () {
    'use strict';

    var app = angular.module('app');

    app.controller('LoanReportListController', function LoanReportListController(
        $http,
        $filter,
        $scope,
        toastr,
        NgTableParams,
        appFactory,
        $state,
        $timeout
    ) {
        $scope.reports = [
            {
                category: 'Loan Releases',
                subcategory: [
                    {
                        name: 'Per Area',
                        filter: 'branch',
                        url: '/api/loans/loanreports/',
                    },
                    {
                        name: 'Per Window',
                        filter: 'loanProgram_name',
                        url: '/api/loans/loanreports/',
                    },
                    {
                        name: 'By Loan Term',
                        filter: 'term_name',
                        url: '/api/loans/loanreports/',
                    },
                    {
                        name: 'By Interest Rate',
                        filter: 'interestRate',
                        url: '/api/loans/loanreports/',
                    },
                ],
            },
            {
                category: 'Outstanding Balances',
                subcategory: [
                    {
                        name: 'Per Area',
                        filter: 'branch',
                        url: '/api/loans/loanreports/',
                    },
                    {
                        name: 'Per Window',
                        filter: 'loanProgram_name',
                        url: '/api/loans/loanreports/',
                    },
                    {
                        name: 'By Loan Term',
                        filter: 'term_name',
                        url: '/api/loans/loanreports/',
                    },
                    {
                        name: 'By Interest Rate',
                        filter: 'interestRate',
                        url: '/api/loans/loanreports/',
                    },
                ],
            },
            {
                category: 'Accrued Interest Receivable',
                subcategory: [
                    {
                        name: 'Per Area',
                        filter: 'branch',
                    },
                    {
                        name: 'Per Window',
                        filter: 'loanProgram_name',
                    },
                ],
            },
            {
                category: 'Schedules',
                subcategory: [
                    {
                        name: 'Top Borrowers',
                        filter: '',
                    },
                    {
                        name: 'Loan Payments',
                        filter: '',
                    },
                    {
                        name: 'Secured Loans',
                        filter: '',
                    },
                    {
                        name: 'Unsecured Loans',
                        filter: '',
                    },
                    {
                        name: 'Pulled-out Checks',
                        filter: '',
                    },
                    {
                        name: 'Bounced Checks',
                        filter: '',
                    },
                ],
            },
        ];

        $scope.selectReport = function (category, subcategory, filter, url) {
            var slugCategory = appFactory.slugify(category);
            var slugSubCategory = appFactory.slugify(subcategory);
            $state.go('app.lms-reports.info', { category: slugCategory, subcategory: slugSubCategory, filter: filter, url: url });
        };
    });

    app.controller('ReportsInfoController', function ReportsInfoController(
        $http,
        $filter,
        $scope,
        toastr,
        NgTableParams,
        appFactory,
        $state,
        $timeout,
        $window
    ) {
        $scope.loadReport = function () {
            if ($scope.filter) {
                $http({
                    url: $scope.url,
                    method: 'GET',
                }).then(
                    function (response) {
                        $scope.response = response.data;
                        $scope.groupArray($scope.response, $scope.filter.toString());
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve ' + $scope.category + ' List. Please contact System Administrator.'
                        );
                    }
                );
            } else {
                $state.go('app.lms-reports.list');
            }
        };

        $scope.groupArray = function (array, filter) {
            var array = array;
            var filter = filter;

            var groups = array.reduce(function (obj, item) {
                obj[item[filter]] = obj[item[filter]] || [];
                obj[item[filter]].push(item);
                return obj;
            }, {});

            var myArray = Object.keys(groups).map(function (key) {
                return { parent: key, children: groups[key] };
            });
            console.log(myArray);
            $scope.data = myArray;
        };

        $scope.loadReport();

        $scope.retrieveHeaders = function () {
            var headers = [];
            var ngTable = document.getElementById('tableReports');
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
            var ngTable = document.getElementById('tableReports');
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
            // var filters = [];
            // angular.forEach($scope.filters, function (filter) {
            //     if (filter.showFilter) {
            //         var parameters = {};
            //         angular.forEach(filter.params, function (param) {
            //             parameters[param] = $scope.params[param];
            //         });
            //         filters.push({
            //             name: filter.name,
            //             filterFormat: filter.filterFormat,
            //             params: parameters,
            //         });
            //     }
            // });
            var $popup = $window.open('/print/reports', '_blank', 'directories=0,width=800,height=800');
            $popup.title = $scope.category + ' ' + $scope.subcategory;
            $popup.user = $scope.loadCurrentUserInfo();
            $popup.headers = $scope.retrieveHeaders();
            $popup.cellValues = $scope.retrieveCellValues();
        };
    });
});
