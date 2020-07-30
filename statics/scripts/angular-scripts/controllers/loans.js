define(function () {
    'use strict';

    var app = angular.module('app');

    app.controller('LoanListController', function LoanListController(
        $http,
        $filter,
        $scope,
        toastr,
        NgTableParams,
        $state,
        $timeout,
        appFactory
    ) {
        $scope.tableLoans = new NgTableParams(
            {
                page: 1,
                count: 10,
            },
            {
                counts: [10, 20, 30, 50, 100],
                getData: function (params) {
                    return $http.get('/api/loans/loans/', { params: $scope.params }).then(
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
                                'Could not Load Loans. Please contact System Administrator.'
                            );
                        }
                    );
                },
            }
        );

        $scope.$watch(
            'searchTermAuto',
            function (newTerm, oldTerm) {
                $scope.tableLoans.filter({ $: newTerm });
            },
            true
        );

        appFactory.getLoanPrograms().then(function (data) {
            $scope.loanPrograms = data;
        });

        appFactory.getLoanStatus().then(function (data) {
            $scope.loanStatuses = data;
        });

        $scope.params = {};

        $scope.filters = [
            {
                name: 'Date Released Range',
                showFilter: false,
                params: {
                    param1: 'dateFrom',
                    param2: 'dateTo',
                },
            },
            {
                name: 'Loan Range',
                showFilter: false,
                params: {
                    param1: 'loanFrom',
                    param2: 'loanTo',
                },
            },
            {
                name: 'Window',
                showFilter: false,
                params: {
                    param1: 'loanProgram',
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
            $scope.tableLoans.reload();
        };

        $scope.resetFilter = function () {
            angular.forEach($scope.filters, function (filter) {
                filter.showFilter = false;
            });
            $scope.showFilterButton = false;
            $scope.params = {};
            $scope.tablePayments.reload();
        };

        $scope.view = function (id) {
            $state.go('app.loans.info', { loanId: id });
        };
    });

    app.controller('LoanInfoController', function LoanInfoController(
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
        $http
            .get('/api/loans/loans/', {
                params: { loanId: $scope.loanId },
            })
            .then(
                function (response) {
                    $scope.loan = response.data[0];
                    $scope.loan.outStandingBalance = parseFloat($scope.loan.outStandingBalance);
                    console.log($scope.loan.outStandingBalance <= 0);
                    $scope.currentAmortization = $scope.loan.amortizations[0];
                    $http
                        .get('/api/borrowers/borrowers/', {
                            params: { borrowerId: $scope.loan.borrower },
                        })
                        .then(
                            function (response) {
                                $scope.borrower = response.data[0];
                                $scope.showAccomodations = false;
                                appFactory.getLoanProgramsByid($scope.borrower.borrowerId).then(function (data) {
                                    console.log(data);
                                    $scope.windows = data;
                                    $scope.showAccomodations = true;
                                });

                                $http
                                .get('/api/documents/documents/', {
                                    params: { loanId: $scope.loan.id },
                                })
                                .then(
                                    function (response) {
                                        $scope.documents = response.data;
                                         
                                    },
                                    function (error) {
                                        toastr.error(
                                            'Error ' + error.status + ' ' + error.statusText,
                                            'Could not retrieve Documents. Please contact System Administrator.'
                                        );
                                    }
                                );

                                $scope.loadNotes();
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

        $scope.loadAmortization = function (id) {
            $http
                .get('/api/loans/amortizations/', {
                    params: { amortizationId: id },
                })
                .then(
                    function (response) {
                        $scope.currentAmortization = response.data[0];
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Amortizaion Information. Please contact System Administrator.'
                        );
                    }
                );

            console.log($scope.currentAmortization);
        };

        $scope.loadNotes = function () {
            return appFactory.getContentTypeId('note').then(function (data) {
                return appFactory.getNotes($scope.loanId, data).then(function (response) {
                    $scope.notes = response;
                });
            });
        };


        $scope.newLoanRelease = function (borrowerId, loanId) {
            $state.go('app.borrowers.create_loan_release', { borrowerId: borrowerId, loanId: loanId });
        };
        $scope.goToFile = function (subProcessName,documentId) {
            var subProcessNameSlug = appFactory.slugify(subProcessName);
            $state.go('app.documents.info', { subProcessName: subProcessNameSlug, documentId: documentId });
        };

        $scope.newPayment = function (id) {
            $state.go('app.payments.new', { loanId: id });
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

        $scope.previewPaymentHistory = function (id) {
            $window.open('/print/loans/payment-history/' + id, '_blank', 'width=800,height=800');
        };

        $scope.previewAmortizationHistory = function (id) {
            $window.open('/print/loans/amortization-history/' + id, '_blank', 'width=800,height=800');
        };

        $scope.previewCheckRelease = function (id) {
            $window.open('/print/loans/check/' + id, '_blank', 'width=800,height=800');
        };

        // -- Start Simple Pagination --
        $scope.currentPage = {
            notes: 0,
        };

        $scope.pageSize = {
            notes: 5,
        };
        // -- End Simple Pagination --

        var noteBlockUI = blockUI.instances.get('noteBlockUI');

        $scope.newNote = {
            noteDescription: '',
        };

        $scope.addNote = function (loan) {
            noteBlockUI.start('Adding Note...');
            $scope.note = {
                committee: 1, //default commiitee to be replaced with
                object_type: 'Loan',
                object_id: loan.id,
                content_type: '',
                note: $scope.newNote.noteDescription,
            };
            return appFactory.getContentTypeId('note').then(function (data) {
                $scope.note.content_type = data;
                console.log($scope.note);
                return $http.post('/api/committees/notes/', $scope.note).then(
                    function () {
                        toastr.success('Success', 'Note added succesfully.');
                        $scope.loadNotes();

                        $scope.newNote.noteDescription = '';
                        noteBlockUI.stop();
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not create new record. Please contact System Administrator.'
                        );
                        noteBlockUI.stop();
                    }
                );
            });
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

                    $http
                        .get('/api/loans/loans/', {
                            params: { borrowerId: $scope.loan.borrower, status: 'CURRENT' },
                        })
                        .then(
                            function (response) {
                                $scope.loans = response.data;
                            },
                            function (error) {
                                toastr.error(
                                    'Error ' + error.status + ' ' + error.statusText,
                                    'Could not retrieve Loans Information. Please contact System Administrator.'
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

    app.controller('CheckReleasePrintController', function CheckReleasePrintController(
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
                    $scope.loanAmountWords = appFactory.convertAmountToWords(response.data[0].amount);
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

                    $http
                        .get('/api/loans/loans/', {
                            params: { borrowerId: $scope.loan.borrower, status: 'CURRENT' },
                        })
                        .then(
                            function (response) {
                                $scope.loans = response.data;

                                // $timeout(function () {
                                //     $window.print();
                                // }, 500);
                            },
                            function (error) {
                                toastr.error(
                                    'Error ' + error.status + ' ' + error.statusText,
                                    'Could not retrieve Loans Information. Please contact System Administrator.'
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

    app.controller('AmortizationHistoryPrintController', function AmortizationHistoryPrintController(
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
                                });
                            },
                            function (error) {
                                toastr.error(
                                    'Error ' + error.status + ' ' + error.statusText,
                                    'Could not retrieve Borrower Information. Please contact System Administrator.'
                                );
                            }
                        );

                    $http
                        .get('/api/loans/loans/', {
                            params: { borrowerId: $scope.loan.borrower, status: 'CURRENT' },
                        })
                        .then(
                            function (response) {
                                $scope.loans = response.data;

                                // $timeout(function () {
                                //     $window.print();
                                // }, 500);
                            },
                            function (error) {
                                toastr.error(
                                    'Error ' + error.status + ' ' + error.statusText,
                                    'Could not retrieve Loans Information. Please contact System Administrator.'
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

        $scope.loadAmortization = function (id) {
            $http
                .get('/api/loans/amortizations/', {
                    params: { amortizationId: id },
                })
                .then(
                    function (response) {},
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Amortizaion Information. Please contact System Administrator.'
                        );
                    }
                );

            console.log($scope.currentAmortization);
        };
    });

    app.controller('AmortizationSchedulePrintController', function AmortizationSchedulePrintController(
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
