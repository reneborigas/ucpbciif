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
        NgTableParams,
        $window,
        blockUI
    ) {
        $scope.searchTermAuto = {
            keyword: '',
        };

        var creditLineListBlockUI = blockUI.instances.get('creditLineListBlockUI');

        $scope.loadCreditLines = function () {
            creditLineListBlockUI.start('Loading Credit Lines...');
            $scope.tableCreditLine = new NgTableParams(
                {
                    page: 1,
                    count: 20,
                },
                {
                    counts: [10, 20, 30, 50, 100],
                    getData: function (params) {
                        return $http.get('/api/loans/creditlines/', { params: $scope.params }).then(
                            function (response) {
                                console.log(response.data);
                                var filteredData = params.filter() ? $filter('filter')(response.data, params.filter()) : response.data;
                                var orderedData = params.sorting() ? $filter('orderBy')(filteredData, params.orderBy()) : filteredData;
                                var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                params.total(response.data.length);

                                var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                creditLineListBlockUI.stop();
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
        };

        $scope.$watch(
            'searchTermAuto.keyword',
            function (newTerm, oldTerm) {
                $scope.tableCreditLine.filter({ $: newTerm });
            },
            true
        );

        $scope.loadCreditLines();

        appFactory.getLoanTerms().then(function (data) {
            $scope.terms = data;
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
                name: 'Term',
                showFilter: false,
                filterFormat: 'uppercase',
                params: {
                    param1: 'term',
                },
            },
            {
                name: 'Credit Line Amount Range',
                showFilter: false,
                filterFormat: "currency :'₱'",
                params: {
                    param1: 'creditLineAmountFrom',
                    param2: 'creditLineAmountTo',
                },
            },
            {
                name: 'Total Availment Range',
                showFilter: false,
                filterFormat: "currency :'₱'",
                params: {
                    param1: 'totalAvailmentFrom',
                    param2: 'totalAvailmentTo',
                },
            },
            {
                name: 'Interest Range',
                showFilter: false,
                filterFormat: 'staticPercentage',
                params: {
                    param1: 'interestFrom',
                    param2: 'interestTo',
                },
            },
            {
                name: 'Date Approved Range',
                showFilter: false,
                filterFormat: "date : 'mediumDate'",
                params: {
                    param1: 'dateApprovedFrom',
                    param2: 'dateApprovedTo',
                },
            },
            {
                name: 'Expiry Date Range',
                showFilter: false,
                filterFormat: "date : 'mediumDate'",
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
            $scope.loadCreditLines();
        };

        $scope.resetFilter = function () {
            angular.forEach($scope.filters, function (filter) {
                filter.showFilter = false;
            });
            $scope.showFilterButton = false;
            $scope.params = {};
            $scope.loadCreditLines();
        };

        $scope.view = function (creditLineId) {
            $state.go('app.creditline.info', { creditLineId: creditLineId });
        };

        $scope.retrieveHeaders = function () {
            var headers = [];
            var ngTable = document.getElementById('tableCreditLine');
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
            var ngTable = document.getElementById('tableCreditLine');
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
            $popup.title = 'Credit Line List';
            $popup.dateToday = new Date();
            $popup.user = $scope.loadCurrentUserInfo();
            $popup.filters = filters;
            $popup.headers = $scope.retrieveHeaders();
            $popup.cellValues = $scope.retrieveCellValues();
        };
    });

    app.controller('CreditLineInfoController', function CreditLineInfoController(
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
            .get('/api/loans/creditlines/', {
                params: { creditLineId: $scope.creditLineId },
            })
            .then(
                function (response) {
                    $scope.creditLine = response.data[0];

                    $http
                        .get('/api/borrowers/borrowers/', {
                            params: { borrowerId: $scope.creditLine.borrower },
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
                                        params: { creditLineId: $scope.creditLine.id, subProcessName: 'Credit Line Approval' },
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

                                $http
                                    .get('/api/loans/loans/', {
                                        params: { creditLineId: $scope.creditLine.id },
                                    })
                                    .then(
                                        function (response) {
                                            $scope.loans = response.data;
                                        },
                                        function (error) {
                                            toastr.error(
                                                'Error ' + error.status + ' ' + error.statusText,
                                                'Could not retrieve Loans. Please contact System Administrator.'
                                            );
                                        }
                                    );

                                // $scope.loadNotes();
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
                            'Could not retrieve Amortization Information. Please contact System Administrator.'
                        );
                    }
                );

            console.log($scope.currentAmortization);
        };
        $scope.viewLoan = function (id) {
            $state.go('app.loans.info', { loanId: id });
        };
        $scope.loadNotes = function () {
            return appFactory.getContentTypeId('note').then(function (data) {
                return appFactory.getNotes($scope.loanId, data).then(function (response) {
                    $scope.notes = response;
                });
            });
        };

        $scope.newLoanAvailment = function (borrowerId, creditLineId) {
            $state.go('app.borrowers.create_loan_availment', { borrowerId: borrowerId, creditLineId: creditLineId });
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

        var amortizationSchedulePaymentBlockUI = blockUI.instances.get('amortizationSchedulePaymentBlockUI');

        $scope.viewAmortizationPayment = function (amortizationItemId) {
            $scope.showAmortizationSchedule = false;
            angular.element('#amortization-payment').modal('show');
            amortizationSchedulePaymentBlockUI.start('Fetching Amortization Payment Schedule...');
            $http
                .get('/api/loans/amortizationitems/', {
                    params: { amortizationItemId: amortizationItemId },
                })
                .then(
                    function (response) {
                        $scope.amortizationItem = response.data[0];
                        $timeout(function () {
                            $scope.showAmortizationSchedule = true;
                            amortizationSchedulePaymentBlockUI.stop();
                        }, 1000);
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Loan Information. Please contact System Administrator.'
                        );
                    }
                );
        };
        $scope.restructureAmortization = function (id) {
            $state.go('app.loans.restructeamortization', { loanId: id });
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
                    .post('/api/loans/updatecreditlineview/', {
                        creditLineId: $scope.update.id,
                        security: $scope.update.note,
                    })
                    .then(
                        function (response) {
                            angular.element('#edit-purpose-security').modal('hide');
                            $('body').removeClass('modal-open');
                            $('.modal-backdrop').remove();
                            $scope.creditLine.security = response.data.new_value;
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
                    .post('/api/loans/updatecreditlineview/', {
                        creditLineId: $scope.update.id,
                        purpose: $scope.update.note,
                    })
                    .then(
                        function (response) {
                            angular.element('#edit-purpose-security').modal('hide');
                            $('body').removeClass('modal-open');
                            $('.modal-backdrop').remove();
                            $scope.creditLine.purpose = response.data.new_value;
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

        $scope.editReleaseDate = function (id, dateReleased) {
            $scope.update.id = id;
            $scope.update.releaseDate = new Date(dateReleased);
            angular.element('#edit-release-date').modal('show');
        };

        $scope.updateReleaseDate = function () {
            $http
                .post('/api/loans/updateloanview/', {
                    loanId: $scope.update.id,
                    dateReleased: $scope.update.releaseDate,
                })
                .then(
                    function (response) {
                        angular.element('#edit-release-date').modal('hide');
                        $('body').removeClass('modal-open');
                        $('.modal-backdrop').remove();
                        $state.reload();
                        toastr.success('Success', 'Date Released updated.');
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not update date released. Please contact System Administrator.'
                        );
                    }
                );
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
});
