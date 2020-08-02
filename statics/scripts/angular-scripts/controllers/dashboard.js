define(function () {
    'use strict';

    var app = angular.module('app');

    app.controller('DashboardController', function DashboardController(
        $http,
        $filter,
        $scope,
        toastr,
        NgTableParams,
        appFactory,
        $state,
        $timeout
    ) {

        

        // fullCalendar = FullCalendar;
        $scope.loadCalendar = function(fullCalendar){

            console.log($scope.calendarData);
            var calendarElement = document.getElementById('calendar');
            var calendar = new fullCalendar.Calendar(calendarElement, {
                headerToolbar: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek',
                },
                height: 800,
                contentHeight: 750,
                aspectRatio: 3,
                views: {
                    dayGridMonth: { buttonText: 'month' },
                    timeGridWeek: { buttonText: 'week' },
                    timeGridDay: { buttonText: 'day' },
                    listDay: { buttonText: 'list' },
                    listWeek: { buttonText: 'list' },
                },
                defaultView: 'listWeek',
                initialDate: new Date(),
                navLinks: true, // can click day/week names to navigate views
                editable: false,
                selectable: true,
                selectMirror: true,
                dayMaxEvents: true, // allow "more" link when too many events
                // eventSources: {
                //     url: 'http://35.240.176.124:8000/api/loans/amortizationitemscalendar/',
                //     method: 'GET',
                //     extraParams: {
                //       custom_param1: 'something',
                //       custom_param2: 'somethingelse'
                //     },
                //     failure: function() {
                //       alert('there was an error while fetching events!');
                //     },
                //     color: 'yellow',   // a non-ajax option
                //     textColor: 'black' // a non-ajax option
                //   }
                events:  $scope.calendarData,
                // events: $scope.calendarData,
                //     {
                //         title: 'Long Event',
                //         start: '2020-06-07',
                //         end: '2020-06-10',
                //     },
                //     {
                //         groupId: 999,
                //         title: 'Repeating Event',
                //         start: '2020-06-09T16:00:00',
                //     },
                //     {
                //         groupId: 999,
                //         title: 'Repeating Event',
                //         start: '2020-06-16T16:00:00',
                //     },
                //     {
                //         title: 'Conference',
                //         start: '2020-06-11',
                //         end: '2020-06-13',
                //         className: 'fc-event-solid-danger fc-event-light',
                //         description: 'Lorem ipsum dolor sit ctetur adipi scing',
                //     },
                //     {
                //         title: 'Meeting',
                //         start: '2020-06-12T10:30:00',
                //         end: '2020-06-12T12:30:00',
                //     },
                //     {
                //         title: 'Lunch',
                //         start: '2020-06-12T12:00:00',
                //     },
                //     {
                //         title: 'Meeting',
                //         start: '2020-06-12T14:30:00',
                //     },
                //     {
                //         title: 'Happy Hour',
                //         start: '2020-06-12T17:30:00',
                //     },
                //     {
                //         title: 'Dinner',
                //         start: '2020-06-12T20:00:00',
                //     },
                //     {
                //         title: 'Birthday Party',
                //         start: '2020-06-13T07:00:00',
                //     },
                //     {
                //         title: 'Click for Google',
                //         url: 'http://google.com/',
                //         start: '2020-06-28',
                //     },
                // ],
            });
    
            calendar.render();

        };


        $http.get('/api/loans/amortizationitemscalendar/' )
        .then(
            function (response) {
                $scope.calendarData = response.data;
                $scope.loadCalendar(FullCalendar);
                $scope.loadCurrentUser();
                
            },
            function (error) {
                toastr.error(
                    'Error ' + error.status + ' ' + error.statusText,
                    'Could not retrieve Borrower Information. Please contact System Administrator.'
                );
            }
        );
      


        $scope.loadCurrentUser = function () {
            return appFactory.getCurrentUserInfo().then(function (data) {
            $scope.user = data;

            $scope.loadNotifications($scope.user); 
        });
        }
        

        $scope.loadNotifications = function (user) { 
                console.log(user.committeeId);
                console.log(user.committeeId);
                 
                    return appFactory.getNotifications(user.id,user.committeeId).then(function (response) {
                        $scope.notifications = response;
    
                        console.log($scope.notifications);
                       
                    });
            
        }; 

        $scope.notifView = function (notificationId, object_id,content_type,slug ) {
            console.log($scope.user.id);
            if($scope.user.committeeId){
                $http.post('/api/notifications/viewnotifications/', {
                    notificationId: notificationId ,  userId:$scope.user.id ,committeeId:$scope.user.committeeId ,
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


            }else{
                $http.post('/api/notifications/viewnotifications/', {
                    notificationId: notificationId , userId:$scope.user.id ,committeeId:$scope.user.committeeId ,
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
            
            if(content_type == 33){//documents
                // $state.go('app.loans.info', { loanId: loanId }); 
                  
                        $state.go('app.documents.info', { subProcessName: slug, documentId: object_id });
                      
              
        
            }

        };

    });
});
