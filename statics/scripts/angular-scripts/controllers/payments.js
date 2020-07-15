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
                count: 15,
            },
            {
                counts: [10, 20, 30, 50, 100],
                getData: function (params) {
                    return $http.get('/api/payments/payments/').then(
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

        $scope.view = function (id) {
            $state.go('app.loans.info', { loanId: id });
        };
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
        });

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
                        check: '',
                        cash: '',
                        total: '',
                        balance: '',
                        paymentType: '',
                        checkNo: '',
                        bankACcount: '',
                        datePayment: '',
                        outStandingBalance: '',
                        remarks: '',
                        description: '',
                        paymentStatus: '2',
                        createdBy: '1',
                    };

                    // $scope.insufficient = false;
                    $scope.$watch(
                        'payment.cash',
                        function (newTerm, oldTerm) {
                            $scope.payment.total = $scope.payment.cash + $scope.payment.check;
                        },
                        true
                    );
                    $scope.$watch(
                        'payment.check',
                        function (newTerm, oldTerm) {
                            $scope.payment.total = $scope.payment.cash + $scope.payment.check;
                        },
                        true
                    );

                    $scope.$watch(
                        'payment.total',
                        function (newTerm, oldTerm) {
                            console.log(newTerm);
                            $scope.payment.balance = $scope.getBalance();
                            $scope.payment.overPayment = $scope.getOverPayment();
                            $scope.payment.outStandingBalance = $scope.getOutStandingBalance();

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

                                appFactory.getLoanPrograms($scope.borrower.borrowerId).then(function (data) {
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

        $scope.getBalance = function () {
            if ($scope.loan.currentAmortizationItem.total - $scope.payment.total <= 0) {
                return 0;
            }
            return $scope.loan.currentAmortizationItem.total - $scope.payment.total;
        };

        $scope.getOverPayment = function () {
            if ($scope.payment.total - $scope.loan.currentAmortizationItem.total <= 0) {
                return 0;
            }
            return $scope.payment.total - $scope.loan.currentAmortizationItem.total;
        };

        $scope.getOutStandingBalance = function () {
            console.log($scope.loan.currentAmortizationItem.interest);

            if ($scope.payment.total > parseFloat($scope.loan.currentAmortizationItem.total)) {
                return (
                    parseFloat($scope.loan.currentAmortizationItem.principalBalance) +
                    parseFloat($scope.loan.currentAmortizationItem.principal) -
                    $scope.payment.total +
                    parseFloat($scope.loan.currentAmortizationItem.interest) +
                    (parseFloat($scope.loan.interestBalance) - parseFloat($scope.loan.currentAmortizationItem.interest))
                );
            } else {
                return (
                    parseFloat($scope.loan.currentAmortizationItem.principalBalance) +
                    parseFloat($scope.loan.currentAmortizationItem.principal) -
                    $scope.payment.total +
                    parseFloat($scope.loan.currentAmortizationItem.interest)
                );
            }
        };
        // + parseFloat($scope.loan.currentAmortizationItem.interest)
        $scope.save = function () {
            $scope.payment.total = $scope.payment.cash + $scope.payment.check;
            $scope.payment.balance = $scope.getBalance().toFixed(2);
            $scope.payment.overPayment = $scope.getOverPayment().toFixed(2);
            $scope.payment.outStandingBalance = $scope.getOutStandingBalance().toFixed(2);

            console.log($scope.payment.balance);
            console.log($scope.payment.overPayment);
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
    });

    app.controller('DocumentAddController', function DocumentAddController(
        $http,
        $filter,
        $scope,
        toastr,
        NgTableParams,
        $state,
        $timeout
    ) {
        $scope.loan = {
            loanName: '',
            loanAmount: '',
            borrower: '',
        };

        $scope.save = function () {
            swal({
                title: 'Create Document',
                text: 'Do you want to save and create this loan?',
                icon: 'info',
                buttons: {
                    cancel: true,
                    confirm: 'Create',
                },
            }).then((isConfirm) => {
                if (isConfirm) {
                    $http.post('/api/documents/documents/', $scope.loan).then(
                        function () {
                            toastr.success('Success', 'New loan created.');
                            swal('Success!', 'New Borrower Created.', 'success');
                            $state.go('app.documents.list');
                        },
                        function (error) {
                            toastr.error(
                                'Error ' + error.status + ' ' + error.statusText,
                                'Could not create new record. Please contact System Administrator.'
                            );
                        }
                    );
                }
            });
        };
    });

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
                params: { loanId: $scope.loandId },
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

                                appFactory.getLoanPrograms($scope.borrower.borrowerId).then(function (data) {
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

                                appFactory.getLoanPrograms($scope.borrower.borrowerId).then(function (data) {
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
