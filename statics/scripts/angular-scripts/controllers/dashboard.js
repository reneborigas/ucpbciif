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
        $scope.loadCalendar = function (fullCalendar) {
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
                initialView: 'dayGridMonth',
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
                events: $scope.calendarData,
            });

            calendar.render();
        };

        $http.get('/api/loans/amortizationitemscalendar/').then(
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
        };

        $scope.loadNotifications = function (user) {
            console.log(user.committeeId);
            console.log(user.committeeId);

            return appFactory.getNotifications(user.id, user.committeeId).then(function (response) {
                $scope.notifications = response;

                console.log($scope.notifications);
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

                $state.go('app.documents.info', { subProcessName: slug, documentId: object_id });
            }
        };

        $scope.chart1 = {
            gui: {
                contextMenu: {
                    button: {
                        visible: 0,
                    },
                },
            },
            backgroundColor: 'transparent',
            globals: {
                shadow: false,
                fontFamily: 'Poppins',
            },
            type: 'area',
            legend: {
                layout: 'x4',
                backgroundColor: 'transparent',
                borderColor: 'transparent',
                marker: {
                    borderRadius: '50px',
                    borderColor: 'transparent',
                },
                item: {
                    fontColor: '#464e5f',
                },
            },
            scaleX: {
                maxItems: 8,
                transform: {
                    type: 'date',
                },
                zooming: true,
                values: [
                    1442905200000,
                    1442908800000,
                    1442912400000,
                    1442916000000,
                    1442919600000,
                    1442923200000,
                    1442926800000,
                    1442930400000,
                    1442934000000,
                    1442937600000,
                    1442941200000,
                    1442944800000,
                    1442948400000,
                ],
                lineColor: '#464e5f ',
                lineWidth: '1px',
                tick: {
                    lineColor: '#464e5f ',
                    lineWidth: '1px',
                },
                item: {
                    fontColor: '#464e5f ',
                },
                guide: {
                    visible: false,
                },
            },
            scaleY: {
                lineColor: '#464e5f ',
                lineWidth: '1px',
                tick: {
                    lineColor: '#464e5f ',
                    lineWidth: '1px',
                },
                guide: {
                    lineStyle: 'solid',
                    lineColor: '#626262',
                },
                item: {
                    fontColor: '#464e5f ',
                },
            },
            tooltip: {
                visible: false,
            },
            crosshairX: {
                scaleLabel: {
                    backgroundColor: '#fff',
                    fontColor: 'black',
                },
                plotLabel: {
                    backgroundColor: '#464e5f',
                    fontColor: '#FFF',
                    _text: 'Number of hits : %v',
                },
            },
            plot: {
                lineWidth: '2px',
                aspect: 'spline',
                marker: {
                    visible: false,
                },
            },
            series: [
                {
                    text: 'All Sites',
                    values: [
                        2596,
                        2626,
                        4480,
                        6394,
                        7488,
                        14510,
                        7012,
                        10389,
                        20281,
                        25597,
                        23309,
                        22385,
                        25097,
                        20813,
                        20510,
                    ],
                    backgroundColor1: '#77d9f8',
                    backgroundColor2: '#272822',
                    lineColor: '#40beeb',
                },
                {
                    text: 'Site 1',
                    values: [
                        479,
                        199,
                        583,
                        1624,
                        2772,
                        7899,
                        3467,
                        3227,
                        12885,
                        17873,
                        14420,
                        12569,
                        17721,
                        11569,
                        7362,
                    ],
                    backgroundColor1: '#4AD8CC',
                    backgroundColor2: '#272822',
                    lineColor: '#4AD8CC',
                },
                {
                    text: 'Site 2',
                    values: [989, 1364, 2161, 2644, 1754, 2015, 818, 77, 1260, 3912, 1671, 1836, 2589, 1706, 1161],
                    backgroundColor1: '#1D8CD9',
                    backgroundColor2: '#1D8CD9',
                    lineColor: '#1D8CD9',
                },
                {
                    text: 'Site 3',
                    values: [408, 343, 410, 840, 1614, 3274, 2092, 914, 5709, 6317, 6633, 6720, 6504, 6821, 4565],
                    backgroundColor1: '#D8CD98',
                    backgroundColor2: '#272822',
                    lineColor: '#D8CD98',
                },
            ],
        };

        $scope.chart2 = {
            globals: {
                shadow: false,
                fontFamily: 'Poppins',
            },
            title: {
                textAlign: 'center',
                text: 'Chart 2',
            },
            type: 'line',
            series: [{ values: [54, 23, 34, 23, 43] }, { values: [10, 15, 16, 20, 40] }],
        };

        $scope.chart3 = {
            type: 'pie',
            title: {
                textAlign: 'center',
                text: 'Chart 3',
            },
            globals: {
                shadow: false,
                fontFamily: 'Poppins',
            },
            plot: {
                slice: 50, //to make a donut
            },
            series: [
                {
                    values: [3],
                    text: 'Total Commits',
                },
                {
                    values: [4],
                    text: 'Issues Solved',
                },
                {
                    values: [8],
                    text: 'Issues Submitted',
                },
                {
                    values: [7],
                    text: 'Number of Clones',
                },
            ],
        };

        $scope.chart4 = {
            globals: {
                shadow: false,
                fontFamily: 'Poppins',
            },
            type: 'bar',
            title: {
                backgroundColor: 'transparent',
                fontColor: 'black',
                text: 'Chart 3',
            },
            series: [
                {
                    values: [1, 2, 3, 4],
                    backgroundColor: '#4DC0CF',
                },
            ],
        };
    });
});
