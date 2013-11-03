/* global angular */

var paySystem = angular.module('claims', []);

paySystem.config(function($interpolateProvider) {
	// allow django templates and angular to co-exist
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
});

paySystem.controller('ListCtrl', function ListCtrl($scope, $log){

	$scope.initialize = function(data) {
		$log.log('initialize', data);
		$scope.initData = data;
	};
});