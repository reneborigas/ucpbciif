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
                count: 15,
            },
            {
                counts: [10, 20, 30, 50, 100],
                getData: function (params) {
                    return $http
                        .get('/api/loans/loans/')
                        .then(
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

        $scope.view = function ( id) {
            
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
                params: {  loanId: $scope.loanId },
            })
            .then(
                function (response) {
                    $scope.loan = response.data[0];
                    $scope.currentAmortization = $scope.loan.amortizations[0];
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

        

        $scope.newPayment = function ( id) { 
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

        
        $scope.loadAmortization = function (id) { 

              $http
              .get('/api/loans/amortizations/', {
                  params: { amortizationId: id },
              })
              .then(
                  function (response) { 
                      $scope.currentAmortization= response.data[0];
                  },
                  function (error) {
                      toastr.error(
                          'Error ' + error.status + ' ' + error.statusText,
                          'Could not retrieve Amortizaion Information. Please contact System Administrator.'
                      );
                  }
              );
              
              console.log(  $scope.currentAmortization);
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



                        $http
                        .get('/api/loans/loans/', {
                            params: { borrowerId: $scope.loan.borrower,status:'RELEASED' },
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
