define(function() {
	'use strict';
	
	var app = angular.module('app', [
		'ui.router',
		'oc.lazyLoad',
		'ncy-angular-breadcrumb',
		'angular-loading-bar',
		'toastr',
		'ngTable',
	])
	
	app.config(['cfpLoadingBarProvider', function (cfpLoadingBarProvider) {
		cfpLoadingBarProvider.includeSpinner = false;
		cfpLoadingBarProvider.latencyThreshold = 1;
	}])

	app.run(['$rootScope', '$state', '$stateParams', '$http', function ($rootScope, $state, $stateParams, $http) {
		$http.defaults.xsrfHeaderName = 'X-CSRFToken';
		$http.defaults.xsrfCookieName = 'csrftoken';

		$rootScope.$on('$stateChangeSuccess', function () {
			document.body.scrollTop = document.documentElement.scrollTop = 0;			
		});		
		$rootScope.$state = $state;
		return $rootScope.$stateParams = $stateParams;
	}]);

});
	