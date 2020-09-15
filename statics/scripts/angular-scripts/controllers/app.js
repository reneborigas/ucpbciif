define(function () {
    'use strict';

    var app = angular.module('app');

    // app.controller('NavBarController', function NavBarController( $http,toastr,$scope, appFactory, appLoginService, $state) {
    //     appFactory.getCurrentUserInfo().then(function (data) {
    //         $scope.user = data;

    //         $scope.loadNotifications($scope.user);

    //         if (!$scope.user) {
    //             $scope.logout();
    //         } else {
    //             $scope.gotToMetro = function () {
    //                 $state.go('main.menu');
    //             };
    //         }
    //     });
    //     $scope.logout = appLoginService.logout;
    //     $scope.showHeader = false;
    //     $scope.showHeader = appLoginService.isLoggedIn();

    //     $scope.loadNotifications = function (user) {
    //             console.log(user.committeeId);
    //             console.log(user.committeeId);

    //                 return appFactory.getNotifications(user.id,user.committeeId).then(function (response) {
    //                     $scope.notifications = response;

    //                     console.log($scope.notifications);
    //                 });

    //     };

    //     $scope.notifView = function (notificationId, object_id,content_type,slug ) {
    //         console.log($scope.user.id);
    //         if($scope.user.committeeId){
    //             $http.post('/api/notifications/viewnotifications/', {
    //                 notificationId: notificationId ,  userId:$scope.user.id ,committeeId:$scope.user.committeeId ,
    //            })
    //            .then(
    //                function (response) {
    //                    console.log(response);

    //                },
    //                function (error) {
    //                    toastr.error(
    //                        'Error ' + error.status + ' ' + error.statusText,
    //                        'Could not retrieve view notification. Please contact System Administrator.'
    //                    );
    //                }
    //            );

    //         }else{
    //             $http.post('/api/notifications/viewnotifications/', {
    //                 notificationId: notificationId , userId:$scope.user.id ,committeeId:$scope.user.committeeId ,
    //            })
    //            .then(
    //                function (response) {
    //                    console.log(response);

    //                },
    //                function (error) {
    //                    toastr.error(
    //                        'Error ' + error.status + ' ' + error.statusText,
    //                        'Could not retrieve view notification. Please contact System Administrator.'
    //                    );
    //                }
    //            );

    //         }

    //         if(content_type == 33){//documents
    //             // $state.go('app.loans.info', { loanId: loanId });

    //                 return appFactory.getNotifications($scope.user.id,$scope.user.committeeId).then(function (response) {
    //                     $scope.notifications = response;
    //                     $state.go('app.documents.info', { subProcessName: slug, documentId: object_id });
    //                     console.log($scope.notifications);
    //                 });

    //         }

    //     };

    // });

    app.controller('NavBarController', function NavBarController($http, toastr, $scope, appFactory, appLoginService, $state) {
        appFactory.getCurrentUserInfo().then(function (data) {
            $scope.user = data;

            $scope.loadNotifications($scope.user);

            if (!$scope.user) {
                $scope.logout();
            } else {
                $scope.gotToMetro = function () {
                    $state.go('main.menu');
                };
            }
        });
        $scope.logout = appLoginService.logout;
        $scope.showHeader = false;
        $scope.showHeader = appLoginService.isLoggedIn();

        $scope.loadNotifications = function (user) {
            $scope.notifClick = true;

            return appFactory.getNotifications(user.id, user.committeeId).then(function (response) {
                $scope.notifications = response;

                console.log($scope.notifications);
                $scope.notifClick = false;
            });
        };

        $scope.notifView = function (notificationId, object_id, content_type, slug) {
            console.log($scope.user.id);
            if ($scope.user.committeeId) {
                $http
                    .post('/api/notifications/viewnotifications/', {
                        notificationId: notificationId,
                        userId: $scope.user.id,
                        committeeId: $scope.user.committeeId,
                    })
                    .then(
                        function (response) {
                            console.log(response);
                        },
                        function (error) {
                            toastr.error(
                                'Error ' + error.status + ' ' + error.statusText,
                                'Could not retrieve view notification. Please contact System Administrator.'
                            );
                        }
                    );
            } else {
                $http
                    .post('/api/notifications/viewnotifications/', {
                        notificationId: notificationId,
                        userId: $scope.user.id,
                        committeeId: $scope.user.committeeId,
                    })
                    .then(
                        function (response) {
                            console.log(response);
                        },
                        function (error) {
                            toastr.error(
                                'Error ' + error.status + ' ' + error.statusText,
                                'Could not retrieve view notification. Please contact System Administrator.'
                            );
                        }
                    );
            }

            if (content_type == 33) {
                //documents
                // $state.go('app.loans.info', { loanId: loanId });

                return appFactory.getNotifications($scope.user.id, $scope.user.committeeId).then(function (response) {
                    $scope.notifications = response;
                    $state.go('app.documents.info', { subProcessName: slug, documentId: object_id });
                    console.log($scope.notifications);
                });
            }
        };
    });

    app.controller('FooterController', function FooterController($scope) {
        $scope.date = new Date();
    });

    app.controller('SideBarController', function SideBarController($http, $scope, toastr, $state, $timeout, appFactory) {
        $http.get('/api/processes/subprocesses/').then(
            function (response) {
                $scope.subProcesses = response.data;
                $scope.subProcessSlugs = [];
                angular.forEach($scope.subProcesses, function (subProcess) {
                    $scope.subProcessSlugs.push({
                        name: subProcess.name,
                        slug: appFactory.slugify(subProcess.name),
                    });
                });
            },
            function (error) {
                toastr.error('Error ' + error.status + error.statusText, 'Could not retrieve Sub Processes. Please contact System Administrator.');
            }
        );
        var app = JSON.parse(localStorage.getItem('selectedApp'));
        $scope.navDirectory = app['navBar'];
    });

    app.controller('MetroController', function MetroController($scope, $state, $http, $sce, appFactory) {
        appFactory.getCurrentUserApps().then(function (data) {
            $scope.apps = data;
        });

        $scope.goToApp = function (app) {
            var appInfo = {
                name: app.name,
                navBar: app.navDirectory,
            };
            localStorage.selectedApp = JSON.stringify(appInfo);
            $state.go('app.dashboard');
        };
    });

    app.controller('RerouteController', function RerouteController($scope, $state, $location) {
        $scope.goToPreviousState = function () {
            if ($scope.previousState) {
                $location.path($scope.previousState.url);
            } else {
                $state.go('app.dashboard');
            }
        };
    });
});
