define(function(){
    'use strict';

    var app =  angular.module('app');

    app.controller('BorrowerListController',
        function BorrowerListController($http, $filter, $scope, $state, $timeout, toastr, appFactory, NgTableParams){

            $scope.totalRecords;
            $scope.countFrom;
            $scope.countTo;

            $scope.tableBorrowers = new NgTableParams({
                page:1,
                count: 10,
                },
                {
                counts: [],        
                getData: function(params){
                    return $http.get('/api/borrowers/cooperatives/').then(
                        function(response){
                            var filteredData = params.filter() ? $filter('filter')(response.data, params.filter()) : response.data;
                            var orderedData = params.sorting() ? $filter('orderBy')(filteredData, params.orderBy()) : filteredData;
                            var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                            params.total(response.data.length);
                            
                            $scope.countFrom = ((params.page() - 1) * params.count()) + 1;
                            $scope.countTo = params.count() * params.page() > params.total() ? params.total() : params.count() * params.page();
                            $scope.totalRecords = params.total();
                            var count = $scope.tableBorrowers._params.count
                            $scope.globalPageCount = count.toString()

                            var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                            return page
                    
                    },
                        function(error){
                            toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not load Borrowers. Please contact System Administrator.'); 
                    })
                }
            });

            $scope.$watch('searchTermAuto', function(newTerm, oldTerm) {
                $scope.tableBorrowers.filter({ $: newTerm });
            }, true);

            $scope.$watch('globalPageCount', function(newValue, oldValue) {
                if (newValue){
                    $scope.tableBorrowers._params.count = newValue;
                }
            }, true);

            $scope.view = function(id){
                $state.go('app.borrowers.info', {borrowerId:id});
            }

            // $scope.edit = function(id){
            //     $state.go('app.borrowers.edit', {id:id});
            // }

            // $scope.delete = function(id){
            //     console.log(id)
            // }

        }        
    );

    app.controller('BorrowerAddController',
        function BorrowerAddController($http, $filter, $scope, toastr, NgTableParams, appFactory, $state, $timeout){

            $scope.steps = [
                {
                    step: 1,
                    name: "Basic Info",
                    desc: "Borrower Information",
                    templateUrl: '/statics/partials/pages/borrowers/wizard/step1.html',
                },
                {
                    step: 2,
                    name: "Structure",
                    desc: "Incorporation Details",
                    templateUrl: '/statics/partials/pages/borrowers/wizard/step2.html',
                },
                {
                    step: 3,
                    name: "Committee",
                    desc: "Director and Committee Info",
                    templateUrl: '/statics/partials/pages/borrowers/wizard/step3.html',
                },
                {
                    step: 4,
                    name: "Grants",
                    desc: "Grant Info",
                    templateUrl: '/statics/partials/pages/borrowers/wizard/step4.html',
                }
            ]

            $scope.currentStep = 1;

            $scope.getStepTemplate = function(){
                for (var i = 0; i < $scope.steps.length; i++) {
                    if ($scope.currentStep == $scope.steps[i].step) {
                        return $scope.steps[i].templateUrl;
                    }
                }
            }

            $scope.goToStep = function(step){
                $scope.currentStep = step;
                $scope.changeStep = true;
            }

            $scope.nextStep = function(){
                $scope.changeStep = true;
                if ($scope.wizardForm.$valid){
                    console.log($scope.borrower)
                    $scope.currentStep = $scope.currentStep + 1;
                }
            }

            $scope.prevStep = function(){
                $scope.currentStep = $scope.currentStep - 1;
            }

            appFactory.getGenders().then(function(data) {
                $scope.genders = data
            });

            appFactory.getCooperativeType().then(function(data) {
                $scope.cooperativetypes = data
            });

            $scope.cooperative = {
                name : '',
                icRiskRating : '',
                tin : '',
                cdaRegistrationDate : '',
                initialMembershipSize : 0,
                membershipSize : 0,
                paidUpCapitalInitial : 0,
                noOfCooperators : 0,
                coconutFarmers : 0,
                authorized : 0,
                fullyPaidSharesNo : 0,
                bookValue : 0,
                parValue : 0,
                paidUp : 0,
                fullyPaidPercent : 0,
                initialPaidUpShare : 0,
                address : '',
                telNo : '',
                emailAddress : '',
                phoneNo : '',
                fax : '',
                cooperativeType : '',
                description : '',
                remarks : '',
                createdBy : appFactory.getCurrentUser(),
                directors: [{
                    name : '',
                    department : '',
                    position : '',
                    educationalAttainment : '',
                    age : '',
                    yearsInCoop : '',
                    oSLoanWithCoop : '',
                    status : '',
                    createdBy : appFactory.getCurrentUser(),
                }],
                standingCommittees: [{
                    name : '',
                    position : '',
                    educationalAttainment : '',
                    age : '',
                    yearsInCoop : '',
                    oSLoanWithCoop : '',
                    status : '',
                    createdBy : appFactory.getCurrentUser(),
                }],
                grants: [{
                    cooperative : '',
                    donor : '',
                    projectType : '',
                    amount : 0,
                    projectStatus : '',
                    createdBy : appFactory.getCurrentUser(),
                }],
            }

            $scope.contactPerson = {
                firstname: '',
                middlename: '',
                lastname: '',
                address: '',
                telNo: '',
                emailAddress: '',
                phoneNo: '',
                createdBy: appFactory.getCurrentUser(),
            }

            $scope.borrower = {
                cooperative: '',
                contactPerson: '',
                status: '',
                clientSince: '',
                remarks: '',
                createdBy: appFactory.getCurrentUser(),
            }



            $scope.addCommittee = function(){
                $scope.borrower.standingCommittees.push({
                    name : '',
                    position : '',
                    educationalAttainment : '',
                    age : '',
                    yearsInCoop : '',
                    oSLoanWithCoop : '',
                    status : '',
                    createdBy : '',
                })
            }

            $scope.removeCommittee = function(index){
                $scope.borrower.standingCommittees.splice(index,1)
            }

            $scope.addDirector = function(){
                $scope.borrower.directors.push({
                    name : '',
                    department : '',
                    position : '',
                    educationalAttainment : '',
                    age : '',
                    yearsInCoop : '',
                    oSLoanWithCoop : '',
                    status : '',
                    createdBy : appFactory.getCurrentUser(),
                })
            }

            $scope.removeDirector = function(index){
                $scope.borrower.directors.splice(index,1)
            }

            $scope.save = function(){
                console.log($scope.borrower)
                if ($scope.wizardForm.$valid){
                    swal({
                        title: "Create Borrower",
                        text: "Do you want to save and create this borrower?",
                        icon: "info",
                        buttons:{
                            cancel: true,
                            confirm: "Create",
                        }
                    }).then((isConfirm)=>{                              
                            if (isConfirm){
                                $http.post('/api/borrowers/cooperatives/', $scope.cooperative)
                                    .then(function(responseCooperative){
                                        return $http.post('/api/borrowers/contactperson/',$scope.contactPerson)
                                            .then(function(responseContactPerson){

                                                $scope.borrower.cooperative = responseCooperative.data.id;
                                                $scope.borrower.cooperative = responseContactPerson.data.id;

                                                return $http.post('/api/borrowers/borrowers',$scope.borrower)
                                                    .then(function(){

                                                },function(error){
                                                    toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not create new borrower. Please contact System Administrator.'); 
                                                })
                                            },function(error){
                                                toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not create new contact person. Please contact System Administrator.'); 
                                            })
                                        // toastr.success('Success','New borrower created.');     
                                        // swal("Success!", "New Borrower Created.", "success");      
                                        // $state.go('app.borrowers.list');

                                },
                                function(error){
                                    toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not create new cooperative. Please contact System Administrator.'); 
                                }); 
                            }
                    });
                }
            }

        }        
    );

    app.controller('BorrowerInfoController',
        function BorrowerInfoController($http, $filter, $scope, toastr, NgTableParams, appFactory, $state, $timeout){

            $http.get('/api/borrowers/borrowers/', {params:{ borrowerId : $scope.borrowerId }}).then(
                function(response){
                    $scope.borrower = response.data[0];
                    console.log($scope.borrower)
            },
            function(error){
                toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not retrieve Borrower Information. Please contact System Administrator.'); 
            });

            $scope.edit = function(id){
                $state.go('borrowers.edit', {borrowerId:id});
            }

            // $scope.delete = function(id){
            //     console.log(id)
            // }

        }        
    );

    app.controller('BorrowerEditController',
        function BorrowerEditController($http, $filter, $scope, toastr, NgTableParams, appFactory, $state, $timeout){

            $http.get('/api/borrowers/borrowers/', {params:{ borrowerId : $scope.borrowerId }}).then(
                function(response){
                    $scope.borrower = response.data[0];
            },
            function(error){
                toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not retrieve Borrower Information. Please contact System Administrator.'); 
            });

            $scope.goBack = function(id){
                $state.go('borrowers.info', {borrowerId:id});
            }

            $scope.update = function(id){
                swal({
                    title: "Update Borrower",
                    text: "Do you want to update this borrower?",
                    icon: "info",
                    buttons:{
                        cancel: true,
                        confirm: "Update",
                    }
                }).then((isConfirm)=>{                              
                        if (isConfirm){
                            $http.patch('/api/borrowers/borrowers/'+ id +'/', $scope.borrower)
                                .then(function(){                      
                                    toastr.success('Success','Borrower updated.');     
                                    swal("Success!", "Borrower Updated.", "success");      
                                    $state.go('borrowers.info',({ borrowerId: id }));
                            },
                            function(error){
                                toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not update record. Please contact System Administrator.'); 
                            }); 
                        }
                });
            }
            
        }        
    );

});