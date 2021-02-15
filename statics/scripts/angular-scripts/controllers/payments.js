define(function () {
    'use strict';

    var app = angular.module('app');

    app.controller(
        'PaymentListController',
        function PaymentListController($http, $filter, $scope, toastr, NgTableParams, $state, $timeout, appFactory, $window, blockUI) {
            $scope.searchTermAuto = {
                keyword: '',
            };

            var paymentListBlockUI = blockUI.instances.get('paymentListBlockUI');

            $scope.loadPayments = function () {
                paymentListBlockUI.start('Loading Payments...');
                $scope.tablePayments = new NgTableParams(
                    {
                        page: 1,
                        count: 20,
                    },
                    {
                        counts: [10, 20, 30, 50, 100],
                        getData: function (params) {
                            return $http.get('/api/payments/payments/', { params: $scope.params }).then(
                                function (response) {
                                    var filteredData = params.filter() ? $filter('filter')(response.data, params.filter()) : response.data;
                                    var orderedData = params.sorting() ? $filter('orderBy')(filteredData, params.orderBy()) : filteredData;
                                    var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                    params.total(response.data.length);

                                    var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                    paymentListBlockUI.stop();
                                    return page;
                                },
                                function (error) {
                                    paymentListBlockUI.stop();
                                    toastr.error(
                                        'Error ' + error.status + ' ' + error.statusText,
                                        'Could not Load Payments. Please contact System Administrator.'
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
                    $scope.tablePayments.filter({ $: newTerm });
                },
                true
            );

            $scope.loadPayments();

            appFactory.getPaymentStatus().then(function (data) {
                $scope.paymentStatuses = data;
            });

            appFactory.getPaymentType().then(function (data) {
                $scope.paymentTypes = data;
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
                    name: 'Principal Payment Range',
                    showFilter: false,
                    filterFormat: "currency :'₱'",
                    params: {
                        param1: 'principalFrom',
                        param2: 'principalTo',
                    },
                },
                {
                    name: 'Interest Payment Range',
                    showFilter: false,
                    filterFormat: "currency :'₱'",
                    params: {
                        param1: 'interestFrom',
                        param2: 'interestTo',
                    },
                },
                {
                    name: 'Accrued Interest Payment Range',
                    showFilter: false,
                    filterFormat: "currency :'₱'",
                    params: {
                        param1: 'interestFrom',
                        param2: 'interestTo',
                    },
                },
                {
                    name: 'Payment Date Range',
                    showFilter: false,
                    filterFormat: "date : 'mediumDate'",
                    params: {
                        param1: 'paymentDateFrom',
                        param2: 'paymentDateTo',
                    },
                },
                {
                    name: 'Total Payment Range',
                    showFilter: false,
                    filterFormat: "currency :'₱'",
                    params: {
                        param1: 'totalPaymentFrom',
                        param2: 'totalPaymentTo',
                    },
                },
                {
                    name: 'Payment Type',
                    showFilter: false,
                    filterFormat: 'uppercase',
                    params: {
                        param1: 'paymentType',
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
                $scope.loadPayments();
            };

            $scope.resetFilter = function () {
                angular.forEach($scope.filters, function (filter) {
                    filter.showFilter = false;
                });
                $scope.showFilterButton = false;
                $scope.params = {};
                $scope.loadPayments();
            };

            $scope.viewLoan = function (id) {
                $state.go('app.loans.info', { loanId: id });
            };

            $scope.viewBorrower = function (id) {
                $state.go('app.borrowers.info', { borrowerId: id });
            };

            $scope.retrieveHeaders = function () {
                var headers = [];
                var ngTable = document.getElementById('tablePayments');
                var rowLength = ngTable.rows.length;

                for (var i = 0; i < rowLength; i++) {
                    var ngCells = ngTable.rows.item(i).cells;
                    var cellLength = ngCells.length;

                    for (var j = 0; j < cellLength; j++) {
                        var cellTitle = ngCells.item(j).getAttribute('data-title');
                        if (cellTitle) {
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
                var ngTable = document.getElementById('tablePayments');
                var rowLength = ngTable.rows.length;

                for (var i = 2; i < rowLength; i++) {
                    var ngCells = ngTable.rows.item(i).cells;
                    var cellLength = ngCells.length;
                    var cells = [];
                    for (var j = 0; j < cellLength; j++) {
                        cells.push(ngCells.item(j).innerText);
                    }
                    values.push(cells);
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
                var $popup = $window.open('/print/payments', '_blank', 'directories=0,width=800,height=800');
                $popup.title = 'Payment List';
                $popup.dateToday = new Date();
                $popup.user = $scope.loadCurrentUserInfo();
                $popup.filters = filters;
                $popup.headers = $scope.retrieveHeaders();
                $popup.cellValues = $scope.retrieveCellValues();
            };
        }
    );

    app.controller(
        'NewPaymentController',
        function NewPaymentController($http, $filter, $scope, toastr, NgTableParams, appFactory, $state, $timeout, blockUI, $q, $window) {
            appFactory.getPaymentType().then(function (data) {
                $scope.paymentTypes = data;

                console.log($scope.loanId);
                $http
                    .get('/api/loans/loans/', {
                        params: { loanId: $scope.loanId },
                    })
                    .then(
                        function (response) {
                            $scope.loan = response.data[0];

                            $scope.payment = {
                                loan: $scope.loan.id,
                                amortization: $scope.loan.latestAmortization.id,
                                amortizationItem: $scope.loan.currentAmortizationItem.id,
                                principal: '0',
                                days: '0',
                                interest: '0',
                                totalToPay: '0',
                                principalBalance: '0',
                                check: '0',
                                cash: '0',
                                total: '0',
                                balance: '',
                                paymentType: $scope.paymentTypes[1].id,
                                checkNo: '',
                                interestPayment: '0',
                                penaltyPayment: '0',
                                principalPayment: '0',
                                exemptAdditionalInterest: '0',
                                exemptPenalty: '0',
                                bankACcount: '',
                                datePayment: new Date($scope.loan.currentAmortizationItem.schedule),
                                outStandingBalance: '',
                                remarks: '',
                                description: '',
                                paymentStatus: '2',
                                createdBy: '1',
                            };
                            $scope.payment.cash = 0;
                            $scope.payment.check = 0;
                            console.log($scope.payment.paymentType);

                            $scope.$watch(
                                'payment.datePayment',
                                function (newTerm, oldTerm) {
                                    console.log(newTerm.toLocaleDateString());
                                    $scope.payment.cash = 0;
                                    $scope.payment.check = 0;
                                    $scope.payment.interestPayment = 0;
                                    $scope.payment.penaltyPayment = 0;
                                    $scope.payment.paymentFromOverPayment = 0;
                                    $http
                                        .post('/api/processes/calculatepmt/', {
                                            params: {
                                                datePayment: newTerm.toLocaleDateString(),
                                                loanId: $scope.payment.loan,
                                                dateSchedule: new Date($scope.loan.currentAmortizationItem.schedule).toLocaleDateString(),
                                            },
                                        })
                                        .then(
                                            function (response) {
                                                console.log(response.data);
                                                $scope.newAmortization = response.data;
                                                $scope.payment.isPaymentExtension = false;
                                                $scope.isPaymentExtensionButton = 'Apply Payment Extensions';

                                                $scope.payment.days = $scope.newAmortization.days;
                                                $scope.payment.principal = $scope.newAmortization.principal;
                                                $scope.payment.interest = $scope.newAmortization.interest;
                                                $scope.payment.accruedInterest = $scope.newAmortization.accruedInterest;

                                                $scope.payment.totalInterest = $scope.newAmortization.totalInterest;
                                                $scope.payment.currentOverPayment = $scope.newAmortization.totalOverPayment;

                                                $scope.payment.totalToPay = $scope.newAmortization.totalToPay;
                                                $scope.payment.totalToPayWithPenalty = $scope.newAmortization.totalToPayWithPenalty;
                                                $scope.payment.daysExceed = $scope.newAmortization.daysExceed;
                                                $scope.payment.daysAdvanced = $scope.newAmortization.daysAdvanced;
                                                $scope.payment.principalBalance = $scope.newAmortization.principalBalance;

                                                $scope.payment.additionalInterest = $scope.newAmortization.additionalInterest;
                                                $scope.payment.penalty = $scope.newAmortization.penalty;
                                                $scope.payment.total =
                                                    parseFloat($scope.payment.cash) +
                                                    parseFloat($scope.payment.check) +
                                                    parseFloat($scope.payment.interestPayment) +
                                                    parseFloat($scope.payment.accruedInterestPayment) +
                                                    // parseFloat($scope.payment.paymentFromOverPayment) +
                                                    parseFloat($scope.payment.penaltyPayment);
                                                // check
                                                if ($scope.payment.paymentType == 2) {
                                                    $scope.payment.check = $scope.payment.principal.toFixed(2);
                                                } else {
                                                    $scope.payment.cash = $scope.payment.principal.toFixed(2);
                                                }

                                                $scope.payment.interestPayment =
                                                    $scope.payment.totalInterest.toFixed(2) - $scope.payment.accruedInterest.toFixed(2);
                                                $scope.payment.penaltyPayment = $scope.payment.penalty;
                                                $scope.payment.accruedInterestPayment = $scope.payment.accruedInterest.toFixed(2);
                                                $scope.payment.total = parseFloat($scope.payment.total);
                                                $scope.payment.interestBalance = $scope.getInterestBalance().toFixed(2);
                                                $scope.payment.penaltyBalance = $scope.getPenaltyBalance().toFixed(2);
                                                $scope.payment.balance = $scope.getBalance();

                                                $scope.payment.overPayment = $scope.getOverPayment();
                                                $scope.payment.outStandingBalance = parseFloat($scope.getOutStandingBalance()).toFixed(2);
                                            },
                                            function (error) {
                                                toastr.error(
                                                    'Error ' + error.status + ' ' + error.statusText,
                                                    'Could not calculate amortization. Please contact System Administrator.'
                                                );
                                            }
                                        );
                                },
                                true
                            );
                            // $scope.insufficient = false;

                            $scope.getTotalPayment = function () {
                                $scope.payment.total =
                                    parseFloat($scope.payment.penaltyPayment) +
                                    parseFloat($scope.payment.cash) +
                                    parseFloat($scope.payment.interestPayment) +
                                    parseFloat($scope.payment.accruedInterestPayment) +
                                    parseFloat($scope.payment.paymentFromOverPayment) +
                                    parseFloat($scope.payment.check);
                            };

                            $scope.$watch(
                                'payment.cash',
                                function (newTerm, oldTerm) {
                                    $scope.getTotalPayment();
                                },
                                true
                            );
                            $scope.$watch(
                                'payment.check',
                                function (newTerm, oldTerm) {
                                    $scope.getTotalPayment();
                                },
                                true
                            );
                            $scope.$watch(
                                'payment.paymentFromOverPayment',
                                function (newTerm, oldTerm) {
                                    $scope.payment.remainingOverPayment = $scope.payment.currentOverPayment - $scope.payment.paymentFromOverPayment;
                                    $scope.getTotalPayment();
                                    console.log('asd');
                                },
                                true
                            );
                            $scope.$watch(
                                'payment.total',
                                function (newTerm, oldTerm) {
                                    console.log(newTerm);
                                    $scope.payment.balance = $scope.getBalance().toFixed(0);
                                    $scope.payment.overPayment = $scope.getOverPayment();
                                    $scope.payment.outStandingBalance = parseFloat($scope.getOutStandingBalance()).toFixed(2);
                                    $scope.payment.interestBalance = $scope.getInterestBalance().toFixed(2);
                                    $scope.payment.penaltyBalance = $scope.getPenaltyBalance().toFixed(2);
                                    console.log($scope.payment.outStandingBalance);
                                },
                                true
                            );

                            $scope.$watch(
                                'payment.penaltyPayment',
                                function (newTerm, oldTerm) {
                                    $scope.getTotalPayment();
                                },
                                true
                            );

                            $scope.$watch(
                                'payment.interestPayment',
                                function (newTerm, oldTerm) {
                                    $scope.getTotalPayment();
                                },
                                true
                            );

                            $scope.$watch(
                                'payment.total',
                                function (newTerm, oldTerm) {
                                    console.log(newTerm);
                                    $scope.payment.balance = $scope.getBalance().toFixed(0);
                                    $scope.payment.overPayment = $scope.getOverPayment();
                                    $scope.payment.outStandingBalance = parseFloat($scope.getOutStandingBalance()).toFixed(2);
                                    $scope.payment.interestBalance = $scope.getInterestBalance().toFixed(2);
                                    $scope.payment.penaltyBalance = $scope.getPenaltyBalance().toFixed(2);
                                    console.log($scope.payment.outStandingBalance);
                                },
                                true
                            );

                            $scope.$watch(
                                'payment.penaltyBalance',
                                function (newTerm, oldTerm) {
                                    console.log(newTerm);
                                    if (newTerm > 0) {
                                        $scope.payment.interestPayment = 0;
                                    }
                                },
                                true
                            );

                            $scope.$watch(
                                'payment.interestBalance',
                                function (newTerm, oldTerm) {
                                    console.log(newTerm);
                                    if (newTerm > 0) {
                                        $scope.payment.cash = 0;
                                        $scope.payment.check = 0;
                                    }
                                },
                                true
                            );

                            // $scope.$watch(
                            //     'payment.total',
                            //     function (newTerm, oldTerm) {
                            //         if (newTerm > $scope.subProcess.parentLastDocumentCreditLine.remainingCreditLine) {
                            //             //Error
                            //             console.log('invalid');

                            //             $scope.exceeded = true;
                            //         } else {
                            //             $scope.exceeded = false;
                            //         }
                            //     },
                            //     true
                            // );

                            $scope.$watch(
                                'payment.paymentType',
                                function (newTerm, oldTerm) {
                                    console.log(newTerm);
                                    $scope.payment.cash = 0;
                                    $scope.payment.check = 0;
                                    $scope.payment.checkNo = '';
                                },
                                true
                            );

                            $http
                                .get('/api/borrowers/borrowers/', {
                                    params: { borrowerId: $scope.loan.borrower },
                                })
                                .then(
                                    function (response) {
                                        $scope.borrower = response.data[0];

                                        appFactory.getLoanProgramsByid($scope.borrower.borrowerId).then(function (data) {
                                            console.log(data);
                                            $scope.windows = data;
                                        });
                                    },
                                    function (error) {
                                        toastr.error(
                                            'Error ' + error.status + ' ' + error.statusText,
                                            'Could not retrieve Borrower Information. Please contact System Administrator.'
                                        );
                                    }
                                );
                        },
                        function (error) {
                            toastr.error(
                                'Error ' + error.status + ' ' + error.statusText,
                                'Could not retrieve Loan Information. Please contact System Administrator.'
                            );
                        }
                    );
            });

            $scope.getBalance = function () {
                if (parseFloat($scope.payment.totalToPayWithPenalty) - parseFloat($scope.payment.total) <= 0) {
                    return 0;
                }
                return parseFloat($scope.payment.totalToPayWithPenalty) - parseFloat($scope.payment.total);
            };

            $scope.getInterestBalance = function () {
                if (
                    parseFloat($scope.payment.totalInterest) -
                        parseFloat($scope.payment.interestPayment) -
                        parseFloat($scope.payment.accruedInterestPayment) <=
                    0
                ) {
                    return 0;
                }
                return (
                    parseFloat($scope.payment.totalInterest) -
                    parseFloat($scope.payment.interestPayment) -
                    parseFloat($scope.payment.accruedInterestPayment)
                );
            };

            $scope.getPenaltyBalance = function () {
                if (parseFloat($scope.payment.penalty) - parseFloat($scope.payment.penaltyPayment) <= 0) {
                    return 0;
                }
                return parseFloat($scope.payment.penalty) - parseFloat($scope.payment.penaltyPayment);
            };

            $scope.getOverPayment = function () {
                if (parseFloat($scope.payment.total) - parseFloat($scope.payment.totalToPayWithPenalty) <= 0) {
                    return 0;
                }
                return (parseFloat($scope.payment.total) - parseFloat($scope.payment.totalToPayWithPenalty)).toFixed(2);
            };

            $scope.getOutStandingBalance = function () {
                console.log(parseFloat($scope.payment.total));
                console.log(parseFloat($scope.payment.totalToPay));
                if ($scope.getOverPayment() >= 1) {
                    // if (parseFloat($scope.payment.total).toFixed(2) > parseFloat($scope.payment.totalToPay).toFixed(2)) {
                    return parseFloat($scope.payment.principalBalance);
                    // parseFloat($scope.payment.principal) -
                    // parseFloat($scope.payment.total) +
                    // parseFloat($scope.payment.totalInterest) +
                    // parseFloat($scope.payment.penalty)
                    // (parseFloat($scope.loan.interestBalance) - parseFloat($scope.payment.interest))
                } else {
                    return parseFloat($scope.payment.principalBalance);
                    // parseFloat($scope.payment.principal) -
                    // parseFloat($scope.payment.total) +
                    // parseFloat($scope.payment.totalInterest) +
                    // parseFloat($scope.payment.penalty)
                }
            };
            // + parseFloat($scope.loan.currentAmortizationItem.interest)
            $scope.save = function () {
                // $scope.payment.total =
                // parseFloat($scope.payment.cash) +
                // parseFloat($scope.payment.check) +
                // parseFloat($scope.payment.interestPayment)+
                // parseFloat($scope.payment.penaltyPayment);
                $scope.payment.total = parseFloat($scope.payment.total).toFixed(2);
                // $scope.payment.outStandingBalance = parseFloat( $scope.payment.outStandingBalance).toFixed(2);
                $scope.payment.interest = parseFloat($scope.payment.interest).toFixed(2);
                $scope.payment.accruedInterest = parseFloat($scope.payment.accruedInterest).toFixed(2);
                $scope.payment.principalBalance = parseFloat($scope.payment.principalBalance).toFixed(0);
                $scope.payment.principal = parseFloat($scope.payment.principal).toFixed(2);
                $scope.payment.totalToPay = parseFloat($scope.payment.totalToPay).toFixed(2);
                $scope.payment.additionalInterest = parseFloat($scope.payment.additionalInterest).toFixed(2);
                $scope.payment.totalToPayWithPenalty = parseFloat($scope.payment.totalToPayWithPenalty).toFixed(2);
                // $scope.payment.interestBalance = parseFloat($scope.payment.interestBalance).toFixed(2);
                $scope.payment.penalty = parseFloat($scope.payment.penalty).toFixed(2);
                $scope.payment.penaltyBalance = parseFloat($scope.payment.penaltyBalance).toFixed(2);
                $scope.payment.cash = parseFloat($scope.payment.cash).toFixed(2);
                $scope.payment.check = parseFloat($scope.payment.check).toFixed(2);
                $scope.payment.interestPayment = parseFloat($scope.payment.interestPayment).toFixed(2);
                $scope.payment.accruedInterestPayment = parseFloat($scope.payment.accruedInterestPayment).toFixed(2);

                $scope.payment.penaltyPayment = parseFloat($scope.payment.penaltyPayment).toFixed(2);
                $scope.payment.balance = parseFloat($scope.payment.balance).toFixed(0);
                $scope.payment.overPayment = parseFloat($scope.payment.overPayment).toFixed(0);
                // $scope.payment.isSkipped = false
                if ($scope.loan.currentAmortizationItem.latestCheck) {
                    $scope.payment.pdc = $scope.loan.currentAmortizationItem.latestCheck.id;
                }
                $scope.payment.paymentFromOverPayment = parseFloat($scope.payment.paymentFromOverPayment).toFixed(2);
                console.log($scope.payment.paymentFromOverPayment);
                // console.log($scope.payment.overPayment);
                // console.log($scope.payment.outStandingBalance);
                console.log($scope.payment);

                // if ($scope.newPaymentForm.$valid) {
                console.log($scope.payment);
                swal({
                    title: 'Save Payment',
                    text: 'Do you want to save new payment record?',
                    icon: 'info',
                    buttons: {
                        cancel: true,
                        confirm: 'Save',
                    },
                }).then((isConfirm) => {
                    if (isConfirm) {
                        $http.post('/api/payments/payments/', $scope.payment).then(
                            function () {
                                toastr.success('Success', 'Payment Successful.');
                                swal('Success!', 'Payment Successful.', 'success');
                                $state.go('app.loans.info', { loanId: $scope.payment.loan });
                            },
                            function (error) {
                                // toastr.error(
                                //     'Error ' + error.status + ' ' + error.statusText,
                                //     'Could not create payment. Please contact System Administrator.'
                                // );
                            }
                        );
                    }
                });
                // }
            };
            $scope.skipPayment = function () {
                swal({
                    title: 'Skip Payment',
                    text: 'Continue Skipping Payment for this Amortization Schedule?',
                    icon: 'info',
                    buttons: {
                        cancel: true,
                        confirm: 'Skip Payment',
                    },
                }).then((isConfirm) => {
                    if (isConfirm) {
                        $http
                            .post('/api/payments/skippayment/', {
                                amortizationItemId: $scope.loan.currentAmortizationItem.id,
                            })
                            .then(
                                function () {
                                    toastr.success('Success', 'Skip Payment Successful.');
                                    swal('Success!', 'Skip Payment Successful.', 'success');
                                    $state.go('app.loans.info', { loanId: $scope.payment.loan });
                                },
                                function (error) {
                                    // toastr.error(
                                    //     'Error ' + error.status + ' ' + error.statusText,
                                    //     'Could not create payment. Please contact System Administrator.'
                                    // );
                                }
                            );
                    }
                });
                // }
            };

            var addPaymentBlockUI = blockUI.instances.get('addPaymentBlockUI');

            $scope.paymentExtension = function (paymentExtension) {
                if (paymentExtension == false) {
                    addPaymentBlockUI.start('Applying Payment Extension...');
                    $scope.payment.isPaymentExtension = true;
                    $scope.payment.additionalInterest = 0;
                    $scope.payment.totalInterest = $scope.newAmortization.interest;
                    $scope.payment.penalty = 0;
                    $scope.payment.interestPayment = $scope.newAmortization.interest;
                    $scope.payment.penaltyPayment = 0;
                    $scope.payment.totalToPayWithPenalty = $scope.newAmortization.totalToPay;
                    $scope.payment.exemptAdditionalInterest = parseFloat($scope.newAmortization.additionalInterest).toFixed(2);
                    $scope.payment.exemptPenalty = parseFloat($scope.newAmortization.penalty).toFixed(2);
                    $scope.isPaymentExtensionButton = 'Remove Payment Extensions';
                    addPaymentBlockUI.stop();
                } else {
                    addPaymentBlockUI.start('Removing Payment Extension...');
                    $scope.payment.datePayment = new Date($scope.loan.currentAmortizationItem.schedule);
                    $scope.payment.isPaymentExtension = false;
                    addPaymentBlockUI.stop();
                }
            };

            $scope.viewBorrower = function (id) {
                $state.go('app.borrowers.info', { borrowerId: id });
            };

            $scope.previewLoanRelease = function (id) {
                $window.open('/print/files/' + id, '_blank', 'width=800,height=800');
            };

            $scope.previewAmortizationSchedule = function (id) {
                $window.open('/print/files/amortization/' + id, '_blank', 'width=800,height=800');
            };
            $scope.cancel = function (id) {
                $state.go('app.loans.info', { loanId: id });
            };

            // OverPayment
            $scope.addAdditionalPayment = function () {
                // $scope.payment.remainingOverPayment = 0;

                angular.element('#additional-payment').modal('show');
            };

            $scope.applyOverPayment = function (paymentFromOverPayment) {
                console.log(paymentFromOverPayment);
                // $scope.payment.paymentFromOverPayment = parseFloat(overPaymentToApply).toFixed(2);
                // $scope.getTotalPayment();
                angular.element('#additional-payment').modal('hide');
            };
        }
    );

    app.controller(
        'PaymentAddController',
        function PaymentAddController($http, $filter, $scope, toastr, NgTableParams, $state, $timeout, appFactory, limitToFilter, blockUI) {
            $scope.searchTermAuto = {
                keyword: '',
            };

            var paymentAddBlockUI = blockUI.instances.get('paymentAddBlockUI');

            $scope.tableLoans = new NgTableParams(
                {
                    page: 1,
                    count: 20,
                },
                {
                    counts: [10, 20, 30, 50, 100],
                    getData: function (params) {
                        return $http.get('/api/loans/loans/', { params: { status: 'CURRENT' } }).then(
                            function (response) {
                                var filteredData = params.filter() ? $filter('filter')(response.data, params.filter()) : response.data;
                                var orderedData = params.sorting() ? $filter('orderBy')(filteredData, params.orderBy()) : filteredData;
                                var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                params.total(response.data.length);

                                var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());

                                paymentAddBlockUI.stop();
                                return page;
                            },
                            function (error) {
                                toastr.error(
                                    'Error ' + error.status + ' ' + error.statusText,
                                    'Could not Load Loans. Please contact System Administrator.'
                                );
                            }
                        );
                    },
                }
            );

            $scope.searchLoan = function (term) {
                paymentAddBlockUI.start('Loading Loans...');
                $scope.tableLoans.filter({ pnNo: term });
                if (term) {
                    $timeout(function () {
                        $scope.showTable = true;
                    }, 1000);
                } else {
                    $timeout(function () {
                        $scope.showTable = false;
                    }, 1000);
                }
            };

            $scope.addPayment = function (id, pnNo) {
                swal({
                    title: 'Process Payment',
                    text: 'Process Payment for ' + pnNo + '?',
                    icon: 'info',
                    buttons: {
                        cancel: false,
                        confirm: 'Proceed',
                    },
                }).then((isConfirm) => {
                    if (isConfirm) {
                        $state.go('app.payments.new', { loanId: id });
                    }
                });
            };
        }
    );

    app.controller(
        'LoanReleasePrintController',
        function LoanReleasePrintController($http, $filter, $scope, toastr, NgTableParams, $state, $timeout, appFactory, $window) {
            $scope.dateToday = new Date();
            $http
                .get('/api/loans/loans/', {
                    params: { loanId: $scope.loanId },
                })
                .then(
                    function (response) {
                        $scope.loan = response.data[0];

                        $http
                            .get('/api/borrowers/borrowers/', {
                                params: { borrowerId: $scope.loan.borrower },
                            })
                            .then(
                                function (response) {
                                    $scope.borrower = response.data[0];

                                    appFactory.getLoanProgramsByid($scope.borrower.borrowerId).then(function (data) {
                                        console.log(data);
                                        $scope.windows = data;
                                        $timeout(function () {
                                            $window.print();
                                        }, 500);
                                    });
                                },
                                function (error) {
                                    toastr.error(
                                        'Error ' + error.status + ' ' + error.statusText,
                                        'Could not retrieve Borrower Information. Please contact System Administrator.'
                                    );
                                }
                            );
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Loan Information. Please contact System Administrator.'
                        );
                    }
                );
        }
    );

    app.controller(
        'AmortizationSchedulePrintController',
        function DocumentAmortizationSchedulePrintController($http, $filter, $scope, toastr, NgTableParams, $state, $timeout, appFactory, $window) {
            $scope.dateToday = new Date();
            $http
                .get('/api/loans/loans/', {
                    params: { loanId: $scope.loanId },
                })
                .then(
                    function (response) {
                        $scope.loan = response.data[0];

                        $http
                            .get('/api/borrowers/borrowers/', {
                                params: { borrowerId: $scope.loan.borrower },
                            })
                            .then(
                                function (response) {
                                    $scope.borrower = response.data[0];

                                    appFactory.getLoanProgramsByid($scope.borrower.borrowerId).then(function (data) {
                                        console.log(data);
                                        $scope.windows = data;
                                        $timeout(function () {
                                            $window.print();
                                        }, 500);
                                    });
                                },
                                function (error) {
                                    toastr.error(
                                        'Error ' + error.status + ' ' + error.statusText,
                                        'Could not retrieve Borrower Information. Please contact System Administrator.'
                                    );
                                }
                            );
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Loan Information. Please contact System Administrator.'
                        );
                    }
                );
        }
    );
});
