require.config({
    baseUrl: '/statics/',
    urlArgs: 'bust=' + new Date().getTime(),
    waitSeconds: 200,
    paths: {
        jquery: 'libs/jquery/jquery.min',
        popper: 'libs/popper/popper.min',
        moment: 'libs/moment/moment',
        fullcalendar: 'libs/fullcalendar/fullcalendar.min',
        bootstrap: 'libs/bootstrap/js/bootstrap.bundle.min',

        angular: 'libs/angular/angular.min',
        ngIdle: 'libs/angular/angular-idle',
        ngAnimate: 'libs/angular/angular-animate.min',
        ngSanitize: 'libs/angular/angular-sanitize.min',
        ngRoute: 'libs/angular/angular-ui-router',
        ngBreadcrumb: 'libs/ngBreadcrumb/angular-breadcrumb.min',
        ngLoadingbar: 'libs/angular/angular-loading-bar.min',
        ocLazyLoad: 'libs/ocLazyLoad/ocLazyLoad.require.min',

        app: 'scripts/angular-scripts/app',
        routes: 'scripts/angular-scripts/routes',
        directives: 'scripts/angular-scripts/directives',
        factories: 'scripts/angular-scripts/factories',
        services: 'scripts/angular-scripts/services',
        filters: 'scripts/angular-scripts/filters',
        animations: 'scripts/angular-scripts/animations',
        ngTouch: 'libs/angular/angular-touch.min',
        ngBootstrap: 'libs/angular/angular-ui-bootstrap-tpls.min',

        ngTags: 'libs/ngTags/ng-tags-input.min',
        zingchart: 'libs/charts/zingchart.min',
        ngCharts: 'libs/charts/zingchart-angular',
        ngToastr: 'libs/toastr/dist/js/angular-toastr.tpls.min',
        ngTable: 'libs/ngTable/ng-table',
        sweetalert: 'libs/sweetalert/sweetalert.min',
        ngSweetalert: 'libs/sweetalert/SweetAlert',
        ngBlock: 'libs/ngBlock/angular-block-ui.min',
        ngMoment: 'libs/ngMoment/ng-moment',

        datepicker: 'libs/bootstrap-datepicker/bootstrap-datepicker.min',
        ngDatepicker: 'libs/ngDatepicker/ng-datepicker',
        // 'ngDatepicker': 'libs/ui-datepicker/datetime-picker.min',
    },
    shim: {
        angular: {
            exports: 'angular',
            deps: ['jquery'],
        },
        ngAnimate: {
            deps: ['angular'],
        },
        ngSanitize: {
            deps: ['angular'],
        },
        ngRoute: {
            deps: ['angular'],
        },
        ngBreadcrumb: {
            deps: ['angular'],
        },
        ngLoadingbar: {
            deps: ['angular'],
        },
        ocLazyLoad: {
            deps: ['angular'],
        },
        ngToastr: {
            deps: ['angular'],
        },
        ngTable: {
            deps: ['angular'],
        },
        ngBlock: {
            deps: ['angular'],
        },
        ngTags: {
            deps: ['angular'],
        },
        ngSweetalert: {
            deps: ['angular', 'sweetalert'],
        },
        ngTouch: {
            deps: ['angular'],
        },
        ngCharts: {
            deps: ['angular', 'zingchart'],
        },
        ngBootstrap: {
            deps: ['angular', 'ngAnimate', 'ngTouch'],
        },
        ngIdle: {
            deps: ['angular'],
        },
        ngMoment: {
            deps: ['angular', 'moment'],
        },
        ngDatepicker: {
            deps: ['angular', 'moment', 'ngMoment', 'datepicker'],
        },
        app: {
            deps: [
                'jquery',
                'angular',
                'ngAnimate',
                'ngSanitize',
                'ngRoute',
                'ngBreadcrumb',
                'ngLoadingbar',
                'ocLazyLoad',
                'ngToastr',
                'ngTable',
                'ngSweetalert',
                'ngBlock',
                'ngTags',
                'ngTouch',
                'ngBootstrap',
                'ngIdle',
                'ngCharts',
                'ngMoment',
                'ngDatepicker',
            ],
        },
        routes: {
            deps: ['app'],
        },
        directives: {
            deps: ['app'],
        },
        factories: {
            deps: ['app'],
        },
        factories: {
            deps: ['app'],
        },
        services: {
            deps: ['app'],
        },
        filters: {
            deps: ['app'],
        },
        animations: {
            deps: ['app'],
        },
    },
});

require(['jquery', 'popper', 'moment', 'fullcalendar', 'bootstrap', 'datepicker'], function () {});

require(['app', 'routes', 'directives', 'factories', 'services', 'filters', 'animations'], function () {
    angular.bootstrap(document, ['app']);
});
