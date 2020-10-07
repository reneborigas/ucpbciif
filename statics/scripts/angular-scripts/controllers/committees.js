define(function () {
    'use strict';

    var app = angular.module('app');

    app.controller('CommitteeOfficeListController', function CommitteeOfficeListController(
        $http,
        $filter,
        $scope,
        $state,
        $timeout,
        toastr,
        appFactory,
        NgTableParams,
        blockUI
    ) {
        $scope.searchTermAuto = {
            keyword: '',
        };

        var officeListBlockUI = blockUI.instances.get('officeListBlockUI');

        $scope.loadOffices = function () {
            officeListBlockUI.start('Loading Commitees...');
            $scope.tableOffices = new NgTableParams(
                {
                    page: 1,
                    count: 20,
                },
                {
                    counts: [10, 20, 30, 50, 100],
                    getData: function (params) {
                        return $http.get('/api/committees/offices/').then(
                            function (response) {
                                var filteredData = params.filter() ? $filter('filter')(response.data, params.filter()) : response.data;
                                var orderedData = params.sorting() ? $filter('orderBy')(filteredData, params.orderBy()) : filteredData;
                                var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                params.total(response.data.length);

                                var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                officeListBlockUI.stop();
                                return page;
                            },
                            function (error) {
                                toastr.error(
                                    'Error ' + error.status + ' ' + error.statusText,
                                    'Could not load Commitee Offices. Please contact System Administrator.'
                                );
                            }
                        );
                    },
                }
            );
        };

        $scope.loadOffices();

        $scope.$watch(
            'searchTermAuto.keyword',
            function (newTerm, oldTerm) {
                $scope.tableOffices.filter({ $: newTerm });
            },
            true
        );

        $scope.view = function (officeName) {
            var officeNameSlug = appFactory.slugify(officeName);
            $state.go('app.committees.info', { officeName: officeNameSlug });
        };
    });

    app.controller('CommitteeOfficeAddController', function CommitteeOfficeAddController(
        $http,
        $filter,
        $scope,
        $state,
        $timeout,
        toastr,
        appFactory,
        NgTableParams
    ) {
        $scope.createOffice = function (office) {
            swal({
                title: 'Create Office',
                text: 'Do you want to save and create this office?',
                icon: 'info',
                buttons: {
                    cancel: true,
                    confirm: 'Create',
                },
            }).then((isConfirm) => {
                if (isConfirm) {
                    $http.post('/api/committees/offices/', office).then(
                        function (response) {
                            var user = JSON.parse(localStorage.getItem('currentUser'));
                            var userLogs = {
                                user: user['id'],
                                action_type: 'Created', //String value of action i.e. Created, Updated, Approved, Complete etc.
                                content_type: '', //value return by appFactory, model name i.e. committee, documentmovement, steps etc.
                                object_id: response.data.id, //ID of object created i.e. borrowerId, id etc.
                                object_type: 'Office', //String value to display on viewing i.e. Committee Member, Document etc
                                apiLink: '/api/committees/offices', //api link to access object_id. if object_id = borrowerId, then apiLInk = /api/borrowers/borrowers
                                valueToDisplay: 'name', //field value on api link to display. if object_id = borrowerId, apiLInk = /api/borrowers/borrowers, then  borrowerName
                                logDetails: [
                                    {
                                        action: 'Created ' + response.data.name, //Details of Log
                                    },
                                ],
                            };
                            return appFactory.getContentTypeId('office').then(function (data) {
                                userLogs.content_type = data;
                                return $http.post('/api/users/userlogs/', userLogs).then(
                                    function () {
                                        swal('Success!', 'New Office Created.', 'success');
                                        toastr.success('Success', 'New Office Created.');
                                        $state.go('app.committees.offices');
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
                                'Could not create new office. Please contact System Administrator.'
                            );
                        }
                    );
                }
            });
        };
    });

    app.controller('CommitteeInfoController', function CommitteeInfoController(
        $http,
        $filter,
        $scope,
        $state,
        $timeout,
        toastr,
        appFactory,
        NgTableParams,
        blockUI
    ) {
        $scope.currentCommitteePosition = '';
        $scope.currentCommitteePositionName = '';

        appFactory.getOfficeId($scope.officeName).then(function (data) {
            $scope.officeId = data;
            $scope.tablePositions = new NgTableParams(
                {
                    page: 1,
                    count: 20,
                },
                {
                    counts: [10, 20, 30, 50, 100],
                    getData: function (params) {
                        return $http.get('/api/committees/positions/', { params: { officeId: data } }).then(
                            function (response) {
                                if (response.data.length > 0) {
                                    $scope.loadCommittee(response.data[0].id, response.data[0].name);
                                }
                                var filteredData = params.filter() ? $filter('filter')(response.data, params.filter()) : response.data;
                                var orderedData = params.sorting() ? $filter('orderBy')(filteredData, params.orderBy()) : filteredData;
                                var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                params.total(response.data.length);

                                var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                return page;
                            },
                            function (error) {
                                toastr.error(
                                    'Error ' + error.status + ' ' + error.statusText,
                                    'Could not load Commitee Positions for ' + $scope.officeName + '. Please contact System Administrator.'
                                );
                            }
                        );
                    },
                }
            );
        });
        var committeeBlockUI = blockUI.instances.get('committeeBlockUI');

        $scope.loadCommittee = function (positionId, positionName) {
            $scope.currentCommitteePosition = positionId;
            $scope.currentCommitteePositionName = positionName;
            committeeBlockUI.start('Loading Committee...');
            $scope.tableCommitteeMembers = new NgTableParams(
                {
                    page: 1,
                    count: 20,
                },
                {
                    counts: [10, 20, 30, 50, 100],
                    getData: function (params) {
                        return $http.get('/api/committees/committees/', { params: { positionId: positionId } }).then(
                            function (response) {
                                var filteredData = params.filter() ? $filter('filter')(response.data, params.filter()) : response.data;
                                var orderedData = params.sorting() ? $filter('orderBy')(filteredData, params.orderBy()) : filteredData;
                                var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                params.total(response.data.length);

                                var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                $timeout(function () {
                                    committeeBlockUI.stop();
                                }, 1000);

                                return page;
                            },
                            function (error) {
                                toastr.error(
                                    'Error ' + error.status + ' ' + error.statusText,
                                    'Could not load Commitee Personnel for ' + $scope.officeName + '. Please contact System Administrator.'
                                );
                                $timeout(function () {
                                    committeeBlockUI.stop();
                                }, 1000);
                            }
                        );
                    },
                }
            );
        };

        $scope.createPosition = function (position) {
            angular.element('#new-position').modal('hide');
            position.office = $scope.officeId;
            console.log(position);
            swal({
                title: 'Create Committee Position',
                text: 'Do you want to save and create this committee position?',
                icon: 'info',
                buttons: {
                    cancel: true,
                    confirm: 'Create',
                },
            }).then((isConfirm) => {
                if (isConfirm) {
                    $http.post('/api/committees/positions/', position).then(
                        function (response) {
                            var user = JSON.parse(localStorage.getItem('currentUser'));
                            var userLogs = {
                                user: user['id'],
                                action_type: 'Created', //String value of action i.e. Created, Updated, Approved, Complete etc.
                                content_type: '', //value return by appFactory, model name i.e. committee, documentmovement, steps etc.
                                object_id: response.data.id, //ID of object created i.e. borrowerId, id etc.
                                object_type: 'Committee Position', //String value to display on viewing i.e. Committee Member, Document etc
                                apiLink: '/api/committees/positions', //api link to access object_id. if object_id = borrowerId, then apiLInk = /api/borrowers/borrowers
                                valueToDisplay: 'name', //field value on api link to display. if object_id = borrowerId, apiLInk = /api/borrowers/borrowers, then  borrowerName
                                logDetails: [
                                    {
                                        action: 'Created ' + $scope.officeName + ' ' + response.data.name, //Details of Log
                                    },
                                ],
                            };
                            return appFactory.getContentTypeId('committee').then(function (data) {
                                userLogs.content_type = data;
                                return $http.post('/api/users/userlogs/', userLogs).then(
                                    function () {
                                        swal('Success!', 'New Committee Position Created.', 'success');
                                        toastr.success('Success', 'New Committee Position Created.');
                                        $scope.tablePositions.reload();
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
                                'Could not create new committee position. Please contact System Administrator.'
                            );
                        }
                    );
                }
            });
        };

        $scope.createCommittee = function (committee) {
            angular.element('#new-committee').modal('hide');
            committee.position = $scope.currentCommitteePosition;
            swal({
                title: 'Create Committee Member',
                text: 'Do you want to save and create this committee member?',
                icon: 'info',
                buttons: {
                    cancel: true,
                    confirm: 'Create',
                },
            }).then((isConfirm) => {
                if (isConfirm) {
                    $http.post('/api/committees/committees/', committee).then(
                        function (response) {
                            var user = JSON.parse(localStorage.getItem('currentUser'));
                            var userLogs = {
                                user: user['id'],
                                action_type: 'Created', //String value of action i.e. Created, Updated, Approved, Complete etc.
                                content_type: '', //value return by appFactory, model name i.e. committee, documentmovement, steps etc.
                                object_id: response.data.id, //ID of object created i.e. borrowerId, id etc.
                                object_type: 'Committee Member', //String value to display on viewing i.e. Committee Member, Document etc
                                apiLink: '/api/committees/committees', //api link to access object_id. if object_id = borrowerId, then apiLInk = /api/borrowers/borrowers
                                valueToDisplay: 'committeeName', //field value on api link to display. if object_id = borrowerId, apiLInk = /api/borrowers/borrowers, then  borrowerName
                                logDetails: [
                                    {
                                        action: 'Created ' + $scope.currentCommitteePositionName + ' ' + response.data.committeeName, //Details of Log
                                    },
                                ],
                            };
                            return appFactory.getContentTypeId('committee').then(function (data) {
                                userLogs.content_type = data;
                                return $http.post('/api/users/userlogs/', userLogs).then(
                                    function () {
                                        swal('Success!', 'New Committee Member Created.', 'success');
                                        toastr.success('Success', 'New Committee Member Created.');
                                        $scope.tablePositions.reload();
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
                                'Could not create new committee member. Please contact System Administrator.'
                            );
                        }
                    );
                }
            });
        };

        $scope.resetModalForm = function (modalName) {
            angular.element(modalName).modal('hide');
            $timeout(function () {
                $state.reload();
            }, 500);
        };

        $scope.viewMember = function (officeName, committeeId) {
            var officeNameSlug = appFactory.slugify(officeName);
            $state.go('app.committees.member', { officeName: officeNameSlug, committeeId: committeeId });
        };

        $scope.checkEmailAddress = function (emailAddress) {
            if (emailAddress) {
                $http
                    .get('/api/committees/committees/', {
                        params: { emailAddress: emailAddress },
                    })
                    .then(
                        function (response) {
                            if (response.data.length > 0) {
                                $scope.isValidEmail = false;
                            } else {
                                $scope.isValidEmail = true;
                            }
                        },
                        function (error) {
                            toastr.error(
                                'Error ' + error.status + ' ' + error.statusText,
                                'Could not retrieve Committee Email Addresses. Please contact System Administrator.'
                            );
                        }
                    );
            }
        };
    });

    app.controller('CommitteeOfficeInfoMemberController', function CommitteeOfficeInfoMemberController(
        $http,
        $filter,
        $scope,
        $state,
        $timeout,
        toastr,
        appFactory,
        NgTableParams
    ) {
        $scope.steps = [
            {
                step: 1,
                name: 'Personal Information',
                class: 'fad fa-info-circle',
                templateUrl: '/statics/partials/pages/committees/info-member/personal-information.html',
            },
            {
                step: 2,
                name: 'Account Information',
                class: 'fad fa-user-cog',
                templateUrl: '/statics/partials/pages/committees/info-member/account-information.html',
            },
            // {
            //     step: 3,
            //     name: 'Change Password',
            //     class: 'fad fa-unlock-alt',
            //     templateUrl: '/statics/partials/pages/committees/info-member/change-password.html',
            // },
        ];

        $scope.currentStep = 2;

        $scope.getStepTemplate = function () {
            for (var i = 0; i < $scope.steps.length; i++) {
                if ($scope.currentStep == $scope.steps[i].step) {
                    return $scope.steps[i].templateUrl;
                }
            }
        };

        $scope.goToStep = function (step) {
            $scope.currentStep = step;
            $scope.changeStep = true;
        };

        $scope.newUser = {
            username: 'dawin',
            email_address: '',
            password: '',
            account_type: null,
            is_active: true,
            profile: [
                {
                    name: '',
                },
            ],
        };

        $http
            .get('/api/committees/committees/', {
                params: { committeeId: $scope.committeeId },
            })
            .then(
                function (response) {
                    $scope.committee = response.data[0];
                    $scope.newUser.username = $scope.committee.committeeName.replace(/\s/g, '').toLowerCase();
                    $scope.newUser.email_address = $scope.committee.emailAddress;
                    $scope.newUser.profile[0].name = $scope.committee.committeeName;
                    appFactory.getUserAccountTypeID('Committee').then(function (data) {
                        $scope.newUser.account_type = data;
                    });
                    if ($scope.committee.user) {
                        $http
                            .get('/api/users/users/', {
                                params: { id: $scope.committee.user },
                            })
                            .then(
                                function (response) {
                                    $scope.committeeUserAccount = response.data[0];
                                },
                                function (error) {
                                    toastr.error(
                                        'Error ' + error.status + ' ' + error.statusText,
                                        'Could not retrieve Committee Member User Information. Please contact System Administrator.'
                                    );
                                }
                            );
                    }
                },
                function (error) {
                    toastr.error(
                        'Error ' + error.status + ' ' + error.statusText,
                        'Could not retrieve Committee Member Information. Please contact System Administrator.'
                    );
                }
            );

        $scope.saveAccount = function () {
            swal({
                title: 'Create User',
                text: 'Do you want to save the information and create this user?',
                icon: 'info',
                buttons: {
                    cancel: true,
                    confirm: 'Save',
                },
            }).then((isConfirm) => {
                if (isConfirm) {
                    $http.post('/api/users/users/', $scope.newUser).then(
                        function (response) {
                            var commitee = {
                                user: response.data.id,
                            };
                            return $http.patch('/api/committees/committees/' + $scope.committeeId + '/', commitee).then(
                                function (response1) {
                                    var user = JSON.parse(localStorage.getItem('currentUser'));
                                    var userLogs = {
                                        user: user['id'],
                                        action_type: 'Created', //String value of action i.e. Created, Updated, Approved, Complete etc.
                                        content_type: '', //value return by appFactory, model name i.e. committee, documentmovement, steps etc.
                                        object_id: response.data.id, //ID of object created i.e. borrowerId, id etc.
                                        object_type: 'Committee User Account', //String value to display on viewing i.e. Committee Member, Document etc
                                        apiLink: '/api/committees/committees', //api link to access object_id. if object_id = borrowerId, then apiLInk = /api/borrowers/borrowers
                                        valueToDisplay: 'fullName', //field value on api link to display. if object_id = borrowerId, apiLInk = /api/borrowers/borrowers, then  borrowerName
                                        logDetails: [
                                            {
                                                action: 'Created User Account for ' + $scope.committee.committeeName, //Details of Log
                                            },
                                        ],
                                    };
                                    return appFactory.getContentTypeId('customuser').then(function (data) {
                                        userLogs.content_type = data;
                                        return $http.post('/api/users/userlogs/', userLogs).then(
                                            function () {
                                                swal('Success!', 'Committee User Created.', 'success');
                                                toastr.success('Success', 'Committee User Created.');
                                                $state.reload();
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
                                        'Could not Update Commitee Account. Please contact System Administrator.'
                                    );
                                }
                            );
                        },
                        function (error) {
                            $scope.creationError = error.data;
                            toastr.error(
                                'Error ' + error.status + ' ' + error.statusText,
                                'Could not Create Committee User Account. Please contact System Administrator'
                            );
                        }
                    );
                }
            });
        };

        $scope.changePassword = function () {
            console.log($scope.committeeUserAccount);
            $http
                .get('/api/auth/validatepassword/', {
                    params: {
                        username: $scope.committeeUserAccount.username,
                        password: $scope.committeeUserAccount.password,
                    },
                })
                .then(function (response) {
                    console.log(response.data);
                });
        };
    });
});
