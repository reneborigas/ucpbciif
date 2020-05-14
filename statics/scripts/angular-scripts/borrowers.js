define(function(){
    'use strict';

    var lmsApp =  angular.module('lmsApp');

    lmsApp.controller('BorrowerListController',
        function BorrowerListController($http, $filter, $scope, toastr, NgTableParams, lmsService, $state, $timeout){

            $scope.tableBorrowers = new NgTableParams({
                page:1,
                count: 10,
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
                            return page
                    
                    },
                        function(error){
                            toastr.error('Error '+ error.status +' '+ error.statusText, 'Could not load Borrowers. Please contact System Administrator.'); 
                    })
                }
            });

            $scope.view = function(id){
                $state.go('borrowers.info', {borrowerId:id});
            }

            $scope.edit = function(id){
                $state.go('borrowers.edit', {borrowerId:id});
            }

            // $scope.delete = function(id){
            //     console.log(id)
            // }

        }        
    );

    lmsApp.controller('BorrowerAddController',
        function BorrowerAddController($http, $filter, $scope, toastr, NgTableParams, lmsService, $state, $timeout){

            lmsService.getGenders().then(function(data) {
                $scope.genders = data
            });

            $scope.newBorrower = {
                firstname: '',
                middlename: '',
                lastname: '',
                status: 'Active',
                description: '',
                remarks: '',                
                createdBy: lmsService.getCurrentUser(),
                borrowerPersonalInfo: [{
                    birthdate: '',
                    birthplace: '',
                    gender: '',
                    weight: '',
                    height: '',
                }],
            }

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

    lmsApp.controller('BorrowerInfoController',
        function BorrowerInfoController($http, $filter, $scope, toastr, NgTableParams, lmsService, $state, $timeout){

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

    lmsApp.controller('BorrowerEditController',
        function BorrowerEditController($http, $filter, $scope, toastr, NgTableParams, lmsService, $state, $timeout){

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