define(function () {
    'use strict';

    var app = angular.module('app');

    app.controller('BorrowerListController', function BorrowerListController(
        $http,
        $filter,
        $scope,
        $state,
        $timeout,
        toastr,
        appFactory,
        NgTableParams
    ) {
        $scope.totalRecords;
        $scope.countFrom;
        $scope.countTo;

        $scope.tableBorrowers = new NgTableParams(
            {
                page: 1,
                count: 10,
            },
            {
                counts: [],
                getData: function (params) {
                    return $http.get('/api/borrowers/borrowers/').then(
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

                            $scope.countFrom = (params.page() - 1) * params.count() + 1;
                            $scope.countTo =
                                params.count() * params.page() > params.total()
                                    ? params.total()
                                    : params.count() * params.page();
                            $scope.totalRecords = params.total();
                            var count = $scope.tableBorrowers._params.count;
                            $scope.globalPageCount = count.toString();

                            var page = orderedData.slice(
                                (params.page() - 1) * params.count(),
                                params.page() * params.count()
                            );
                            return page;
                        },
                        function (error) {
                            toastr.error(
                                'Error ' + error.status + ' ' + error.statusText,
                                'Could not load Borrowers. Please contact System Administrator.'
                            );
                        }
                    );
                },
            }
        );

        $scope.tableBorrowersContactPerson = new NgTableParams(
            {
                page: 1,
                count: 10,
            },
            {
                counts: [],
                getData: function (params) {
                    return $http.get('/api/borrowers/borrowers/').then(
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

                            // $scope.countFrom = ((params.page() - 1) * params.count()) + 1;
                            // $scope.countTo = params.count() * params.page() > params.total() ? params.total() : params.count() * params.page();
                            // $scope.totalRecords = params.total();
                            // var count = $scope.tableBorrowers._params.count
                            // $scope.globalPageCount = count.toString()

                            var page = orderedData.slice(
                                (params.page() - 1) * params.count(),
                                params.page() * params.count()
                            );
                            return page;
                        },
                        function (error) {
                            toastr.error(
                                'Error ' + error.status + ' ' + error.statusText,
                                'Could not load Borrowers. Please contact System Administrator.'
                            );
                        }
                    );
                },
            }
        );

        $scope.$watch(
            'searchTermAuto',
            function (newTerm, oldTerm) {
                $scope.tableBorrowers.filter({ $: newTerm });
            },
            true
        );

        $scope.$watch(
            'globalPageCount',
            function (newValue, oldValue) {
                if (newValue) {
                    $scope.tableBorrowers._params.count = newValue;
                }
            },
            true
        );

        $scope.view = function (id) {
            $state.go('app.borrowers.info', { borrowerId: id });
        };

        $scope.edit = function (id) {
            $state.go('app.borrowers.edit', { borrowerId: id });
        };

        // $scope.delete = function(id){
        //     console.log(id)
        // }
    });

    app.controller('BorrowerAddController', function BorrowerAddController(
        $http,
        $filter,
        $scope,
        toastr,
        NgTableParams,
        appFactory,
        $state,
        $timeout
    ) {
        $scope.steps = [
            {
                step: 1,
                name: 'Basic Info',
                desc: 'Borrower Information',
                templateUrl: '/statics/partials/pages/borrowers/wizard/step1.html',
            },
            {
                step: 2,
                name: 'Structure',
                desc: 'Incorporation Details',
                templateUrl: '/statics/partials/pages/borrowers/wizard/step2.html',
            },
            {
                step: 3,
                name: 'Committee',
                desc: 'Director and Committee Info',
                templateUrl: '/statics/partials/pages/borrowers/wizard/step3.html',
            },
            {
                step: 4,
                name: 'Grants',
                desc: 'Grant Info',
                templateUrl: '/statics/partials/pages/borrowers/wizard/step4.html',
            },
        ];

        $scope.currentStep = 1;

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

        $scope.nextStep = function () {
            $scope.changeStep = true;
            if ($scope.wizardForm.$valid) {
                $scope.currentStep = $scope.currentStep + 1;
            }
        };

        $scope.prevStep = function () {
            $scope.currentStep = $scope.currentStep - 1;
        };

        appFactory.getGenders().then(function (data) {
            $scope.genders = data;
        });

        appFactory.getCooperativeType().then(function (data) {
            $scope.cooperativetypes = data;
        });

        $scope.cooperative = {
            name: '',
            icRiskRating: '',
            tin: '',
            cdaRegistrationDate: '',
            initialMembershipSize: 0,
            membershipSize: 0,
            paidUpCapitalInitial: 0,
            noOfCooperators: 0,
            coconutFarmers: 0,
            authorized: 0,
            fullyPaidSharesNo: 0,
            bookValue: 0,
            parValue: 0,
            paidUp: 0,
            fullyPaidPercent: 0,
            initialPaidUpShare: 0,
            address: '',
            telNo: '',
            emailAddress: '',
            phoneNo: '',
            fax: '',
            cooperativeType: '',
            description: '',
            remarks: '',
            createdBy: appFactory.getCurrentUser(),
            directors: [
                {
                    name: '',
                    department: '',
                    position: '',
                    educationalAttainment: '',
                    age: '',
                    yearsInCoop: '',
                    oSLoanWithCoop: '',
                    status: '',
                    createdBy: appFactory.getCurrentUser(),
                },
            ],
            standingCommittees: [
                {
                    name: '',
                    position: '',
                    educationalAttainment: '',
                    age: '',
                    yearsInCoop: '',
                    oSLoanWithCoop: '',
                    status: '',
                    createdBy: appFactory.getCurrentUser(),
                },
            ],
            grants: [
                {
                    cooperative: '',
                    donor: '',
                    projectType: '',
                    amount: 0,
                    projectStatus: '',
                    createdBy: appFactory.getCurrentUser(),
                },
            ],
        };

        $scope.contactPerson = {
            firstname: '',
            middlename: '',
            lastname: '',
            address: '',
            telNo: '',
            emailAddress: '',
            phoneNo: '',
            createdBy: appFactory.getCurrentUser(),
        };

        $scope.borrower = {
            cooperative: '',
            contactPerson: '',
            status: '',
            clientSince: '',
            remarks: '',
            createdBy: appFactory.getCurrentUser(),
        };

        $scope.addDirector = function () {
            $scope.borrower.directors.push({
                name: '',
                department: '',
                position: '',
                educationalAttainment: '',
                age: '',
                yearsInCoop: '',
                oSLoanWithCoop: '',
                status: '',
                createdBy: appFactory.getCurrentUser(),
            });
        };

        $scope.removeDirector = function (index) {
            $scope.borrower.directors.splice(index, 1);
        };

        $scope.addCommittee = function () {
            $scope.borrower.standingCommittees.push({
                name: '',
                position: '',
                educationalAttainment: '',
                age: '',
                yearsInCoop: '',
                oSLoanWithCoop: '',
                status: '',
                createdBy: '',
            });
        };

        $scope.removeCommittee = function (index) {
            $scope.borrower.standingCommittees.splice(index, 1);
        };

        $scope.save = function () {
            if ($scope.wizardForm.$valid) {
                swal({
                    title: 'Create Borrower',
                    text: 'Do you want to save and create this borrower?',
                    icon: 'info',
                    buttons: {
                        cancel: true,
                        confirm: 'Create',
                    },
                }).then((isConfirm) => {
                    if (isConfirm) {
                        $http.post('/api/borrowers/cooperatives/', $scope.cooperative).then(
                            function (responseCooperative) {
                                return $http.post('/api/borrowers/contactpersons/', $scope.contactPerson).then(
                                    function (responseContactPerson) {
                                        $scope.borrower.cooperative = responseCooperative.data.id;
                                        $scope.borrower.cooperative = responseContactPerson.data.id;
                                        return $http.post('/api/borrowers/borrowers/', $scope.borrower).then(
                                            function () {
                                                swal('Success!', 'New Borrower Created.', 'success');
                                                toastr.success('Success', 'New Borrower Updated.');
                                                $state.go('app.borrower.list');
                                            },
                                            function (error) {
                                                toastr.error(
                                                    'Error ' + error.status + ' ' + error.statusText,
                                                    'Could not create new borrower. Please contact System Administrator.'
                                                );
                                            }
                                        );
                                    },
                                    function (error) {
                                        toastr.error(
                                            'Error ' + error.status + ' ' + error.statusText,
                                            'Could not create new contact person. Please contact System Administrator.'
                                        );
                                    }
                                );
                            },
                            function (error) {
                                toastr.error(
                                    'Error ' + error.status + ' ' + error.statusText,
                                    'Could not create new cooperative. Please contact System Administrator.'
                                );
                            }
                        );
                    }
                });
            }
        };
    });

    app.controller('BorrowerInfoController', function BorrowerInfoController(
        $http,
        $filter,
        $scope,
        toastr,
        NgTableParams,
        appFactory,
        $state,
        $timeout,
        $q,
        blockUI
    ) {
        $http.get('/api/borrowers/borrowers/', { params: { borrowerId: $scope.borrowerId } }).then(
            function (response) {
                $scope.borrower = response.data[0];
                $scope.getBorrowerAttachments($scope.borrowerId);
                $http.get('/api/processes/subprocesses/', { params: { borrowerId: $scope.borrowerId } }).then(
                    function (response) {
                        $scope.subprocesses = response.data;
                        $scope.subProcessCurrentPage.length = 0;
                        angular.forEach($scope.subprocesses, function (subprocess) {
                            $scope.subProcessCurrentPage[subprocess.name] = 0;
                        });
                        //     if($scope.borrower.documents.length){

                        //     angular.forEach($scope.subprocesses, function (subProcess) {
                        //         angular.forEach($scope.borrower.documents, function (document) {
                        //             if (document.subProcess.id === subProcess.id) {

                        //                 if (!document.documentMovements[0].status.isFinalStatus) {
                        //                     subProcess.isAllowed = false;
                        //                     subProcess.isAllowedByParent = false;
                        //                 } else {
                        //                     if (subProcess.relatedProcesses.length) {
                        //                         angular.forEach($scope.borrower.documents, function (document) {
                        //                             if (document.subProcess.id === subProcess.relatedProcesses[0].id) {
                        //                                 $scope.document_item = document;

                        //                             }
                        //                         });
                        //                         if (!$scope.document_item.documentMovements[0].status.isFinalStatus) {
                        //                             subProcess.isAllowedByParent = false;
                        //                         } else {
                        //                             if (
                        //                                 !$scope.document_item.documentMovements[0].status.isNegativeResult
                        //                             ) {
                        //                                 subProcess.isAllowedByParent = true;
                        //                             } else {
                        //                                 subProcess.isAllowedByParent = false;
                        //                             }
                        //                         }
                        //                     } else {
                        //                         subProcess.isAllowedByParent = true;

                        //                     }
                        //                     subProcess.isAllowed = true;
                        //                 }
                        //             }else{
                        //                 if (subProcess.relatedProcesses.length) {
                        //                     angular.forEach($scope.borrower.documents, function (document) {
                        //                         if (document.subProcess.id === subProcess.relatedProcesses[0].id) {
                        //                             $scope.document_item = document;

                        //                         }
                        //                     });
                        //                     if (!$scope.document_item.documentMovements[0].status.isFinalStatus) {
                        //                         subProcess.isAllowedByParent = false;
                        //                     } else {
                        //                         if (
                        //                             !$scope.document_item.documentMovements[0].status.isNegativeResult
                        //                         ) {
                        //                             subProcess.isAllowedByParent = true;
                        //                         } else {
                        //                             subProcess.isAllowedByParent = false;
                        //                         }
                        //                     }
                        //                 } else {
                        //                     subProcess.isAllowedByParent = true;

                        //                 }
                        //                 subProcess.isAllowed = true;
                        //             }
                        //         });
                        //     });

                        //  }else{
                        //     $scope.subprocesses[0].isAllowed=true;
                        //     $scope.subprocesses[0].isAllowedByParent=true;
                        //  }
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Sub Processes. Please contact System Administrator.'
                        );
                    }
                );
            },
            function (error) {
                toastr.error(
                    'Error ' + error.status + ' ' + error.statusText,
                    'Could not retrieve Borrower Information. Please contact System Administrator.'
                );
            }
        );

        $scope.isCanCreate = function (subProcessId) {};

        $scope.edit = function (id) {
            $state.go('app.borrowers.edit', { borrowerId: id });
        };

        $scope.goToFile = function (subProcessName, id) {
            console.log(subProcessName);
            var subProcessNameSlug = appFactory.slugify(subProcessName);
            $state.go('app.documents.info', { subProcessName: subProcessNameSlug, documentId: id });
        };

        $scope.newLoanApplication = function (borrowerId, subProcessId) {
            $state.go('app.borrowers.create_loan_application', { borrowerId: borrowerId, subProcessId: subProcessId });
        };

        $scope.templates = [
            {
                templateNumber: 1,
                name: 'Basic Information',
                icon: 'fad fa-info-square',
                templateUrl: '/statics/partials/pages/borrowers/info/basic.html',
            },
            {
                templateNumber: 2,
                name: 'Contact Details',
                icon: 'fad fa-address-book',
                templateUrl: '/statics/partials/pages/borrowers/info/contact.html',
            },
            {
                templateNumber: 3,
                name: 'Background',
                icon: 'fad fa-user-friends',
                templateUrl: '/statics/partials/pages/borrowers/info/directorCommittee.html',
            },
            {
                templateNumber: 4,
                name: 'Grants',
                icon: 'fad fa-coin',
                templateUrl: '/statics/partials/pages/borrowers/info/grants.html',
            },
            {
                templateNumber: 5,
                name: 'History',
                icon: 'fad fa-history',
                templateUrl: '/statics/partials/pages/borrowers/info/history.html',
            },
        ];

        $scope.currentTemplate = $scope.templates[0];

        $scope.getTemplate = function () {
            for (var i = 0; i < $scope.templates.length; i++) {
                if ($scope.currentTemplate.templateNumber == $scope.templates[i].templateNumber) {
                    return $scope.templates[i].templateUrl;
                }
            }
        };

        $scope.goToTemplate = function (templateNumber) {
            for (var i = 0; i < $scope.templates.length; i++) {
                if ($scope.templates[i].templateNumber == templateNumber) {
                    $scope.currentTemplate = $scope.templates[i];
                }
            }
        };

        $scope.getBorrowerAttachments = function (borrowerId) {
            $http
                .get('/api/borrowers/borrowerattachments/', {
                    params: { borrowerId: $scope.borrowerId },
                })
                .then(
                    function (response) {
                        $scope.borrowerAttachments = response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Borrower Attachments Information. Please contact System Administrator.'
                        );
                    }
                );
        };

        var attachmentBlockUI = blockUI.instances.get('attachmentBlockUI');

        $scope.currentPageAttachment = 0;
        $scope.pageSizeAttachment = 5;

        $scope.pageRangeAttachment = function (size) {
            var pages = [];
            var range = Math.ceil(size / $scope.pageSizeAttachment);
            for (var i = 1; i <= range; i++) {
                pages.push(i);
            }
            return pages;
        };

        $scope.gotoPrevAttachment = function () {
            $scope.currentPageAttachment--;
        };

        $scope.gotoNextAttachment = function () {
            $scope.currentPageAttachment++;
        };

        $scope.jumpToPageAttachment = function (n) {
            $scope.currentPageAttachment = n - 1;
        };

        $scope.subProcessCurrentPage = {};

        $scope.currentPageDocument = function (subProcess) {
            var currentPage;
            angular.forEach($scope.subProcessCurrentPage, function (value, key) {
                if (subProcess.name == key) {
                    currentPage = value;
                }
            });
            return currentPage;
        };

        $scope.pageSizeDocument = 5;

        $scope.pageRangeDocument = function (size) {
            var pages = [];
            var range = Math.ceil(size / $scope.pageSizeDocument);
            for (var i = 1; i <= range; i++) {
                pages.push(i);
            }
            return pages;
        };

        $scope.gotoPrevDocument = function (subProcess) {
            $scope.subProcessCurrentPage[subProcess.name]--;
        };

        $scope.gotoNextDocument = function (subProcess) {
            $scope.subProcessCurrentPage[subProcess.name]++;
        };

        $scope.jumpToPageDocument = function (n, subProcess) {
            $scope.subProcessCurrentPage[subProcess.name] = n - 1;
        };

        $scope.fileAttachment = {
            attachment: [],
        };

        $scope.newAttachment = {
            attachmentDescription: '',
        };

        $scope.selectFile = function () {
            $timeout(function () {
                angular.element('#fileAttachment').trigger('click');
            }, 0);
        };

        $scope.$watch('fileAttachment.attachment', function (newValue, oldValue) {
            $scope.fileList = [];
            Array.prototype.forEach.call(newValue, function (file) {
                $scope.fileList.push({
                    name: file.name,
                    size: file.size,
                });
            });
        });

        $scope.removeFile = function (index) {
            $scope.fileList.splice(index, 1);
        };

        var promises = [];

        $scope.attachFile = function (borrower) {
            attachmentBlockUI.start('Attaching File...');
            angular.forEach($scope.fileList, function (fileList, index) {
                var newAttachment = {
                    fileName: $scope.fileAttachment.attachment[index].name,
                    fileAttachment: $scope.fileAttachment.attachment[index],
                    description: $scope.newAttachment.attachmentDescription,
                    borrower: borrower.borrowerId,
                };
                var formData = new FormData();
                angular.forEach(newAttachment, function (value, key) {
                    formData.append(key, value);
                });
                promises.push($scope.uploadFile(formData));
            });

            $q.all(promises).then(
                function (response) {
                    toastr.success('Success', 'All attachment successfully saved.');
                    $scope.fileList.length = 0;
                    $scope.newAttachment.attachmentDescription = '';
                    $scope.getBorrowerAttachments($scope.borrowerId);
                    angular.element('#attach-file').modal('hide');
                    attachmentBlockUI.stop();
                },
                function (error) {
                    toastr.error(
                        'Error ' + error.status + ' ' + error.statusText,
                        'Could not create upload attachments. Please contact System Administrator.'
                    );
                    angular.element('#attach-file').modal('hide');
                    attachmentBlockUI.stop();
                }
            );
        };

        $scope.uploadFile = function (formData) {
            var defer = $q.defer();
            return $http
                .post('/api/borrowers/borrowerattachments/', formData, {
                    transformRequest: angular.identity,
                    headers: { 'Content-Type': undefined },
                })
                .then(
                    function (response) {
                        defer.resolve(
                            'Success',
                            appFactory.trimString(response.data.fileName, 9) + ' uploaded successfully.'
                        );

                        return defer.promise;
                    },
                    function (error) {
                        defer.reject(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not create new file attachment. Please contact System Administrator.'
                        );

                        return defer.promise;
                    }
                );
        };

        $scope.downloadFile = function (link, fileName) {
            var downloadLink = angular.element('<a></a>');
            downloadLink.attr('target', '_self');
            downloadLink.attr('href', link);
            downloadLink.attr('download', fileName);
            downloadLink[0].click();
        };
    });

    app.controller('BorrowerEditController', function BorrowerEditController(
        $http,
        $filter,
        $scope,
        toastr,
        NgTableParams,
        appFactory,
        $state,
        $timeout
    ) {
        $http.get('/api/borrowers/borrowers/', { params: { borrowerId: $scope.borrowerId } }).then(
            function (response) {
                $scope.borrower = response.data[0];
                $scope.borrower.cooperative.paidUpCapitalInitial = parseFloat(
                    $scope.borrower.cooperative.paidUpCapitalInitial
                );
                $scope.borrower.cooperative.authorized = parseFloat($scope.borrower.cooperative.authorized);
                $scope.borrower.cooperative.parValue = parseFloat($scope.borrower.cooperative.parValue);
                $scope.borrower.cooperative.paidUp = parseFloat($scope.borrower.cooperative.paidUp);
                $scope.borrower.cooperative.cdaRegistrationDate = new Date(
                    $scope.borrower.cooperative.cdaRegistrationDate
                );
                angular.forEach($scope.borrower.cooperative.directors, function (director) {
                    director.oSLoanWithCoop = parseFloat(director.oSLoanWithCoop);
                });
                angular.forEach($scope.borrower.cooperative.standingCommittees, function (standingCommittee) {
                    standingCommittee.oSLoanWithCoop = parseFloat(standingCommittee.oSLoanWithCoop);
                });
                angular.forEach($scope.borrower.cooperative.grants, function (grant) {
                    grant.amount = parseFloat(grant.amount);
                });
            },
            function (error) {
                toastr.error(
                    'Error ' + error.status + ' ' + error.statusText,
                    'Could not retrieve Borrower Information. Please contact System Administrator.'
                );
            }
        );

        $scope.templates = [
            {
                templateNumber: 1,
                name: 'Borrower Information',
                desc: 'Basic Information',
                templateUrl: '/statics/partials/pages/borrowers/edit/basic.html',
            },
            {
                templateNumber: 2,
                name: 'Background',
                desc: 'Incorporation Details',
                templateUrl: '/statics/partials/pages/borrowers/edit/background.html',
            },
            {
                templateNumber: 3,
                name: 'Directors and Committee',
                desc: 'Director and Committee Information',
                templateUrl: '/statics/partials/pages/borrowers/edit/directorCommittee.html',
            },
            {
                templateNumber: 4,
                name: 'Grants',
                desc: 'Grant Info',
                templateUrl: '/statics/partials/pages/borrowers/edit/grants.html',
            },
        ];

        $scope.currentTemplate = $scope.templates[0];

        $scope.getTemplate = function () {
            for (var i = 0; i < $scope.templates.length; i++) {
                if ($scope.currentTemplate.templateNumber == $scope.templates[i].templateNumber) {
                    return $scope.templates[i].templateUrl;
                }
            }
        };

        $scope.goToTemplate = function (templateNumber) {
            for (var i = 0; i < $scope.templates.length; i++) {
                if ($scope.templates[i].templateNumber == templateNumber) {
                    $scope.currentTemplate = $scope.templates[i];
                }
            }
        };

        appFactory.getCooperativeType().then(function (data) {
            $scope.cooperativetypes = data;
        });

        $scope.addDirector = function () {
            $scope.borrower.cooperative.directors.push({
                name: '',
                department: '',
                position: '',
                educationalAttainment: '',
                age: '',
                yearsInCoop: '',
                oSLoanWithCoop: '',
                status: '',
                createdBy: appFactory.getCurrentUser(),
            });
        };

        $scope.removeDirector = function (index) {
            $scope.borrower.cooperative.directors.splice(index, 1);
        };

        $scope.addCommittee = function () {
            $scope.borrower.cooperative.standingCommittees.push({
                name: '',
                position: '',
                educationalAttainment: '',
                age: '',
                yearsInCoop: '',
                oSLoanWithCoop: '',
                status: '',
                createdBy: '',
            });
        };

        $scope.removeCommittee = function (index) {
            $scope.borrower.cooperative.standingCommittees.splice(index, 1);
        };

        $scope.update = function () {
            $scope.borrower.cooperative.cdaRegistrationDate = appFactory.dateWithoutTime(
                $scope.borrower.cooperative.cdaRegistrationDate,
                'yyyy-MM-dd'
            );
            if ($scope.editForm.$valid) {
                swal({
                    title: 'Update Borrower',
                    text: 'Do you want to update this borrower?',
                    icon: 'info',
                    buttons: {
                        cancel: true,
                        confirm: 'Update',
                    },
                }).then((isConfirm) => {
                    if (isConfirm) {
                        $http
                            .patch(
                                '/api/borrowers/cooperatives/' + $scope.borrower.cooperative.id + '/',
                                $scope.borrower.cooperative
                            )
                            .then(
                                function () {
                                    return $http
                                        .patch(
                                            '/api/borrowers/documents/' + $scope.borrower.contactPerson.id + '/',
                                            $scope.borrower.contactPerson
                                        )
                                        .then(
                                            function () {
                                                return $http
                                                    .patch(
                                                        '/api/borrowers/borrowers/' + $scope.borrower.borrowerId + '/',
                                                        $scope.borrower
                                                    )
                                                    .then(
                                                        function (response) {
                                                            swal('Success!', 'Borrower Updated.', 'success');
                                                            toastr.success('Success', 'Borrower Updated.');
                                                            $state.go('app.borrowers.info', {
                                                                borrowerId: response.data.borrowerId,
                                                            });
                                                        },
                                                        function (error) {
                                                            toastr.error(
                                                                'Error ' + error.status + ' ' + error.statusText,
                                                                'Could not update borrower. Please contact System Administrator.'
                                                            );
                                                        }
                                                    );
                                            },
                                            function (error) {
                                                toastr.error(
                                                    'Error ' + error.status + ' ' + error.statusText,
                                                    'Could not update contact person. Please contact System Administrator.'
                                                );
                                            }
                                        );
                                },
                                function (error) {
                                    toastr.error(
                                        'Error ' + error.status + ' ' + error.statusText,
                                        'Could not update cooperative. Please contact System Administrator.'
                                    );
                                }
                            );
                    }
                });
            }
        };

        $scope.cancel = function (id) {
            $state.go('app.borrowers.info', { borrowerId: id });
        };
    });

    app.controller('BorrowerNewLoanApplicationController', function BorrowerNewLoanApplicationController(
        $http,
        $filter,
        $scope,
        toastr,
        NgTableParams,
        appFactory,
        $state,
        $timeout
    ) {
        appFactory.getCommittee().then(function (data) {
            $scope.committees = data;
        });

        appFactory.getTerm().then(function (data) {
            $scope.terms = data;
        });
        appFactory.getLoanPrograms().then(function (data) {
            $scope.loanPrograms = data;
        });
        $scope.exceeded = false;
        $scope.$watch(
            'loan.amount',
            function (newTerm, oldTerm) {
                if (newTerm > $scope.subProcess.parentLastDocumentCreditLine.remainingCreditLine) {
                    //Error
                    console.log('invalid');

                    $scope.exceeded = true;
                } else {
                    $scope.exceeded = false;
                }
            },
            true
        );

        $scope.loadCommittee = function (query) {
            return $scope.committees;
        };

        $scope.selectedCommittee = [];

        $scope.loadBorrower = function () {
            if ($scope.creditLine.creditlineid) {
                $scope.params = { borrowerId: $scope.borrowerId, loanProgramId: $scope.creditLine.loanProgram };
            } else {
                $scope.params = { borrowerId: $scope.borrowerId };
            }

            console.log($scope.params);
            $http.get('/api/borrowers/borrowers/', { params: $scope.params }).then(
                function (response) {
                    $scope.borrower = response.data[0];
                    $scope.borrower.cooperative.paidUpCapitalInitial = parseFloat(
                        $scope.borrower.cooperative.paidUpCapitalInitial
                    );
                    $scope.borrower.cooperative.authorized = parseFloat($scope.borrower.cooperative.authorized);
                    $scope.borrower.cooperative.parValue = parseFloat($scope.borrower.cooperative.parValue);
                    $scope.borrower.cooperative.paidUp = parseFloat($scope.borrower.cooperative.paidUp);
                    $scope.borrower.cooperative.cdaRegistrationDate = new Date(
                        $scope.borrower.cooperative.cdaRegistrationDate
                    );
                    angular.forEach($scope.borrower.cooperative.directors, function (director) {
                        director.oSLoanWithCoop = parseFloat(director.oSLoanWithCoop);
                    });
                    angular.forEach($scope.borrower.cooperative.standingCommittees, function (standingCommittee) {
                        standingCommittee.oSLoanWithCoop = parseFloat(standingCommittee.oSLoanWithCoop);
                    });
                    angular.forEach($scope.borrower.cooperative.grants, function (grant) {
                        grant.amount = parseFloat(grant.amount);
                    });
                },
                function (error) {
                    toastr.error(
                        'Error ' + error.status + ' ' + error.statusText,
                        'Could not retrieve Borrower Information. Please contact System Administrator.'
                    );
                }
            );
        };
        $http
            .get('/api/processes/subprocesses/', {
                params: { subProcessId: $scope.subProcessId, borrowerId: $scope.borrowerId },
            })
            .then(
                function (response) {
                    $scope.subProcess = response.data[0];

                    $scope.document = {
                        name: '',
                        description: '',
                        remarks: '',
                        borrower: $scope.borrowerId,
                        subProcess: $scope.subProcess,
                        subProcessId: $scope.subProcessId,
                        documentType: 1,
                        createdBy: appFactory.getCurrentUser(),
                        committee: '',
                        loan: '',
                    };

                    $scope.creditLine = {
                        creditlineid: null,
                        amount: '',
                        interestRate: '',
                        term: '',
                        loanProgram: '',
                        purpose: '',
                        security: '',
                        status: 1,
                        borrower: $scope.borrowerId,
                        createdBy: appFactory.getCurrentUser(),
                    };

                    if ($scope.subProcess.parentLastDocumentCreditLine) {
                        $scope.creditLine = {
                            creditlineid: $scope.subProcess.parentLastDocumentCreditLine.id,
                            amount: parseFloat($scope.subProcess.parentLastDocumentCreditLine.amount),
                            interestRate: parseFloat($scope.subProcess.parentLastDocumentCreditLine.interestRate),
                            term: $scope.subProcess.parentLastDocumentCreditLine.term,

                            loanProgram: $scope.subProcess.parentLastDocumentCreditLine.loanProgram,
                            purpose: $scope.subProcess.parentLastDocumentCreditLine.purpose,
                            security: $scope.subProcess.parentLastDocumentCreditLine.security,
                            status: 1,
                            borrower: $scope.borrowerId,
                            term_name: $scope.subProcess.parentLastDocumentCreditLine.term_name,
                            loanProgram_name: $scope.subProcess.parentLastDocumentCreditLine.loanProgram_name,
                            createdBy: appFactory.getCurrentUser(),
                        };

                        $scope.loan = {
                            loanid: null,
                            amount: '',
                            creditLine: $scope.subProcess.parentLastDocumentCreditLine.id,
                            interestRate: parseFloat($scope.subProcess.parentLastDocumentCreditLine.interestRate),
                            term: $scope.subProcess.parentLastDocumentCreditLine.term,
                            termid: $scope.subProcess.parentLastDocumentCreditLine.term.id,
                            
                            loanProgram: $scope.subProcess.parentLastDocumentCreditLine.loanProgram,
                            purpose: '',
                            security: '',
                            status: 1,
                            borrower: $scope.borrowerId,
                            createdBy: appFactory.getCurrentUser(),
                        };
                    }

                    if ($scope.subProcess.parentLastDocumentLoan) {
                        $scope.loan = {
                            loanid: $scope.subProcess.parentLastDocumentLoan.id,
                            amount: parseFloat($scope.subProcess.parentLastDocumentLoan.amount),
                            creditLine: $scope.subProcess.parentLastDocumentLoan.creditLine,
                            interestRate: parseFloat($scope.subProcess.parentLastDocumentLoan.interestRate),
                            term: $scope.subProcess.parentLastDocumentLoan.term,
                            loanProgram: $scope.subProcess.parentLastDocumentLoan.loanProgram,
                            purpose: $scope.subProcess.parentLastDocumentLoan.purpose,
                            security: $scope.subProcess.parentLastDocumentLoan.security,
                            status: 1,
                            borrower: $scope.borrowerId,
                            term_name: $scope.subProcess.parentLastDocumentLoan.term_name,
                            loanProgram_name: $scope.subProcess.parentLastDocumentLoan.loanProgram_name,
                            createdBy: appFactory.getCurrentUser(),
                        };
                    }
                    $scope.loadBorrower();

                    // $scope.checkLoanDetails = function () {
                    //     if ($scope.subProcess.parentLastDocumentLoan) {
                    //         return true;
                    //     } else {
                    //         if ($scope.newLoanDetailsForm.$valid) {
                    //             return true;
                    //         } else {
                    //             return false;
                    //         }
                    //     }
                    // };
                    // $scope.checkCreditLineDetails = function () {
                    //     if ($scope.subProcess.parentLastDocumentCreditLine) {
                    //         return true;
                    //     } else {
                    //         if ($scope.newCreditLineDetailsForm.$valid) {
                    //             return true;
                    //         } else {
                    //             return false;
                    //         }
                    //     }
                    // };

                    $scope.createDocument = function () {
                        $http
                            .post('/api/documents/documents/', $scope.document)

                            .then(
                                function () {
                                    toastr.success('Success', 'New loan application file created.');

                                    swal('Success!', 'New Loan Application File Created.', 'success');
                                    $state.go('app.borrowers.info', { borrowerId: $scope.borrowerId });
                                },
                                function (error) {
                                    toastr.error(
                                        'Error ' + error.status + ' ' + error.statusText,
                                        'Could not create new loan application file. Please contact System Administrator.'
                                    );
                                }
                            );
                    };
                    $scope.checkDetails = function () {
                        if ($scope.subProcess.parentLastDocumentCreditLine) {
                            if ($scope.subProcess.parentLastDocumentCreditLine) {
                                return true;
                            } else {
                                if ($scope.newCreditLineDetailsForm.$valid) {
                                    return true;
                                } else {
                                    return false;
                                }
                            }
                        } else {
                            if ($scope.newCreditLineDetailsForm.$valid) {
                                return true;
                            } else {
                                return false;
                            }
                        }
                    };

                    $scope.save = function () {
                        console.log($scope.loan);
                        if ($scope.newLoanApplicationForm.$valid && $scope.checkDetails()) {
                            swal({
                                title: 'Create New Loan Application',
                                text: 'Do you want to save and create this loan application file?',
                                icon: 'info',
                                buttons: {
                                    cancel: true,
                                    confirm: 'Create',
                                },
                            }).then((isConfirm) => {
                                if (isConfirm) {
                                    if ($scope.creditLine.creditlineid) {
                                        console.log('Credit Line Exists');
                                        $scope.document.creditlineid = $scope.creditLine.creditlineid;

                                        if ($scope.loan.loanid) {
                                            console.log('Loan Exists');
                                            $scope.document.loanid = $scope.loan.loanid;
                                            console.log($scope.document);
                                            $scope.createDocument();
                                        } else {
                                            $http
                                                .post('/api/loans/loans/', $scope.loan)

                                                .then(
                                                    function (loanResponse) {
                                                        $scope.document.loanid = loanResponse.data.id;
                                                        console.log($scope.document);
                                                        $scope.createDocument();
                                                    },
                                                    function (error) {
                                                        toastr.error(
                                                            'Error ' + error.status + ' ' + error.statusText,
                                                            'Could not create new loan details record. Please contact System Administrator.'
                                                        );
                                                    }
                                                );
                                        }
                                    } else {
                                        $http
                                            .post('/api/loans/creditlines/', $scope.creditLine)

                                            .then(
                                                function (loanResponse) {
                                                    $scope.document.creditlineid = loanResponse.data.id;
                                                    console.log($scope.document);
                                                    $scope.createDocument();
                                                },
                                                function (error) {
                                                    toastr.error(
                                                        'Error ' + error.status + ' ' + error.statusText,
                                                        'Could not create new loan details record. Please contact System Administrator.'
                                                    );
                                                }
                                            );
                                    }
                                }
                            });
                        }
                    };
                },
                function (error) {
                    toastr.error(
                        'Error ' + error.status + ' ' + error.statusText,
                        'Could not retrieve Sub Process Information. Please contact System Administrator.'
                    );
                }
            );

        $scope.cancel = function (id) {
            $state.go('app.borrowers.info', { borrowerId: id });
        };
    });
});
