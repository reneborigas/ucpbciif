require.config({
    baseUrl: '/statics/',
    urlArgs: 'bust=' + new Date().getTime(),
    waitSeconds: 200,
    paths: {
        jquery: 'libs/jquery/jquery.min',
        popper: 'libs/popper/popper.min',
        bootstrap: 'libs/bootstrap/js/bootstrap.bundle.min',

        angular: 'libs/angular/angular.min',
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

        // 'ngDatepicker': 'libs/ui-datepicker/datetime-picker.min',
        // 'ngTouch' : 'libs/angular/angular-touch.min',
        // 'ngBootstrap' : 'libs/angular/angular-ui-bootstrap-tpls.min',
        ngToastr: 'libs/toastr/dist/js/angular-toastr.tpls.min',
        ngTable: 'libs/ngTable/ng-table',
        // 'index': 'scripts/angular-scripts/index',
        sweetalert: 'libs/sweetalert/sweetalert.min',
        ngSweetalert: 'libs/sweetalert/SweetAlert',
        ngBlock: 'libs/ngBlock/angular-block-ui.min',
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
        ngSweetalert: {
            deps: ['angular', 'sweetalert'],
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
    },
});

require(['jquery', 'popper', 'bootstrap'], function () {});

require(['app', 'routes', 'directives', 'factories', 'services', 'filters'], function () {
    angular.bootstrap(document, ['app']);
});
