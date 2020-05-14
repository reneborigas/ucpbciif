define(function(){
    'use strict';

    var app =  angular.module('app');

    app.controller('BorrowerListController',
        function BorrowerListController($http, $filter, $scope, $state, $timeout, toastr, appFactory, NgTableParams){

            $scope.tableBorrowers = new NgTableParams({
                page:1,
                count: 15,
                },
                {
                getData: function(params){
                    return $http.get('/api/borrowers/borrowers/').then(
                        function(response){
                            var filteredData = params.filter() ? $filter('filter')(response.data, params.filter()) : response.data;
                            var orderedData = params.sorting() ? $filter('orderBy')(filteredData, params.orderBy()) : filteredData;
                            var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                            params.total(response.data.length);

                            var page = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
                            console.table(page)
                            return page
                    
                    },
                        function(error){
                            toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not load Borrowers. Please contact System Administrator.'); 
                    })
                }
            });

            // $scope.view = function(id){
            //     $state.go('borrowers.info', {borrowerId:id});
            // }

            // $scope.edit = function(id){
            //     $state.go('borrowers.edit', {borrowerId:id});
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


            // $scope.newBorrower = {
            //     firstname: '',
            //     middlename: '',
            //     lastname: '',
            //     status: 'Active',
            //     description: '',
            //     remarks: '',                
            //     createdBy: appFactory.getCurrentUser(),
            //     borrowerPersonalInfo: [{
            //         birthdate: '',
            //         birthplace: '',
            //         gender: '',
            //         weight: '',
            //         height: '',
            //     }],
            // }

            // $scope.newBorrower = {
            //     status: '',
            //     clientSince: '',
            //     remarks: '',
            //     createdBy: appFactory.getCurrentUser(),
            //     dateCreated: '',
            //     dateUpdated: '',
            //     isDeleted: '',
            // }

            $scope.borrower = {
                name : '',
                icRiskRating : '',
                tin : '',
                cdaRegistrationDate : '',
                initialMembershipSize : '',
                membershipSize : '',
                paidUpCapitalInitial : '',
                noOfCooperators : '',
                coconutFarmers : '',
                authorized : '',
                fullyPaidSharesNo : '',
                bookValue : '',
                parValue : '',
                paidUp : '',
                fullyPaidPercent : '',
                initialPaidUpShare : '',
                address : '',
                telNo : '',
                emailAddress : '',
                phoneNo : '',
                fax : '',
                cooperativeType : '',
                description : '',
                remarks : '',
                createdBy : '',
                dateCreated : '',
                dateUpdated : '',
                isDeleted : '',
                directors: [{
                    name : '',
                    department : '',
                    position : '',
                    educationalAttainment : '',
                    age : '',
                    yearsInCooop : '',
                    oSLoanWithCoop : '',
                    status : '',
                    createdBy : '',
                    dateCreated : '',
                    dateUpdated : '',
                    isDeleted : '',
                }],
                standingCommittees: [{
                    name : '',
                    position : '',
                    educationalAttainment : '',
                    age : '',
                    yearsInCooop : '',
                    oSLoanWithCoop : '',
                    status : '',
                    createdBy : '',
                    dateCreated : '',
                    dateUpdated : '',
                    isDeleted : '',
                }],
                grants: [{
                    cooperative : '',
                    donor : '',
                    projectType : '',
                    amount : '',
                    projectStatus : '',
                    createdBy : '',
                    dateCreated : '',
                    dateUpdated : '',
                    isDeleted : '',
                }],
            }

            $scope.addCommittee = function(){
                $scope.borrower.standingCommittees.push({
                    name : '',
                    position : '',
                    educationalAttainment : '',
                    age : '',
                    yearsInCooop : '',
                    oSLoanWithCoop : '',
                    status : '',
                    createdBy : '',
                    dateCreated : '',
                    dateUpdated : '',
                    isDeleted : '',
                })
            }

            $scope.removeCommittee = function(index){
                $scope.borrower.standingCommittees.splice(index,1)
            }

            // $scope.newContactPerson = {
            //     firstname: '',
            //     middlename: '',
            //     lastname: '',
            //     telNo: '',
            //     emailAddress: '',
            //     phoneNo: '',
            //     createdBy: appFactory.getCurrentUser(),
            //     dateCreated: '',
            //     dateUpdated: '',
            //     isDeleted: '',
            // }


            $scope.save = function(){
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
                            $http.post('/api/borrowers/borrowers/', $scope.newBorrower)
                                .then(function(){                      
                                    toastr.success('Success','New borrower created.');     
                                    swal("Success!", "New Borrower Created.", "success");      
                                    $state.go('borrowers.list');
                            },
                            function(error){
                                toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not create new record. Please contact System Administrator.'); 
                            }); 
                        }
                });
            }

        }        
    );

    app.controller('BorrowerInfoController',
        function BorrowerInfoController($http, $filter, $scope, toastr, NgTableParams, appFactory, $state, $timeout){

            $http.get('/api/borrowers/borrowers/', {params:{ borrowerId : $scope.borrowerId }}).then(
                function(response){
                    $scope.borrower = response.data[0];
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