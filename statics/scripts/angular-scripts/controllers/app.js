define(function() {
	'use strict';

	var app =  angular.module('app');

	app.controller('NavBarController', function NavBarController($scope, appFactory, appLoginService) {

		appFactory.getCurrentUserInfo().then(function(data){
			$scope.user = data;
		});
		$scope.logout = appLoginService.logout;
		$scope.showHeader = false;
		$scope.showHeader = appLoginService.isLoggedIn();
	});

	app.controller('FooterController', function FooterController($scope) {
        $scope.date = new Date();
	});
	
});
