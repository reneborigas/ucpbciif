define(function () {
	'use strict';

	var app = angular.module('app', [
		'ui.router',
		'oc.lazyLoad',
		'ncy-angular-breadcrumb',
		'angular-loading-bar',
		'toastr',
		'ngTable',
		'oitozero.ngSweetAlert',
	])

	app.config(['cfpLoadingBarProvider', function (cfpLoadingBarProvider) {
		cfpLoadingBarProvider.includeSpinner = false;
		cfpLoadingBarProvider.latencyThreshold = 1;
	}])

	app.run(['$rootScope', '$state', '$stateParams', '$http', 'appLoginService', '$transitions', function ($rootScope, $state, $stateParams, $http, appLoginService,$transitions) {
		$http.defaults.xsrfHeaderName = 'X-CSRFToken';
		$http.defaults.xsrfCookieName = 'csrftoken';

		$transitions.onBefore({}, function(transition) {
			if (transition.to().name !== 'simple.login' && !appLoginService.isLoggedIn()) {
				return transition.router.stateService.target('simple.login');
			}
			if (transition.to().name == 'simple.login' && appLoginService.isLoggedIn()) {
				return transition.router.stateService.target('app.main');
			}
		})

		$rootScope.$state = $state;
		return $rootScope.$stateParams = $stateParams;

	}]);

});
