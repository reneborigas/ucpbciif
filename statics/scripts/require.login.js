require.config({
	baseUrl: '/statics/',
	waitSeconds: 0,
	urlArgs: 'bust=' + new Date().getTime(),
	paths: {
		'jquery' : 'libs/jquery/jquery.min',
		'popper' : 'libs/popper/popper.min', 
		'bootstrap' : 'libs/bootstrap/js/bootstrap.bundle.min',
		'angular': 'libs/angular/angular.min',
		'ui-route': 'libs/angular/angular-ui-router',
		'toastr': 'libs/toastr/dist/js/angular-toastr.tpls.min',
		'ng-animate' : 'libs/angular/angular-animate.min',
		'auth': 'scripts/angular-scripts/auth',
		'login': 'scripts/angular-scripts/login'
	},
	shim: {
		'bootstrap' : {
            deps: ['popper','jquery']
        },
		'angular': {
			exports: 'angular',
		},
		'auth': {
			deps: ['angular']
		},
		'ng-animate': {
			deps: ['angular']
		},
		'toastr': {
			deps: ['angular',]
		},
		'ui-route': {
			deps: ['angular',]
		},
		'login': {
			deps: ['angular', 'ui-route', 'ng-animate','auth', 'toastr']
		}
	},
});

require([
    'jquery','popper','bootstrap'
    ],function(){    
});

require(['login'], function () {
	angular.bootstrap(document, ['login']);
});
