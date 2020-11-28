define(function () {
    'use strict';

    var app = angular.module('app');

    app.controller(
        'LoanReportListController',
        function LoanReportListController($http, $filter, $scope, toastr, NgTableParams, appFactory, $state, $timeout, $interpolate) {
            $scope.reports = [
                {
                    category: 'Loan Releases',
                    subcategory: [
                        {
                            name: 'Per Status',
                            filter: 'status',
                            url: '/api/loans/loanreports/',
                            params: {},
                            order: {
                                name: 'Status',
                                expression: 'status',
                                reverse: false,
                            },
                            dateFilter: true,
                            hiddenFields: ['releaseMonth'],
                        },
                        {
                            name: 'Per Area',
                            filter: 'branch',
                            url: '/api/loans/loanreports/',
                            params: {},
                            order: {
                                name: 'Area',
                                expression: 'branch',
                                reverse: false,
                            },
                            dateFilter: true,
                            hiddenFields: ['releaseMonth'],
                        },
                        {
                            name: 'Per Loan Category',
                            filter: 'window',
                            url: '/api/loans/loanreports/',
                            params: {},
                            order: {
                                name: 'Loan Category',
                                expression: 'window',
                                reverse: false,
                            },
                            dateFilter: true,
                            hiddenFields: ['releaseMonth'],
                        },
                        {
                            name: 'By Loan Term',
                            filter: 'loanTerm',
                            url: '/api/loans/loanreports/',
                            params: {},
                            order: {
                                name: 'Loan Term',
                                expression: 'loanTerm',
                                reverse: false,
                            },
                            dateFilter: true,
                            hiddenFields: ['releaseMonth'],
                        },
                        {
                            name: 'By Interest Rate',
                            filter: 'loanInterestRate',
                            url: '/api/loans/loanreports/',
                            params: {},
                            order: {
                                name: 'Interest Rate',
                                expression: 'loanInterestRate',
                                reverse: false,
                            },
                            dateFilter: true,
                            hiddenFields: ['releaseMonth'],
                        },
                        {
                            name: 'By Month',
                            filter: 'releaseMonth',
                            url: '/api/loans/loanreports/',
                            params: {},
                            order: {
                                name: 'Month',
                                expression: 'releaseDate',
                                reverse: false,
                            },
                            dateFilter: true,
                            hiddenFields: ['releaseMonth'],
                        },
                    ],
                },
                {
                    category: 'Outstanding Balances',
                    subcategory: [
                        {
                            name: 'Per Area',
                            filter: 'branch',
                            url: '/api/borrowers/borrowersreports/',
                            params: {
                                outstandingBalance: 'TRUE',
                            },
                            order: {
                                name: 'Area',
                                expression: 'branch',
                                reverse: false,
                            },
                            dateFilter: false,
                            hiddenFields: [],
                        },
                        {
                            name: 'Per Loan Category',
                            filter: 'window',
                            url: '/api/loans/loanreportsoutstandingbalance/',
                            params: {},
                            order: {
                                name: 'Loan Category',
                                expression: 'window',
                                reverse: false,
                            },
                            dateFilter: false,
                            hiddenFields: [],
                        },
                        {
                            name: 'By Loan Term',
                            filter: 'loanTerm',
                            url: '/api/loans/loanreportsoutstandingbalance/',
                            params: {},
                            order: {
                                name: 'Loan Term',
                                expression: 'loanTerm',
                                reverse: false,
                            },
                            dateFilter: false,
                            hiddenFields: [],
                        },
                        {
                            name: 'By Interest Rate',
                            filter: 'loanInterestRate',
                            url: '/api/loans/loanreportsoutstandingbalance/',
                            params: {},
                            order: {
                                name: 'Interest Rate',
                                expression: 'loanInterestRate',
                                reverse: false,
                            },
                            dateFilter: false,
                            hiddenFields: [],
                        },
                    ],
                },
                {
                    category: 'Maturing Amortizations',
                    subcategory: [
                        {
                            name: 'Per Area',
                            filter: 'branch',
                            url: '/api/loans/amortizationitemsreports/',
                            params: {
                                maturing: 'TRUE',
                            },
                            order: {
                                name: 'Area',
                                expression: 'branch',
                                reverse: false,
                            },
                            dateFilter: true,
                            hiddenFields: ['amortizationSchedule'],
                        },
                        {
                            name: 'Per Loan Category',
                            filter: 'window',
                            url: '/api/loans/amortizationitemsreports/',
                            params: {
                                maturing: 'TRUE',
                            },
                            order: {
                                name: 'Loan Category',
                                expression: 'window',
                                reverse: false,
                            },
                            dateFilter: true,
                            hiddenFields: ['amortizationSchedule'],
                        },
                        {
                            name: 'By Month',
                            filter: 'amortizationSchedule',
                            url: '/api/loans/amortizationitemsreports/',
                            params: {
                                maturing: 'TRUE',
                            },
                            order: {
                                name: 'Month',
                                expression: 'schedule',
                                reverse: false,
                            },
                            dateFilter: true,
                            hiddenFields: ['amortizationSchedule'],
                        },
                    ],
                },
                {
                    category: 'Accrued Interest Receivable',
                    subcategory: [
                        {
                            name: 'Per Area',
                            filter: 'branch',
                            url: '/api/loans/amortizationitemsreports/',
                            params: {},
                            order: {
                                name: 'Area',
                                expression: 'branch',
                                reverse: false,
                            },
                            dateFilter: true,
                            hiddenFields: ['amortizationSchedule'],
                        },
                        {
                            name: 'Per Loan Category',
                            filter: 'window',
                            url: '/api/loans/amortizationitemsreports/',
                            params: {},
                            order: {
                                name: 'Loan Category',
                                expression: 'window',
                                reverse: false,
                            },
                            dateFilter: true,
                            hiddenFields: ['amortizationSchedule'],
                        },
                        {
                            name: 'By Month',
                            filter: 'amortizationSchedule',
                            url: '/api/loans/amortizationitemsreports/',
                            params: {},
                            order: {
                                name: 'Month',
                                expression: 'schedule',
                                reverse: false,
                            },
                            dateFilter: true,
                            hiddenFields: ['amortizationSchedule'],
                        },
                    ],
                },
                // {
                //     category: 'Monthly Loan Report',
                //     subcategory: [
                //         {
                //             name: 'Per Area',
                //             filter: 'branch',
                //             url: '/api/loans/amortizationitemsreports/',
                //             params: {},
                //             order: {
                //                 name: 'Area',
                //                 expression: 'branch',
                //                 reverse: false,
                //             },
                //         },
                //         {
                //             name: 'Per Loan Category',
                //             filter: 'window',
                //             url: '/api/loans/amortizationitemsreports/',
                //             params: {},
                //             order: {
                //                 name: 'Loan Category',
                //                 expression: 'window',
                //                 reverse: false,
                //             },
                //         },
                //         {
                //             name: 'Per Status',
                //             filter: 'status',
                //             url: '/api/loans/amortizationitemsreports/',
                //             params: {},
                //             order: {
                //                 name: 'Status',
                //                 expression: 'status',
                //                 reverse: false,
                //             },
                //         },
                //     ],
                // },
                // {
                //     category: 'Schedules',
                //     subcategory: [
                //         {
                //             name: 'Top Borrowers',
                //             filter: '',
                //         },
                //         {
                //             name: 'Loan Payments',
                //             filter: '',
                //         },
                //         {
                //             name: 'Secured Loans',
                //             filter: '',
                //         },
                //         {
                //             name: 'Unsecured Loans',
                //             filter: '',
                //         },
                //         {
                //             name: 'Pulled-out Checks',
                //             filter: '',
                //         },
                //         {
                //             name: 'Bounced Checks',
                //             filter: '',
                //         },
                //     ],
                // },
            ];

            $scope.selectReport = function (category, sub) {
                var slugCategory = appFactory.slugify(category);
                var slugSubCategory = appFactory.slugify(sub.name);
                $state.go('app.lms-reports.info', {
                    category: slugCategory,
                    subcategory: slugSubCategory,
                    filter: sub.filter,
                    url: sub.url,
                    params: sub.params,
                    order: sub.order,
                    dateFilter: sub.dateFilter,
                    hiddenFields: sub.hiddenFields,
                });
            };
        }
    );

    app.controller(
        'ReportsInfoController',
        function ReportsInfoController(
            $http,
            $filter,
            $scope,
            toastr,
            NgTableParams,
            appFactory,
            $state,
            $timeout,
            $window,
            $interpolate,
            $parse,
            Excel,
            moment
        ) {
            $scope.loadReport = function () {
                if ($scope.filter) {
                    if ($scope.dateFilter) {
                        $scope.params.startDate = new Date(moment().startOf('year'));
                        $scope.params.endDate = new Date(moment().endOf('year'));
                    }
                    $http({
                        url: $scope.url,
                        method: 'GET',
                        params: $scope.params,
                    }).then(
                        function (response) {
                            $scope.response = $filter('orderBy')(response.data, $scope.order.expression, $scope.order.reverse);
                            console.log($scope.response);
                            $scope.groupArray($scope.response, $scope.filter.toString());
                            $scope.setUpSorting();
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

            $scope.setUpSorting = function () {
                $scope.sorts = [
                    { name: $scope.order.name + ' (Ascending)', reverse: true },
                    { name: $scope.order.name + ' (Descending)', reverse: false },
                ];
                angular.forEach($scope.sorts, function (sort) {
                    if (sort.reverse == $scope.order.reverse) {
                        $scope.currentSort = sort;
                    }
                });
            };

            $scope.sortData = function (sort) {
                $scope.data = $filter('orderBy')($scope.data, 'parent', sort.reverse);
                $scope.currentSort = sort;
            };

            $scope.dateRange = { date: { startDate: moment().startOf('year'), endDate: moment().endOf('year') } };

            $scope.setDateRange = function (date) {
                $scope.params.startDate = new Date(date.startDate);
                $scope.params.endDate = new Date(date.endDate);
                $http({
                    url: $scope.url,
                    method: 'GET',
                    params: $scope.params,
                }).then(
                    function (response) {
                        $scope.response = $filter('orderBy')(response.data, $scope.order.expression, $scope.order.reverse);
                        $scope.groupArray($scope.response, $scope.filter.toString());
                        $scope.setUpSorting();
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve ' + $scope.category + ' List. Please contact System Administrator.'
                        );
                    }
                );
            };

            $scope.dateRangeOptions = {
                locale: {
                    applyClass: 'btn-primary',
                    applyLabel: 'Apply',
                    fromLabel: 'From',
                    format: 'YYYY-MM-DD',
                    toLabel: 'To',
                    cancelLabel: 'Cancel',
                    customRangeLabel: 'Custom range',
                },
                ranges: {
                    Today: [moment(), moment()],
                    Yesterday: [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                    'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                    'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                    'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
                    'This Month': [moment().startOf('month'), moment().endOf('month')],
                    'Last Year': [moment().subtract(1, 'year').startOf('year'), moment().subtract(1, 'year').endOf('year')],
                    'This Year': [moment().startOf('year'), moment().endOf('year')],
                },
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

                $scope.data = myArray;
                console.log($scope.data);
                if ($scope.data.length > 0) {
                    $scope.getHeaders($scope.data[0].children[0]);
                }
            };

            $scope.interpolateField = function (value) {
                var field = value.toString();
                if (field.indexOf('|') != -1) {
                    field = '{{' + field + '}}';
                    return $interpolate(field)($scope);
                } else {
                    return field;
                }
            };

            $scope.hideFields = function (key) {
                var show = true;
                angular.forEach($scope.hiddenFields, function (field) {
                    if (field == key) {
                        show = false;
                    }
                });
                return show;
            };

            $scope.loadReport();

            $scope.getHeaders = function (array) {
                for (prop in this.reservation) {
                    if (typeof this.reservation[prop] === 'string') {
                        console.log(prop + 'value ' + 'is a string');
                    }
                }
            };

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

                for (var i = 0; i < rowLength; i++) {
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
                console.log(values);
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
                var $popup = $window.open('/print/reports', '_blank', 'directories=0,width=800,height=800');
                $popup.title = $scope.category + ' ' + $scope.subcategory;
                $popup.dateToday = new Date();
                $popup.user = $scope.loadCurrentUserInfo();
                $popup.headers = $scope.retrieveHeaders();
                $popup.cellValues = $scope.retrieveCellValues();
            };

            $scope.exportToExcel = function (tableId) {
                swal('Excel File Name', {
                    content: {
                        element: 'input',
                        attributes: {
                            placeholder: '',
                            type: 'text',
                        },
                    },
                    buttons: {
                        cancel: 'Cancel',
                        confirm: 'Export',
                    },
                }).then((value) => {
                    if (value == '') {
                        swal('Error!', 'Invalid File Name.', 'error');
                    } else if (value) {
                        var exportHref = Excel.tableToExcel(tableId, 'sheet name');
                        $timeout(function () {
                            var a = document.createElement('a');
                            a.href = exportHref;
                            a.download = value + '.xls';
                            document.body.appendChild(a);
                            a.click();
                            a.remove();
                        }, 100);
                    }
                });
            };
        }
    );
});
