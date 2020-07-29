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
        var calendarElement = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarElement, {
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
            events: [
                {
                    title: 'All Day Event',
                    start: '2020-06-01',
                },
                {
                    title: 'Long Event',
                    start: '2020-06-07',
                    end: '2020-06-10',
                },
                {
                    groupId: 999,
                    title: 'Repeating Event',
                    start: '2020-06-09T16:00:00',
                },
                {
                    groupId: 999,
                    title: 'Repeating Event',
                    start: '2020-06-16T16:00:00',
                },
                {
                    title: 'Conference',
                    start: '2020-06-11',
                    end: '2020-06-13',
                    className: 'fc-event-solid-danger fc-event-light',
                    description: 'Lorem ipsum dolor sit ctetur adipi scing',
                },
                {
                    title: 'Meeting',
                    start: '2020-06-12T10:30:00',
                    end: '2020-06-12T12:30:00',
                },
                {
                    title: 'Lunch',
                    start: '2020-06-12T12:00:00',
                },
                {
                    title: 'Meeting',
                    start: '2020-06-12T14:30:00',
                },
                {
                    title: 'Happy Hour',
                    start: '2020-06-12T17:30:00',
                },
                {
                    title: 'Dinner',
                    start: '2020-06-12T20:00:00',
                },
                {
                    title: 'Birthday Party',
                    start: '2020-06-13T07:00:00',
                },
                {
                    title: 'Click for Google',
                    url: 'http://google.com/',
                    start: '2020-06-28',
                },
            ],
        });

        calendar.render();
    });
});
