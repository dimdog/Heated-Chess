'use strict';
var app = angular.module('app');
app.service('$board', ['$http', '$rootScope', '$location', '$state', function($http, $rootScope, $location, $state) {

    var $board = {};
    $board.rows = [8, 7, 6, 5, 4, 3, 2, 1];
    $board.columns = ["A", "B", "C", "D", "E", "F", "G", "H"];

    // --------------
    // API ENDPOINTS
    // --------------

    // GET
    $board.init = function(callback) {
        $http.get("http://localhost/api").success(function(data) {
            $board.data = $.extend({}, data);
            console.log($board.data);
            if (callback) { callback(data); }
        });
    };
    $board.init()
    return $board;

}]);
