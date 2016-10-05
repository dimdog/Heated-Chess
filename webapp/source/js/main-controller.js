'use strict';

var app = angular.module('app');

app.controller('MainCtrl', ['$http', '$rootScope', '$scope', '$state', '$board',
    function($http, $rootScope, $scope, $state, $board) {
        $scope.board = $board;

}]);
