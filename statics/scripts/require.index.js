require.config({
	baseUrl: '/statics/',
	// urlArgs: 'bust=' + (new Date()).getTime(),
	paths: {
		// 'app-options': 'assets/js/app.options',
		// 'plugins-bundle': 'assets/plugins/global/plugins.bundle',
		// 'scripts-bundle': 'assets/js/scripts.bundle',
		'jquery' : 'libs/jquery/jquery.min',
		'angular': 'libs/angular/angular.min',
		'auth': 'scripts/angular-scripts/auth',
		'ui-route': 'libs/angular/angular-ui-router',
		'ngDatepicker': 'libs/ui-datepicker/datetime-picker.min',
		
		'ngAnimate' : 'libs/angular/angular-animate.min',
        'ngTouch' : 'libs/angular/angular-touch.min',
		'ngBootstrap' : 'libs/angular/angular-ui-bootstrap-tpls.min', 
		'ocLazyLoad': 'libs/ocLazyLoad/ocLazyLoad.require.min',
		'toastr': 'libs/toastr/dist/js/angular-toastr.tpls.min',
		'index': 'scripts/angular-scripts/index',
		'sweetalert': 'libs/sweetalert/sweetalert.min',
		'ngSweetalert': 'libs/sweetalert/SweetAlert',
		'ngTable': 'libs/ngTable/ng-table',
		'ngAnimate': 'libs/angular/angular-animate.min',
		'ngBlock': 'libs/ngBlock/angular-block-ui.min',
		'ngSanitize': 'libs/angular/angular-sanitize.min',
		'ngBreadcrumb': 'libs/ngBreadcrumb/angular-breadcrumb.min',
	},
	shim: {
		'angular': {
			exports: 'angular'
		},
		'toastr':{
            deps: ['angular']
        },
		'ngAnimate': {
			deps: [ 'angular' ]
		},
        'ngTouch':{
            deps: ['angular']
        },
		'ngBootstrap':{
            deps: ['angular','ngAnimate','ngTouch']
        },
		'ngDatepicker': {
			deps: [ 'ngBootstrap' ]
		},
		'ngBlock': {
			deps: [ 'angular' ]
		},
		'ngSanitize': {
			deps: [ 'angular' ]
		},
		'auth': {
			deps: [ 'angular' ]
		},
		'ocLazyLoad': {
			deps: [ 'angular' ]
		},
		'ngBreadcrumb': {
			deps: [ 'angular' ]
		},
		'toastr': {
			deps: [ 'angular' ]
		},
		'ngSweetalert': {
			deps: [ 'angular', 'sweetalert' ]
		},
		'ngTable': {
			deps: [ 'angular' ]
		},
		'index': {
			deps: [
				'jquery','angular','ui-route','auth','toastr','ocLazyLoad','ngSweetalert','ngTable','ngBreadcrumb','ngAnimate','ngBlock','ngSanitize','ngBootstrap','ngAnimate'
			]
		}
	},
});

// require(['app-options', 'plugins-bundle', 'scripts-bundle','popper'], function () {
// });

require([ 'index' ], function() {
	angular.bootstrap(document, [ 'lmsApp' ]);
});
