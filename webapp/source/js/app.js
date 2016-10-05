'use strict';

var app = angular.module(
    'app',
    ['ui.router', 'ngCookies', 'ngSanitize']
);

app.config(['$httpProvider', function($httpProvider) {
    var hostname_arr = location.hostname.split('.');
}]);

app.run(['$cookies', '$rootScope', '$http', '$window', '$state', function($cookies, $scope, $http, $window, $state) {
    $http.defaults.headers.common['Cache-Control'] = 'max-age=0';
    var $wind = angular.element($window);

    $http.defaults.xsrfCookieName = '_xsrf';
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.headers.delete = { 'Content-Type' : 'application/json' };

    $scope.$state = $state;

}]);

