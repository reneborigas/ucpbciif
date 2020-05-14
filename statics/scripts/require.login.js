require.config({
	baseUrl: '/statics/',
	waitSeconds: 0,
	urlArgs: 'bust=' + new Date().getTime(),
	paths: {
		'app-options': 'assets/js/app.options',
		'plugins-bundle': 'assets/plugins/global/plugins.bundle',
		'scripts-bundle': 'assets/js/scripts.bundle',
		'login-script': 'assets/js/pages/custom/login/login-general',
		'popper': 'libs/popper/popper',
		'angular': 'libs/angular/angular.min',
		'ui-route': 'libs/angular/angular-ui-router',
		'toastr': 'libs/toastr/dist/js/angular-toastr.tpls.min',
		'auth': 'scripts/angular-scripts/auth',
		'login': 'scripts/angular-scripts/login'
	},
	shim: {
		'popper': {
			exports: "Popper"
		},
		'scripts-bundle': {
			deps: ['popper','plugins-bundle']
		},
		'login-script': {
			deps: ['plugins-bundle']
		},
		'auth': {
			deps: ['angular']
		},
		'toastr': {
			deps: ['angular']
		},
		'login': {
			deps: ['angular', 'ui-route', 'auth', 'toastr']
		}
	},
	map: {
		"*": {
			"popper.js": 'libs/popper/popper',
		}
	}
});

require(['app-options', 'plugins-bundle', 'scripts-bundle', 'login-script','popper'], function () {
 });

require(['login'], function () {
	angular.bootstrap(document, ['login']);
});
