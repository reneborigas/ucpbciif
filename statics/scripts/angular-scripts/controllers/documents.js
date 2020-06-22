define(function () {
    'use strict';

    var app = angular.module('app');

    app.controller('DocumentListController', function DocumentListController(
        $http,
        $filter,
        $scope,
        toastr,
        NgTableParams,
        $state,
        $timeout,
        appFactory
    ) {
        $scope.tableDocuments = new NgTableParams(
            {
                page: 1,
                count: 10,
            },
            {
                counts: [10, 20, 30, 50, 100],
                getData: function (params) {
                    return $http
                        .get('/api/documents/documents/', { params: { subProcessId: $scope.subProcessId } })
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
                                    'Could not Load Documents. Please contact System Administrator.'
                                );
                            }
                        );
                },
            }
        );

        $scope.tableDocumentMovements = new NgTableParams(
            {
                page: 1,
                count: 10,
            },
            {
                counts: [],
                getData: function (params) {
                    return $http.get('/api/documents/documentmovements/').then(
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
                                'Could not load Document Movements. Please contact System Administrator.'
                            );
                        }
                    );
                },
            }
        );

        $scope.$watch(
            'searchTermAuto',
            function (newTerm, oldTerm) {
                $scope.tableDocuments.filter({ $: newTerm });
            },
            true
        );

        $scope.view = function (subProcessName, id) {
            var subProcessNameSlug = appFactory.slugify(subProcessName);
            $state.go('app.documents.info', { subProcessName: subProcessNameSlug, documentId: id });
        };
    });

    app.controller('DocumentInfoController', function DocumentInfoController(
        $http,
        $filter,
        $scope,
        toastr,
        NgTableParams,
        appFactory,
        $state,
        $timeout,
        $q
    ) {
        appFactory.getLastActivity($scope.documentId).then(function (data) {
            $scope.lastActivity = data[0];

            // appFactory.getActivities($scope.documentId).then(function(data) {

            // 	$scope.currentStep = response.data[0];
            // 	$scope.lastActivity = data[0];
            // });

            if ($scope.lastActivity.output == null) {
                $http
                    .get('/api/processes/steps/', {
                        params: { stepId: $scope.lastActivity.stepId, process: 'current' },
                    })
                    .then(
                        function (response) {
                            $scope.currentStep = response.data[0];

                            $http
                                .get('/api/processes/steprequirements/', { params: { stepId: $scope.currentStep.id } })
                                .then(
                                    function (response) {
                                        $scope.stepRequirements = response.data;

                                        $scope.currentRequirement = $scope.stepRequirements[0];
                                        $scope.goToRequirement($scope.stepRequirements[0].id);

                                        // $scope.currentRequirement.attachments =
                                        // 	$scope.currentRequirement.stepRequirementAttachments;
                                    },
                                    function (error) {
                                        toastr.error(
                                            'Error ' + error.status + ' ' + error.statusText,
                                            'Could not retrieve Step Requirements Information. Please contact System Administrator.'
                                        );
                                    }
                                );
                        },
                        function (error) {
                            toastr.error(
                                'Error ' + error.status + ' ' + error.statusText,
                                'Could not retrieve current procedure Information. Please contact System Administrator.'
                            );
                        }
                    );
            } else {
                console.log($scope.lastActivity.output.nextStep);
                if ($scope.lastActivity.output.nextStep) {
                    $http
                        .get('/api/processes/steps/', { params: { stepId: $scope.lastActivity.output.nextStep } })
                        .then(
                            function (response) {
                                $scope.currentStep = response.data[0];
                                $http
                                    .get('/api/processes/steprequirements/', {
                                        params: { stepId: $scope.currentStep.id },
                                    })
                                    .then(
                                        function (response) {
                                            $scope.stepRequirements = response.data;

                                            $scope.currentRequirement = $scope.stepRequirements[0];
                                        },
                                        function (error) {
                                            toastr.error(
                                                'Error ' + error.status + ' ' + error.statusText,
                                                'Could not retrieve Step Requirements Information. Please contact System Administrator.'
                                            );
                                        }
                                    );
                            },
                            function (error) {
                                toastr.error(
                                    'Error ' + error.status + ' ' + error.statusText,
                                    'Could not retrieve current procedure. Please contact System Administrator.'
                                );
                            }
                        );
                }
            }

            // $http.get('/api/processes/steps/', {params:{ stepId : $scope.lastActivity.stepId , process : 'next' }}).then(
            //     function(response){
            //         $scope.nextStep = response.data[0];
            // },

            // function(error){
            //     toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not retrieve Next Step Information. Please contact System Administrator.');
            // });
        });

        $http
            .get('/api/documents/documents/', {
                params: { subProcessName: $scope.subProcessName, documentId: $scope.documentId },
            })
            .then(
                function (response) {
                    $scope.document = response.data[0];
                    $scope.loadNotes();
                },
                function (error) {
                    toastr.error(
                        'Error ' + error.status + ' ' + error.statusText,
                        'Could not retrieve Document Information. Please contact System Administrator.'
                    );
                }
            );

        $scope.loadNotes = function () {
            return appFactory.getContentTypeId('note').then(function (data) {
                return appFactory.getNotes($scope.documentId, data).then(function (response) {
                    $scope.notes = response;
                });
            });
        };

        $http.get('/api/documents/documentmovements/', { params: { documentId: $scope.documentId } }).then(
            function (response) {
                $scope.documentMovements = response.data;
            },
            function (error) {
                toastr.error(
                    'Error ' + error.status + ' ' + error.statusText,
                    'Could not retrieve Document Movement Information. Please contact System Administrator.'
                );
            }
        );

        $http.get('/api/processes/steps/').then(
            function (response) {
                $scope.processSteps = response.data;
            },
            function (error) {
                toastr.error(
                    'Error ' + error.status + ' ' + error.statusText,
                    'Could not retrieve Document Movement Information. Please contact System Administrator.'
                );
            }
        );

        $scope.getRequirement = function () {
            for (var i = 0; i < $scope.stepRequirements.length; i++) {
                if ($scope.currentRequirement.id == $scope.stepRequirements[i].id) {
                    return $scope.stepRequirements[i].id;
                }
            }
        };

        $scope.goToRequirement = function (id) {
            for (var i = 0; i < $scope.stepRequirements.length; i++) {
                if ($scope.stepRequirements[i].id == id) {
                    $scope.currentRequirement = $scope.stepRequirements[i];
                    $http
                        .get('/api/processes/steprequirementsattachments/', {
                            params: { stepRequirementId: $scope.currentRequirement.id, documentId: $scope.documentId },
                        })
                        .then(
                            function (response) {
                                $scope.currentRequirement.attachments = response.data;
                            },
                            function (error) {
                                toastr.error(
                                    'Error ' + error.status + ' ' + error.statusText,
                                    'Could not retrieve attachments Information. Please contact System Administrator.'
                                );
                            }
                        );
                }
            }
        };

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

        $scope.takeActions = function (documentId, output, step) {
            $scope.documentMovement = {
                remarks: $scope.remarks,
                outputId: output.id,
                output: output,
                document: documentId,
                name: step.name,
                step: step.id,
                committee: '1',
                status: step.status,
            };

            console.log($scope.documentMovement);
            swal({
                title: 'Submit Output',
                text: 'Continue submitting file as ' + output.name + '?',
                icon: 'info',
                buttons: {
                    cancel: true,
                    confirm: 'Submit',
                },
            }).then((isConfirm) => {
                if (isConfirm) {
                    $http.post('/api/documents/documentmovements/', $scope.documentMovement).then(
                        function () {
                            toastr.success('Success', 'File successfully moved to the next phase.');
                            swal('Success!', 'File successfully moved to the next phase', 'success');
                            $state.reload();
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

        $scope.fileAttachment = [];
        $scope.newAttachmentDescription = '';
        $scope.selectFile = function () {
            $timeout(function () {
                angular.element('#fileAttachment').trigger('click');
            }, 0);
            console.log($scope.newAttachmentDescription);
        };

        $scope.$watch('fileAttachment', function (newValue, oldValue) {
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

        $scope.attachFile = function (stepRequirement) {
            angular.forEach($scope.fileList, function (fileList, index) {
                var newAttachment = {
                    fileName: $scope.fileAttachment[index].name,
                    fileAttachment: $scope.fileAttachment[index],
                    description: $scope.newAttachmentDescription,
                    stepRequirement: stepRequirement.id,
                    document: $scope.documentId,
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
                    swal('Success!', 'New attachment successfully saved', 'success');
                    // $state.reload();
                    $scope.goToRequirement($scope.currentRequirement.id);
                    $scope.fileList.length = 0;
                    $scope.newAttachmentDescription = '';
                },
                function (error) {
                    toastr.error(
                        'Error ' + error.status + ' ' + error.statusText,
                        'Could not create upload attachments. Please contact System Administrator.'
                    );
                }
            );
        };

        $scope.addNote = function (document) {
            $scope.note = {
                committee: 1, //default commiitee to be replaced with
                object_type: 'Document',
                object_id: document.id,
                content_type: '',
                note: $scope.noteDescription,
            };

            return appFactory.getContentTypeId('note').then(function (data) {
                $scope.note.content_type = data;
                console.log($scope.note);
                return $http.post('/api/committees/notes/', $scope.note).then(
                    function () {
                        toastr.success('Success', 'Note added succesfully.');
                        swal('Success!', 'Note added succesfully.', 'success');
                        $scope.loadNotes();
                        $scope.noteDescription = '';
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not create new record. Please contact System Administrator.'
                        );
                    }
                );
            });
        };

        $scope.uploadFile = function (formData) {
            return $http
                .post('/api/processes/steprequirementsattachments/', formData, {
                    transformRequest: angular.identity,
                    headers: { 'Content-Type': undefined },
                })
                .then(
                    function (response) {
                        toastr.success(
                            'Success',
                            appFactory.trimString(response.data.fileName, 9) + ' uploaded successfully.'
                        );
                        swal('Success!', 'New attachment successfully saved', 'success');
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not create new file attachment. Please contact System Administrator.'
                        );
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

    app.controller('DocumentInfoController', function DocumentInfoController(
        $http,
        $filter,
        $scope,
        toastr,
        NgTableParams,
        appFactory,
        $state,
        $timeout,
        blockUI,
        $q
    ) {
        appFactory.getLastActivity($scope.documentId).then(function (data) {
            $scope.lastActivity = data[0];
            if ($scope.lastActivity.output == null) {
                $http
                    .get('/api/processes/steps/', {
                        params: {
                            stepId: $scope.lastActivity.stepId,
                            process: 'current',
                        },
                    })
                    .then(
                        function (response) {
                            $scope.currentStep = response.data[0];

                            $http
                                .get('/api/processes/steprequirements/', {
                                    params: { stepId: $scope.currentStep.id },
                                })
                                .then(
                                    function (response) {
                                        $scope.stepRequirements = response.data;

                                        $scope.currentRequirement = $scope.stepRequirements[0];
                                        $scope.goToRequirement($scope.stepRequirements[0].id);

                                        // $scope.currentRequirement.attachments =
                                        // 	$scope.currentRequirement.stepRequirementAttachments;
                                    },
                                    function (error) {
                                        toastr.error(
                                            'Error ' + error.status + ' ' + error.statusText,
                                            'Could not retrieve Step Requirements Information. Please contact System Administrator.'
                                        );
                                    }
                                );
                        },
                        function (error) {
                            toastr.error(
                                'Error ' + error.status + ' ' + error.statusText,
                                'Could not retrieve current procedure Information. Please contact System Administrator.'
                            );
                        }
                    );
            } else {
                // console.log($scope.lastActivity.output.nextStep);
                $http
                    .get('/api/processes/steps/', {
                        params: { stepId: $scope.lastActivity.output.nextStep },
                    })
                    .then(
                        function (response) {
                            $scope.currentStep = response.data[0];
                            $http
                                .get('/api/processes/steprequirements/', {
                                    params: { stepId: $scope.currentStep.id },
                                })
                                .then(
                                    function (response) {
                                        $scope.stepRequirements = response.data;

                                        $scope.currentRequirement = $scope.stepRequirements[0];
                                    },
                                    function (error) {
                                        toastr.error(
                                            'Error ' + error.status + ' ' + error.statusText,
                                            'Could not retrieve Step Requirements Information. Please contact System Administrator.'
                                        );
                                    }
                                );
                        },
                        function (error) {
                            toastr.error(
                                'Error ' + error.status + ' ' + error.statusText,
                                'Could not retrieve current procedure. Please contact System Administrator.'
                            );
                        }
                    );
            }

            // $http.get('/api/processes/steps/', {params:{ stepId : $scope.lastActivity.stepId , process : 'next' }}).then(
            //     function(response){
            //         $scope.nextStep = response.data[0];
            // },

            // function(error){
            //     toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not retrieve Next Step Information. Please contact System Administrator.');
            // });
        });

        $http
            .get('/api/documents/documents/', {
                params: {
                    subProcessName: $scope.subProcessName,
                    documentId: $scope.documentId,
                },
            })
            .then(
                function (response) {
                    $scope.document = response.data[0];
                    $scope.loadNotes();
                },
                function (error) {
                    toastr.error(
                        'Error ' + error.status + ' ' + error.statusText,
                        'Could not retrieve Document Information. Please contact System Administrator.'
                    );
                }
            );

        $scope.loadNotes = function () {
            return appFactory.getContentTypeId('note').then(function (data) {
                return appFactory.getNotes($scope.documentId, data).then(function (response) {
                    $scope.notes = response;
                });
            });
        };

        $http
            .get('/api/documents/documentmovements/', {
                params: { documentId: $scope.documentId },
            })
            .then(
                function (response) {
                    $scope.documentMovements = response.data;
                },
                function (error) {
                    toastr.error(
                        'Error ' + error.status + ' ' + error.statusText,
                        'Could not retrieve Document Movement Information. Please contact System Administrator.'
                    );
                }
            );

        $http.get('/api/processes/steps/').then(
            function (response) {
                $scope.processSteps = response.data;
            },
            function (error) {
                toastr.error(
                    'Error ' + error.status + ' ' + error.statusText,
                    'Could not retrieve Document Movement Information. Please contact System Administrator.'
                );
            }
        );

        $scope.getRequirement = function () {
            for (var i = 0; i < $scope.stepRequirements.length; i++) {
                if ($scope.currentRequirement.id == $scope.stepRequirements[i].id) {
                    return $scope.stepRequirements[i].id;
                }
            }
        };

        $scope.goToRequirement = function (id) {
            for (var i = 0; i < $scope.stepRequirements.length; i++) {
                if ($scope.stepRequirements[i].id == id) {
                    $scope.currentRequirement = $scope.stepRequirements[i];
                    $http
                        .get('/api/processes/steprequirementsattachments/', {
                            params: {
                                stepRequirementId: $scope.currentRequirement.id,
                                documentId: $scope.documentId,
                            },
                        })
                        .then(
                            function (response) {
                                $scope.currentRequirement.attachments = response.data;
                            },
                            function (error) {
                                toastr.error(
                                    'Error ' + error.status + ' ' + error.statusText,
                                    'Could not retrieve attachments Information. Please contact System Administrator.'
                                );
                            }
                        );
                }
            }
        };

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

        $scope.takeActions = function (documentId, output, step) {
            $scope.documentMovement = {
                remarks: $scope.remarks,
                outputId: output.id,
                output: output,
                document: documentId,
                name: step.name,
                step: step.id,
                committee: '1',
                status: step.status,
            };
            swal({
                title: 'Submit Output',
                text: 'Continue submitting file as ' + output.name + '?',
                icon: 'info',
                buttons: {
                    cancel: true,
                    confirm: 'Submit',
                },
            }).then((isConfirm) => {
                if (isConfirm) {
                    $http.post('/api/documents/documentmovements/', $scope.documentMovement).then(
                        function () {
                            toastr.success('Success', 'File successfully moved to the next phase.');
                            swal('Success!', 'File successfully moved to the next phase', 'success');
                            $state.reload();
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

        var attachmentBlockUI = blockUI.instances.get('attachmentBlockUI');

        $scope.attachFile = function (stepRequirement) {
            attachmentBlockUI.start('Attaching File...');
            angular.forEach($scope.fileList, function (fileList, index) {
                var newAttachment = {
                    fileName: $scope.fileAttachment.attachment[index].name,
                    fileAttachment: $scope.fileAttachment.attachment[index],
                    description: $scope.newAttachment.attachmentDescription,
                    stepRequirement: stepRequirement.id,
                    document: $scope.documentId,
                };
                var formData = new FormData();
                angular.forEach(newAttachment, function (value, key) {
                    formData.append(key, value);
                });
                console.log(newAttachment);
                promises.push($scope.uploadFile(formData));
            });
            $q.all(promises).then(
                function (response) {
                    toastr.success('Success', 'All attachment successfully saved.');
                    $scope.goToRequirement($scope.currentRequirement.id);
                    $scope.fileList.length = 0;
                    $scope.newAttachment.attachmentDescription = '';
                    attachmentBlockUI.stop();
                },
                function (error) {
                    toastr.error(
                        'Error ' + error.status + ' ' + error.statusText,
                        'Could not create upload attachments. Please contact System Administrator.'
                    );
                    attachmentBlockUI.stop();
                }
            );
        };

        $scope.uploadFile = function (formData) {
            return $http
                .post('/api/processes/steprequirementsattachments/', formData, {
                    transformRequest: angular.identity,
                    headers: { 'Content-Type': undefined },
                })
                .then(
                    function (response) {
                        toastr.success(
                            'Success',
                            appFactory.trimStringWithExtension(response.data.fileName, 9) + ' uploaded successfully.'
                        );
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not create new file attachment. Please contact System Administrator.'
                        );
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

        var noteBlockUI = blockUI.instances.get('noteBlockUI');

        $scope.newNote = {
            noteDescription: '',
        };

        $scope.addNote = function (document) {
            noteBlockUI.start('Adding Note...');
            $scope.note = {
                committee: 1, //default commiitee to be replaced with
                object_type: 'Document',
                object_id: document.id,
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
});
