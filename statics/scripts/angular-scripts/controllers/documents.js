define(function(){
    'use strict';

    var app =  angular.module('app');

    app.controller('DocumentListController',
        function DocumentListController($http, $filter, $scope, toastr, NgTableParams, $state, $timeout, appFactory){

            $scope.tableDocuments = new NgTableParams({
                page:1,
                count: 15,
                },
                {
                getData: function(params){
                    return $http.get('/api/documents/documents/', {params:{ documentId :  $scope.documentId }}).then(
                        function(response){
                            var filteredData = params.filter() ? $filter('filter')(response.data, params.filter()) : response.data;
                            var orderedData = params.sorting() ? $filter('orderBy')(filteredData, params.orderBy()) : filteredData;
                            var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                            params.total(response.data.length);

                            var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                            return page
                    
                    },
                        function(error){
                            toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not load Documetns. Please contact System Administrator.'); 
                    })
                }
            });

            $scope.tableDocumentMovements = new NgTableParams({
                page:1,
                count: 10,
                },
                {
                counts: [],        
                getData: function(params){
                    return $http.get('/api/documents/documentmovements/').then(
                        function(response){
                            var filteredData = params.filter() ? $filter('filter')(response.data, params.filter()) : response.data;
                            var orderedData = params.sorting() ? $filter('orderBy')(filteredData, params.orderBy()) : filteredData;
                            var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                            params.total(response.data.length);
                            
                            $scope.countFrom = ((params.page() - 1) * params.count()) + 1;
                            $scope.countTo = params.count() * params.page() > params.total() ? params.total() : params.count() * params.page();
                            $scope.totalRecords = params.total();
                            var count = $scope.tableDocumentMovements._params.count
                            $scope.globalPageCount = count.toString()

                            var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                            return page
                    
                    },
                        function(error){
                            toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not load Document Movements. Please contact System Administrator.'); 
                    })
                }
            });

            // $scope.$watch('globalPageCount', function(newValue, oldValue) {
            //     if (newValue){
            //         $scope.tableDocuments._params.count = newValue;
            //     }
            // }, true);

            // $scope.$watch('searchTermAuto', function(newTerm, oldTerm) {
            //     $scope.tableDocuments.filter({ $: newTerm });
            // }, true);

            $scope.view = function(subProcessName,id){
                var subProcessNameSlug = appFactory.slugify(subProcessName)
                $state.go('app.documents.info', { subProcessName : subProcessNameSlug, documentId : id});
            }

        }        
    );
    app.controller('DocumentInfoController',
        function DocumentInfoController($http, $filter, $scope, toastr, NgTableParams, appFactory, $state, $timeout){

            appFactory.getLastActivity($scope.documentId).then(function(data) {
                $scope.lastActivity = data[0];   
                if ($scope.lastActivity.output == null){ 
                    $http.get('/api/processes/steps/', {params:{ stepId : $scope.lastActivity.stepId , process : 'current' }}).then(
                    function(response){
                        $scope.currentStep = response.data[0]; 
                    },
                    function(error){
                        toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not retrieve current procedure Information. Please contact System Administrator.'); 
                    });
                }else{
                    console.log($scope.lastActivity.output.nextStep);
                    $http.get('/api/processes/steps/', {params:{ stepId : $scope.lastActivity.output.nextStep  }}).then(
                        function(response){
                            $scope.currentStep = response.data[0];    
                    },
                    function(error){
                        toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not retrieve current procedure. Please contact System Administrator.'); 
                    });
                    console.log( $scope.currentStep);
                }

              
           
                // $http.get('/api/processes/steps/', {params:{ stepId : $scope.lastActivity.stepId , process : 'next' }}).then(
                //     function(response){
                //         $scope.nextStep = response.data[0]; 
                // },
               
                // function(error){
                //     toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not retrieve Next Step Information. Please contact System Administrator.'); 
                // });
                
               
            });

            $http.get('/api/documents/documents/', {params:{ subProcessName : $scope.subProcessName , documentId : $scope.documentId }}).then(
                function(response){
                    $scope.document = response.data[0];
            },
            function(error){
                toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not retrieve Document Information. Please contact System Administrator.'); 
            });

            $http.get('/api/documents/documentmovements/', {params:{ documentId : $scope.documentId }}).then(
                function(response){
                    $scope.documentMovements = response.data;
            },
            function(error){
                toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not retrieve Document Movement Information. Please contact System Administrator.'); 
            });

            $http.get('/api/processes/steps/').then(
                function(response){
                    $scope.processSteps = response.data;
            },
            function(error){
                toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not retrieve Document Movement Information. Please contact System Administrator.'); 
            });

                 
            
            
            $scope.activityTemplates = [
                {
                    templateNumber: 1,
                    name: "Activities",
                    icon: "fad fa-info-square",
                    templateUrl: '/statics/partials/pages/documents/info/activities.html',
                },]

            $scope.templates = [
                {
                    templateNumber: 1,
                    name: "Basic Information",
                    icon: "fad fa-info-square",
                    templateUrl: '/statics/partials/pages/documents/info/basic.html',
                },
                {
                    templateNumber: 2,
                    name: "Contact Details",
                    icon: "fad fa-address-book",
                    templateUrl: '/statics/partials/pages/documents/info/contact.html',
                },
                {
                    templateNumber: 3,
                    name: "Background",
                    icon: "fad fa-user-friends",
                    templateUrl: '/statics/partials/pages/documents/info/directorCommittee.html',
                },
                {
                    templateNumber: 4,
                    name: "Grants",
                    icon: "fad fa-coin",
                    templateUrl: '/statics/partials/pages/documents/info/grants.html',
                },
                {
                    templateNumber: 5,
                    name: "History",
                    icon: "fad fa-history",
                    templateUrl: '/statics/partials/pages/documents/info/history.html',
                }
            ]

            $scope.currentTemplate = $scope.templates[0];
            $scope.currentActivityTemplate = $scope.activityTemplates[0];
            
            $scope.getTemplate = function(){
                for (var i = 0; i < $scope.templates.length; i++) {
                    if ($scope.currentTemplate.templateNumber == $scope.templates[i].templateNumber) {
                        return $scope.templates[i].templateUrl;
                    }
                }
            }
            $scope.getActiviyTemplate = function(){
                for (var i = 0; i < $scope.activityTemplates.length; i++) {
                    if ($scope.currentActivityTemplate.templateNumber == $scope.activityTemplates[i].templateNumber) {
                        return $scope.activityTemplates[i].templateUrl;
                    }
                }
            }
            $scope.goToTemplate = function(templateNumber){
                for (var i = 0; i < $scope.templates.length; i++) {
                    if ($scope.templates[i].templateNumber == templateNumber) {
                        $scope.currentTemplate = $scope.templates[i]
                    }
                }
            }
            $scope.goToActivityTemplate = function(templateNumber){
                for (var i = 0; i < $scope.activityTemplates.length; i++) {
                    if ($scope.activityTemplates[i].templateNumber == templateNumber) {
                        $scope.currentActivityTemplate = $scope.activityTemplates[i]
                    }
                }
            }

            $scope.takeActions = function(documentId,output,step){
                console.log(output.id);
                
                $scope.documentMovement = {
                    outputId:output.id,
                    output:output,
                    document:documentId,
                    name:step.name,
                    step:step.id,
                    committee:'1',
                    status:step.status
                }

                console.log( $scope.documentMovement);
                swal({
                    title: "Submit Output",
                    text: "Continue submitting file as " + output.name + "?",
                    icon: "info",
                    buttons:{
                        cancel: true,
                        confirm: "Submit",
                    }
                }).then((isConfirm)=>{                              
                        if (isConfirm){
                            $http.post('/api/documents/documentmovements/', $scope.documentMovement)
                                .then(function(){                      
                                    toastr.success('Success','File successfully moved to the next phase.');     
                                    swal("Success!", "File successfully moved to the next phase", "success");      
                                    $state.reload();
                                    ;
                            },
                            function(error){
                                toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not create new record. Please contact System Administrator.'); 
                            }); 
                        }
                });
            }
        }        
    );

    app.controller('DocumentAddController',
        function DocumentAddController($http, $filter, $scope, toastr, NgTableParams, $state, $timeout){

                $scope.loan={loanName:'',loanAmount:'',borrower:''}

                $scope.save = function(){
                    swal({
                        title: "Create Document",
                        text: "Do you want to save and create this loan?",
                        icon: "info",
                        buttons:{
                            cancel: true,
                            confirm: "Create",
                        }
                    }).then((isConfirm)=>{                              
                            if (isConfirm){
                                $http.post('/api/documents/documents/', $scope.loan)
                                    .then(function(){                      
                                        toastr.success('Success','New loan created.');     
                                        swal("Success!", "New Borrower Created.", "success");      
                                        $state.go('app.documents.list');
                                },
                                function(error){
                                    toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not create new record. Please contact System Administrator.'); 
                                }); 
                            }
                    });

                }


        }        
    );  
});