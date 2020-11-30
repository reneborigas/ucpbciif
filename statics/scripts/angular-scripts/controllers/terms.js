define(function () {
    'use strict';

    var app = angular.module('app');

    app.controller(
        'TermsListController',
        function TermsListController($http, $filter, $scope, $state, $timeout, toastr, appFactory, NgTableParams, blockUI) {
            $scope.searchTermAuto = {
                keyword: '',
            };

            var termListBlockUI = blockUI.instances.get('termListBlockUI');

            $scope.loadTerms = function () {
                termListBlockUI.start('Loading Terms...');
                $scope.tableTerms = new NgTableParams(
                    {
                        page: 1,
                        count: 20,
                    },
                    {
                        counts: [10, 20, 30, 50, 100],
                        getData: function (params) {
                            return $http.get('/api/loans/terms/').then(
                                function (response) {
                                    var filteredData = params.filter() ? $filter('filter')(response.data, params.filter()) : response.data;
                                    var orderedData = params.sorting() ? $filter('orderBy')(filteredData, params.orderBy()) : filteredData;
                                    var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                    params.total(response.data.length);

                                    var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                    termListBlockUI.stop();
                                    return page;
                                },
                                function (error) {
                                    termListBlockUI.stop();
                                    toastr.error(
                                        'Error ' + error.status + ' ' + error.statusText,
                                        'Could not load Term List. Please contact System Administrator.'
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
                    $scope.tableTerms.filter({ $: newTerm });
                },
                true
            );

            $scope.loadTerms();

            $scope.view = function (termId) {
                $state.go('app.terms.info', { termId: termId });
            };
        }
    );

    app.controller('TermsAddController', function TermsAddController($http, $filter, $scope, $state, $timeout, toastr, appFactory, NgTableParams) {
        $http.get('/api/loans/paymentperiods/').then(function (response) {
            $scope.paymentperiods = response.data;
        });

        $scope.term = {
            name: '',
            days: '',
            principalPaymentPeriod: '',
            interestPaymentPeriod: '',
            remarks: '',
        };

        $scope.createTerm = function () {
            console.log($scope.term);
            swal({
                title: 'Create Term',
                text: 'Do you want to save and create this term?',
                icon: 'info',
                buttons: {
                    cancel: true,
                    confirm: 'Create',
                },
            }).then((isConfirm) => {
                if (isConfirm) {
                    $http.post('/api/loans/crud-terms/', $scope.term).then(
                        function (response) {
                            console.log(response.data);
                            var user = JSON.parse(localStorage.getItem('currentUser'));
                            var userLogs = {
                                user: user['id'],
                                action_type: 'Created', //String value of action i.e. Created, Updated, Approved, Complete etc.
                                content_type: '', //value return by appFactory, model name i.e. committee, documentmovement, steps etc.
                                object_id: response.data.id, //ID of object created i.e. borrowerId, id etc.
                                object_type: 'Term', //String value to display on viewing i.e. Committee Member, Document etc
                                apiLink: '/api/loans/terms', //api link to access object_id. if object_id = borrowerId, then apiLInk = /api/borrowers/borrowers
                                valueToDisplay: 'name', //field value on api link to display. if object_id = borrowerId, apiLInk = /api/borrowers/borrowers, then  borrowerName
                                logDetails: [
                                    {
                                        action: 'Created ' + response.data.name, //Details of Log
                                    },
                                ],
                            };
                            return appFactory.getContentTypeId('term').then(function (data) {
                                userLogs.content_type = data;
                                return $http.post('/api/users/userlogs/', userLogs).then(
                                    function () {
                                        swal('Success!', 'New Term Created.', 'success');
                                        toastr.success('Success', 'New Term Created.');
                                        $state.go('app.terms.list');
                                    },
                                    function (error) {
                                        toastr.error(
                                            'Error ' + error.status + ' ' + error.statusText,
                                            'Could not record logs.  Please contact System Administrator'
                                        );
                                    }
                                );
                            });
                        },
                        function (error) {
                            toastr.error(
                                'Error ' + error.status + ' ' + error.statusText,
                                'Could not create new term. Please contact System Administrator.'
                            );
                        }
                    );
                }
            });
        };
    });

    app.controller('TermsInfoController', function TermsInfoController($http, $filter, $scope, $state, $timeout, toastr, appFactory, NgTableParams) {
        $http
            .get('/api/loans/terms/', {
                params: { termId: $scope.termId },
            })
            .then(
                function (response) {
                    $scope.term = response.data[0];
                },
                function (error) {
                    toastr.error(
                        'Error ' + error.status + ' ' + error.statusText,
                        'Could not retrieve Term Information. Please contact System Administrator.'
                    );
                }
            );
    });
});
