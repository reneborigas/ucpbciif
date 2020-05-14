define(function() {
	'use strict';

	var lmsApp =  angular.module('app');

	lmsApp.controller('NavBarController', function NavBarController($scope, appFactory, appLoginService) {

		appFactory.getCurrentUserInfo().then(function(data){
			$scope.user = data;
		});
		$scope.logout = appLoginService.logout;
		$scope.showHeader = false;
		$scope.showHeader = appLoginService.isLoggedIn();
	});

	lmsApp.controller('FooterController', function FooterController($scope) {
        $scope.date = new Date();
	});
	
});
