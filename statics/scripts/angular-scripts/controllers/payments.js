define(function () {
    'use strict';

    var app = angular.module('app');

    app.controller('PaymentListController', function LoanListController(
        $http,
        $filter,
        $scope,
        toastr,
        NgTableParams,
        $state,
        $timeout,
        appFactory
    ) {
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
                                'Could not Load Payments. Please contact System Administrator.'
                            );
                        }
                    );
                },
            }
        );

        $scope.$watch(
            'searchTermAuto',
            function (newTerm, oldTerm) {
                $scope.tablePayments.filter({ $: newTerm });
            },
            true
        );

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
                params: {
                    param1: 'borrowerId',
                },
            },
            {
                name: 'Principal Range',
                showFilter: false,
                params: {
                    param1: 'principalFrom',
                    param2: 'principalTo',
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
                name: 'Payment Date Range',
                showFilter: false,
                params: {
                    param1: 'paymentDateFrom',
                    param2: 'paymentDateTo',
                },
            },
            {
                name: 'Total Payment Range',
                showFilter: false,
                params: {
                    param1: 'totalPaymentFrom',
                    param2: 'totalPaymentTo',
                },
            },
            {
                name: 'Payment Type',
                showFilter: false,
                params: {
                    param1: 'paymentType',
                },
            },
            {
                name: 'Status',
                showFilter: false,
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
            $scope.tablePayments.reload();
        };

        $scope.resetFilter = function () {
            angular.forEach($scope.filters, function (filter) {
                filter.showFilter = false;
            });
            $scope.showFilterButton = false;
            $scope.params = {};
            $scope.tablePayments.reload();
        };

        $scope.viewLoan = function (id) {
            $state.go('app.loans.info', { loanId: id });
        };

        $scope.viewBorrower = function (id) {
            $state.go('app.borrowers.info', { borrowerId: id });
        };

        $scope.$watch(
            'searchTermAuto',
            function (newTerm, oldTerm) {
                $scope.tablePayments.filter({ $: newTerm });
            },
            true
        );
    });

    app.controller('NewPaymentController', function NewPaymentController(
        $http,
        $filter,
        $scope,
        toastr,
        NgTableParams,
        appFactory,
        $state,
        $timeout,
        blockUI,
        $q,
        $window
    ) {
        appFactory.getPaymentType().then(function (data) {
            $scope.paymentTypes = data;


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
                        bankACcount: '',
                        datePayment: new Date($scope.loan.currentAmortizationItem.schedule),
                        outStandingBalance: '',
                        remarks: '',
                        description: '',
                        paymentStatus: '2',
                        createdBy: '1',
                    };

                    console.log($scope.payment.paymentType);
                   
            
                    $scope.$watch(
                        'payment.datePayment',
                        function (newTerm, oldTerm) {
                            console.log($scope.payment.loan);
                            console.log(new Date($scope.loan.currentAmortizationItem.schedule).toLocaleDateString());
                            $http
                                .post('/api/processes/calculatepmt/', {
                                    params: {
                                        datePayment: newTerm.toLocaleDateString(),
                                        loanId: $scope.payment.loan,  
                                        dateSchedule: new Date(
                                            $scope.loan.currentAmortizationItem.schedule
                                        ).toLocaleDateString(),
                                    },
                                })
                                .then(
                                    function (response) {
                                        console.log(response.data);
                                        $scope.newAmortization = response.data;

                                        $scope.payment.days = $scope.newAmortization.days;
                                        $scope.payment.principal = $scope.newAmortization.principal;
                                        $scope.payment.interest = $scope.newAmortization.interest;
                                        $scope.payment.totalToPay = $scope.newAmortization.totalToPay;
                                        $scope.payment.principalBalance = $scope.newAmortization.principalBalance;

                                        $scope.payment.total =
                                            parseFloat($scope.payment.cash) +
                                            parseFloat($scope.payment.check) +
                                            parseFloat($scope.payment.interestPayment);
                                        $scope.payment.total = parseFloat($scope.payment.total);
                                        $scope.payment.balance = $scope.getBalance();
                                        $scope.payment.overPayment = $scope.getOverPayment();
                                        $scope.payment.outStandingBalance = parseFloat(
                                            $scope.getOutStandingBalance()
                                        ).toFixed(2);
                                    },
                                    function (error) {
                                        toastr.error(
                                            'Error ' + error.status + error.statusText,
                                            'Could not calculate amortization. Please contact System Administrator.'
                                        );
                                    }
                                );
                        },
                        true
                    );
                    // $scope.insufficient = false;
                    $scope.$watch(
                        'payment.cash',
                        function (newTerm, oldTerm) {
                            $scope.payment.total =
                                parseFloat($scope.payment.cash) +
                                parseFloat($scope.payment.interestPayment) +
                                parseFloat($scope.payment.check);
                        },
                        true
                    );
                    $scope.$watch(
                        'payment.check',
                        function (newTerm, oldTerm) {
                            $scope.payment.total =
                                parseFloat($scope.payment.cash) +
                                parseFloat($scope.payment.interestPayment) +
                                parseFloat($scope.payment.check);
                        },
                        true
                    );

                    $scope.$watch(
                        'payment.interestPayment',
                        function (newTerm, oldTerm) {
                            $scope.payment.total =
                                parseFloat($scope.payment.cash) +
                                parseFloat($scope.payment.interestPayment) +
                                parseFloat($scope.payment.check);
                        },
                        true
                    );

                    $scope.$watch(
                        'payment.total',
                        function (newTerm, oldTerm) {
                            console.log(newTerm);
                            $scope.payment.balance = $scope.getBalance();
                            $scope.payment.overPayment = $scope.getOverPayment();
                            $scope.payment.outStandingBalance = parseFloat($scope.getOutStandingBalance()).toFixed(2);

                            console.log($scope.payment.outStandingBalance);
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
            if (parseFloat($scope.payment.totalToPay) - parseFloat($scope.payment.total) <= 0) {
                return 0;
            }
            return parseFloat($scope.payment.totalToPay) - parseFloat($scope.payment.total);
        };

        $scope.getOverPayment = function () {
            if (parseFloat($scope.payment.total) - parseFloat($scope.payment.totalToPay) <= 0) {
                return 0;
            }
            return parseFloat($scope.payment.total) - parseFloat($scope.payment.totalToPay);
        };

        $scope.getOutStandingBalance = function () {
            console.log(parseFloat($scope.payment.total));
            console.log(parseFloat($scope.payment.totalToPay));
            if ($scope.getOverPayment().toFixed(2) >= 1) {
                // if (parseFloat($scope.payment.total).toFixed(2) > parseFloat($scope.payment.totalToPay).toFixed(2)) {
                return (
                    parseFloat($scope.payment.principalBalance) +
                    parseFloat($scope.payment.principal) -
                    parseFloat($scope.payment.total) +
                    parseFloat($scope.payment.interest) +
                    (parseFloat($scope.loan.interestBalance) - parseFloat($scope.payment.interest))
                );
            } else {
                return (
                    parseFloat($scope.payment.principalBalance) +
                    parseFloat($scope.payment.principal) -
                    parseFloat($scope.payment.total) +
                    parseFloat($scope.payment.interest)
                );
            }
        };
        // + parseFloat($scope.loan.currentAmortizationItem.interest)
        $scope.save = function () {
            $scope.payment.total =
                parseFloat($scope.payment.cash) +
                parseFloat($scope.payment.check) +
                parseFloat($scope.payment.interestPayment);
            $scope.payment.total = parseFloat($scope.payment.total).toFixed(2);
            $scope.payment.balance = parseFloat($scope.getBalance()).toFixed(2);
            $scope.payment.overPayment = parseFloat($scope.getOverPayment()).toFixed(2);
            $scope.payment.outStandingBalance = parseFloat($scope.getOutStandingBalance()).toFixed(2);
            $scope.payment.interest = parseFloat($scope.payment.interest).toFixed(2);
            $scope.payment.principalBalance = parseFloat($scope.payment.principalBalance).toFixed(2);
            $scope.payment.principal = parseFloat($scope.payment.principal).toFixed(2);
            $scope.payment.totalToPay = parseFloat($scope.payment.totalToPay).toFixed(2);

            console.log($scope.payment.balance);
            console.log($scope.payment.overPayment);
            console.log($scope.payment.outStandingBalance);
            console.log($scope.payment);

            if ($scope.newPaymentDetailsForm.$valid) {
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
                                toastr.error(
                                    'Error ' + error.status + ' ' + error.statusText,
                                    'Could not create payment. Please contact System Administrator.'
                                );
                            }
                        );
                    }
                });
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
    });

    // app.controller('DocumentAddController', function DocumentAddController(
    //     $http,
    //     $filter,
    //     $scope,
    //     toastr,
    //     NgTableParams,
    //     $state,
    //     $timeout
    // ) {
    //     $scope.loan = {
    //         loanName: '',
    //         loanAmount: '',
    //         borrower: '',
    //     };

    //     $scope.save = function () {
    //         swal({
    //             title: 'Create Document',
    //             text: 'Do you want to save and create this loan?',
    //             icon: 'info',
    //             buttons: {
    //                 cancel: true,
    //                 confirm: 'Create',
    //             },
    //         }).then((isConfirm) => {
    //             if (isConfirm) {
    //                 $http.post('/api/documents/documents/', $scope.loan).then(
    //                     function () {
    //                         toastr.success('Success', 'New loan created.');
    //                         swal('Success!', 'New Borrower Created.', 'success');
    //                         $state.go('app.documents.list');
    //                     },
    //                     function (error) {
    //                         toastr.error(
    //                             'Error ' + error.status + ' ' + error.statusText,
    //                             'Could not create new record. Please contact System Administrator.'
    //                         );
    //                     }
    //                 );
    //             }
    //         });
    //     };
    // });

    app.controller('LoanReleasePrintController', function LoanReleasePrintController(
        $http,
        $filter,
        $scope,
        toastr,
        NgTableParams,
        $state,
        $timeout,
        appFactory,
        $window
    ) {
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
    });

    app.controller('AmortizationSchedulePrintController', function DocumentAmortizationSchedulePrintController(
        $http,
        $filter,
        $scope,
        toastr,
        NgTableParams,
        $state,
        $timeout,
        appFactory,
        $window
    ) {
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
    });
});
