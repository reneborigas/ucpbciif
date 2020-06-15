define(function () {
    'use strict';

    var app = angular.module('app');

    app.controller('DocumentListController',
        function DocumentListController($http, $filter, $scope, toastr, NgTableParams, $state, $timeout, appFactory) {

            $scope.tableDocuments = new NgTableParams({
                page: 1,
                count: 10,
            },
                {
                    counts: [10, 20, 30, 50, 100],
                    getData: function (params) {
                        return $http.get('/api/documents/documents/', { params: { subProcessId: $scope.subProcessId } }).then(
                            function (response) {
                                var filteredData = params.filter() ? $filter('filter')(response.data, params.filter()) : response.data;
                                var orderedData = params.sorting() ? $filter('orderBy')(filteredData, params.orderBy()) : filteredData;
                                var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                params.total(response.data.length);

                                var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                return page
                            },
                            function (error) {
                                toastr.error('Error ' + error.status + ' ' + error.statusText, 'Could not Load Documents. Please contact System Administrator.');
                            })
                    }
                });

            $scope.tableDocumentMovements = new NgTableParams({
                page: 1,
                count: 10,
            },
                {
                    counts: [],
                    getData: function (params) {
                        return $http.get('/api/documents/documentmovements/').then(
                            function (response) {
                                var filteredData = params.filter() ? $filter('filter')(response.data, params.filter()) : response.data;
                                var orderedData = params.sorting() ? $filter('orderBy')(filteredData, params.orderBy()) : filteredData;
                                var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                params.total(response.data.length);

                                var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                                return page

                            },
                            function (error) {
                                toastr.error('Error ' + error.status + ' ' + error.statusText, 'Could not load Document Movements. Please contact System Administrator.');
                            })
                    }
                });

            $scope.$watch('searchTermAuto', function (newTerm, oldTerm) {
                $scope.tableDocuments.filter({ $: newTerm });
            }, true);

            $scope.view = function (subProcessName, id) {
                var subProcessNameSlug = appFactory.slugify(subProcessName)
                $state.go('app.documents.info', { subProcessName: subProcessNameSlug, documentId: id });
            }

        }
    );


    app.controller('DocumentInfoController',
        function DocumentInfoController($http, $filter, $scope, toastr, NgTableParams, appFactory, $state, $timeout) {

            appFactory.getLastActivity($scope.documentId).then(function (data) {
                $scope.lastActivity = data[0];
                if ($scope.lastActivity.output == null) {
                    $http.get('/api/processes/steps/', { params: { stepId: $scope.lastActivity.stepId, process: 'current' } }).then(
                        function (response) {
                            $scope.currentStep = response.data[0];

                            $http.get('/api/processes/steprequirements/', { params: { stepId: $scope.currentStep.id } }).then(
                                function (response) {
                                    $scope.stepRequirements = response.data;

                                    $scope.currentRequirement = $scope.stepRequirements[0];
                                    $scope.currentRequirement.attachments = $scope.currentRequirement.stepRequirementAttachments;

                                },
                                function (error) {
                                    toastr.error('Error ' + error.status + ' ' + error.statusText, 'Could not retrieve Step Requirements Information. Please contact System Administrator.');
                                });

                        },
                        function (error) {
                            toastr.error('Error ' + error.status + ' ' + error.statusText, 'Could not retrieve current procedure Information. Please contact System Administrator.');
                        });
                }
                else {
                    // console.log($scope.lastActivity.output.nextStep);
                    $http.get('/api/processes/steps/', { params: { stepId: $scope.lastActivity.output.nextStep } }).then(
                        function (response) {
                            $scope.currentStep = response.data[0];
                            $http.get('/api/processes/steprequirements/', { params: { stepId: $scope.currentStep.id } }).then(
                                function (response) {
                                    $scope.stepRequirements = response.data;

                                    $scope.currentRequirement = $scope.stepRequirements[0];



                                },
                                function (error) {
                                    toastr.error('Error ' + error.status + ' ' + error.statusText, 'Could not retrieve Step Requirements Information. Please contact System Administrator.');
                                });
                        },
                        function (error) {
                            toastr.error('Error ' + error.status + ' ' + error.statusText, 'Could not retrieve current procedure. Please contact System Administrator.');
                        });

                }

                // $http.get('/api/processes/steps/', {params:{ stepId : $scope.lastActivity.stepId , process : 'next' }}).then(
                //     function(response){
                //         $scope.nextStep = response.data[0]; 
                // },

                // function(error){
                //     toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not retrieve Next Step Information. Please contact System Administrator.'); 
                // });
            });

            $http.get('/api/documents/documents/', { params: { subProcessName: $scope.subProcessName, documentId: $scope.documentId } }).then(
                function (response) {
                    $scope.document = response.data[0];
                },
                function (error) {
                    toastr.error('Error ' + error.status + ' ' + error.statusText, 'Could not retrieve Document Information. Please contact System Administrator.');
                });

            $http.get('/api/documents/documentmovements/', { params: { documentId: $scope.documentId } }).then(
                function (response) {
                    $scope.documentMovements = response.data;
                },
                function (error) {
                    toastr.error('Error ' + error.status + ' ' + error.statusText, 'Could not retrieve Document Movement Information. Please contact System Administrator.');
                });

            $http.get('/api/processes/steps/').then(
                function (response) {
                    $scope.processSteps = response.data;
                },
                function (error) {
                    toastr.error('Error ' + error.status + ' ' + error.statusText, 'Could not retrieve Document Movement Information. Please contact System Administrator.');
                });

            $scope.getRequirement = function () {
                for (var i = 0; i < $scope.stepRequirements.length; i++) {
                    if ($scope.currentRequirement.id == $scope.stepRequirements[i].id) {
                        return $scope.stepRequirements[i].id;
                    }
                }
            }

            $scope.goToRequirement = function (id) {
                for (var i = 0; i < $scope.stepRequirements.length; i++) {
                    if ($scope.stepRequirements[i].id == id) {
                        $scope.currentRequirement = $scope.stepRequirements[i];
                        $http.get('/api/processes/steprequirementsattachments/', { params: { stepRequirementId: $scope.currentRequirement.id } }).then(
                            function (response) {
                                $scope.currentRequirement.attachments = response.data;
                            },
                            function (error) {
                                toastr.error('Error ' + error.status + ' ' + error.statusText, 'Could not retrieve attachments Information. Please contact System Administrator.');
                            });

                    }
                }
            }

            // $scope.activityTemplates = [
            //     {
            //         templateNumber: 1,
            //         name: "Activities",
            //         icon: "fad fa-info-square",
            //         templateUrl: '/statics/partials/pages/documents/info/activities.html',
            //     },]

            // $scope.templates = [
            //     {
            //         templateNumber: 1,
            //         name: "Basic Information",
            //         icon: "fad fa-info-square",
            //         templateUrl: '/statics/partials/pages/documents/info/basic.html',
            //     },
            //     {
            //         templateNumber: 2,
            //         name: "Contact Details",
            //         icon: "fad fa-address-book",
            //         templateUrl: '/statics/partials/pages/documents/info/contact.html',
            //     },
            //     {
            //         templateNumber: 3,
            //         name: "Background",
            //         icon: "fad fa-user-friends",
            //         templateUrl: '/statics/partials/pages/documents/info/directorCommittee.html',
            //     },
            //     {
            //         templateNumber: 4,
            //         name: "Grants",
            //         icon: "fad fa-coin",
            //         templateUrl: '/statics/partials/pages/documents/info/grants.html',
            //     },
            //     {
            //         templateNumber: 5,
            //         name: "History",
            //         icon: "fad fa-history",
            //         templateUrl: '/statics/partials/pages/documents/info/history.html',
            //     }
            // ]

            // $scope.currentTemplate = $scope.templates[0];
            // $scope.currentActivityTemplate = $scope.activityTemplates[0];

            // $scope.getTemplate = function(){
            //     for (var i = 0; i < $scope.templates.length; i++) {
            //         if ($scope.currentTemplate.templateNumber == $scope.templates[i].templateNumber) {
            //             return $scope.templates[i].templateUrl;
            //         }
            //     }
            // }
            // $scope.getActiviyTemplate = function(){
            //     for (var i = 0; i < $scope.activityTemplates.length; i++) {
            //         if ($scope.currentActivityTemplate.templateNumber == $scope.activityTemplates[i].templateNumber) {
            //             return $scope.activityTemplates[i].templateUrl;
            //         }
            //     }
            // }
            // $scope.goToTemplate = function(templateNumber){
            //     for (var i = 0; i < $scope.templates.length; i++) {
            //         if ($scope.templates[i].templateNumber == templateNumber) {
            //             $scope.currentTemplate = $scope.templates[i]
            //         }
            //     }
            // }
            // $scope.goToActivityTemplate = function(templateNumber){
            //     for (var i = 0; i < $scope.activityTemplates.length; i++) {
            //         if ($scope.activityTemplates[i].templateNumber == templateNumber) {
            //             $scope.currentActivityTemplate = $scope.activityTemplates[i]
            //         }
            //     }
            // }

            // $scope.getCurrentProcessStepTemplate = function(){

            // }

            $scope.fileAttachment = [];

            $scope.selectFile = function(){
                $timeout(function() {
                    angular.element('#fileAttachment').trigger('click');
                }, 0);
            }

            $scope.$watch('fileAttachment', function (newValue, oldValue) {
                $scope.fileList = [];
                Array.prototype.forEach.call(newValue, function(file) { 
                    $scope.fileList.push({
                        name: file.name,
                        size: file.size,
                    })
                });
                console.log($scope.fileAttachment[0])
            });

            $scope.removeFile = function(index){
                $scope.fileList.splice(index,1)
            }

            $scope.takeActions = function (documentId, output, step) {
                $scope.documentMovement = {
                    remarks: $scope.remarks,
                    outputId: output.id,
                    output: output,
                    document: documentId,
                    name: step.name,
                    step: step.id,
                    committee: '1',
                    status: step.status
                }

                console.log($scope.documentMovement);
                swal({
                    title: "Submit Output",
                    text: "Continue submitting file as " + output.name + "?",
                    icon: "info",
                    buttons: {
                        cancel: true,
                        confirm: "Submit",
                    }
                }).then((isConfirm) => {
                    if (isConfirm) {
                        $http.post('/api/documents/documentmovements/', $scope.documentMovement)
                            .then(function () {
                                toastr.success('Success', 'File successfully moved to the next phase.');
                                swal("Success!", "File successfully moved to the next phase", "success");
                                $state.reload();
                                ;
                            },
                                function (error) {
                                    toastr.error('Error ' + error.status + ' ' + error.statusText, 'Could not create new record. Please contact System Administrator.');
                                });
                    }
                });
            }

            $scope.attachFile = function (stepRequirement) {
                $scope.newAttachment = {
                    fileName: $scope.newAttachmentName,
                    fileAttachment: $scope.fileAttachment[0],
                    description: $scope.newAttachmenDescription,
                    stepRequirement: stepRequirement.id,
                }

                var formData = new FormData()
                angular.forEach($scope.newAttachment,function(value,key){
                    formData.append(key, value)
                })
                if ($scope.newAttachmentName) {
                    swal({
                        title: "Attach File",
                        text: "Continue attaching file to " + stepRequirement.name + "?",
                        icon: "info",
                        buttons: {
                            cancel: true,
                            confirm: "Submit",
                        }
                    }).then((isConfirm) => {
                        if (isConfirm) {
                            $http.post('/api/processes/steprequirementsattachments/', formData,{
                                transformRequest: angular.identity,
                                headers : {'Content-Type':undefined}
                            }).then(function () {
                                    toastr.success('Success', 'New attachment successfully saved.');
                                    swal("Success!", "New attachment successfully saved", "success");
                                    // $state.reload();
                                    $scope.goToRequirement($scope.currentRequirement.id);
                                    $scope.newAttachmentName = "";
                                    $scope.newAttachmenDescription = "";

                                },
                                    function (error) {
                                        toastr.error('Error ' + error.status + ' ' + error.statusText, 'Could not create new record. Please contact System Administrator.');
                                    });
                        }
                    });
                }
                else {
                    toastr.error('Error: Attachment Error', 'Could not create new attachment. Please select file to attach');
                }
            }
        }
    );

    app.controller('DocumentAddController',
        function DocumentAddController($http, $filter, $scope, toastr, NgTableParams, $state, $timeout) {

            $scope.loan = { loanName: '', loanAmount: '', borrower: '' }

            $scope.save = function () {
                swal({
                    title: "Create Document",
                    text: "Do you want to save and create this loan?",
                    icon: "info",
                    buttons: {
                        cancel: true,
                        confirm: "Create",
                    }
                }).then((isConfirm) => {
                    if (isConfirm) {
                        $http.post('/api/documents/documents/', $scope.loan)
                            .then(function () {
                                toastr.success('Success', 'New loan created.');
                                swal("Success!", "New Borrower Created.", "success");
                                $state.go('app.documents.list');
                            },
                                function (error) {
                                    toastr.error('Error ' + error.status + ' ' + error.statusText, 'Could not create new record. Please contact System Administrator.');
                                });
                    }
                });

            }


        }
    );
});