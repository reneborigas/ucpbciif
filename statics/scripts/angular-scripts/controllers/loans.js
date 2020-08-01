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
        appFactory,
        $window
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
                filterFormat: "date : 'mediumDate'",
                params: {
                    param1: 'dateFrom',
                    param2: 'dateTo',
                },
            },
            {
                name: 'Loan Range',
                showFilter: false,
                filterFormat: "currency :'₱'",
                params: {
                    param1: 'loanFrom',
                    param2: 'loanTo',
                },
            },
            {
                name: 'Window',
                showFilter: false,
                filterFormat: 'uppercase',
                params: {
                    param1: 'loanProgramName',
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

        $scope.retrieveHeaders = function () {
            var headers = [];
            var ngTable = document.getElementById('tableLoans');
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
            var ngTable = document.getElementById('tableLoans');
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
            if ($scope.searchTermAuto) {
                filters.push({
                    name: 'Search',
                    filterFormat: 'uppercase',
                    params: { input: $scope.searchTermAuto },
                });
            }
            var $popup = $window.open('/print/loans', '_blank', 'directories=0,width=800,height=800');
            $popup.title = 'Loan List';
            $popup.user = $scope.loadCurrentUserInfo();
            $popup.filters = filters;
            $popup.headers = $scope.retrieveHeaders();
            $popup.cellValues = $scope.retrieveCellValues();
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
        $scope.goToFile = function (subProcessName, documentId) {
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

        $scope.update = function () {
            if ($scope.modalTitle == 'Security') {
                $http
                    .post('/api/loans/updateloanview/', {
                        loanId: $scope.update.id,
                        security: $scope.update.note,
                    })
                    .then(
                        function (response) {
                            angular.element('#edit-purpose-security').modal('hide');
                            $('body').removeClass('modal-open');
                            $('.modal-backdrop').remove();
                            $scope.loan.security = response.data.new_value;
                            toastr.success('Success', 'Loan Security updated.');
                        },
                        function (error) {
                            toastr.error(
                                'Error ' + error.status + ' ' + error.statusText,
                                'Could not update document. Please contact System Administrator.'
                            );
                        }
                    );
            } else {
                $http
                    .post('/api/loans/updateloanview/', {
                        loanId: $scope.update.id,
                        purpose: $scope.update.note,
                    })
                    .then(
                        function (response) {
                            angular.element('#edit-purpose-security').modal('hide');
                            $('body').removeClass('modal-open');
                            $('.modal-backdrop').remove();
                            $scope.loan.purpose = response.data.new_value;
                            toastr.success('Success', 'Loan Purpose updated.');
                        },
                        function (error) {
                            toastr.error(
                                'Error ' + error.status + ' ' + error.statusText,
                                'Could not update document. Please contact System Administrator.'
                            );
                        }
                    );
            }
        };

        $scope.edit = function (id, value, title) {
            $scope.update.id = id;
            $scope.modalTitle = title;
            $scope.update.note = value;
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
