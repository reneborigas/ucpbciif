define(function(){
    'use strict';

    var app =  angular.module('app');

    app.controller('LoanListController',
        function LoanListController($http, $filter, $scope, toastr, NgTableParams, $state, $timeout){

            $scope.tableLoans = new NgTableParams({
                page:1,
                count: 15,
                },
                {
                getData: function(params){
                    return $http.get('/api/loans/loans/').then(
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


        }        
    );
    app.controller('LoanAddController',
        function LoanAddController($http, $filter, $scope, toastr, NgTableParams, $state, $timeout){

                $scope.loan={loanName:'',loanAmount:'',borrower:''}

                $scope.save = function(){
                    swal({
                        title: "Create Loan",
                        text: "Do you want to save and create this loan?",
                        icon: "info",
                        buttons:{
                            cancel: true,
                            confirm: "Create",
                        }
                    }).then((isConfirm)=>{                              
                            if (isConfirm){
                                $http.post('/api/loans/loans/', $scope.loan)
                                    .then(function(){                      
                                        toastr.success('Success','New loan created.');     
                                        swal("Success!", "New Borrower Created.", "success");      
                                        $state.go('app.loans.list');
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