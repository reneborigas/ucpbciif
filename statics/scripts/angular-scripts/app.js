define(function() {
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

	app.run(['$rootScope', '$state', '$stateParams', '$http', 'appLoginService', function ($rootScope, $state, $stateParams, $http, appLoginService) {
		$http.defaults.xsrfHeaderName = 'X-CSRFToken';
		$http.defaults.xsrfCookieName = 'csrftoken';

		// appLoginService.redirectIfNotLoggedIn();

		// $scope.showHeader = false;
		// $scope.showHeader = Login.isLoggedIn();

		$rootScope.$on('$stateChangeSuccess', function () {
			document.body.scrollTop = document.documentElement.scrollTop = 0;			
		});		
		$rootScope.$state = $state;
		return $rootScope.$stateParams = $stateParams;
	}]);

});
	