app.config(['$stateProvider', '$urlRouterProvider', '$urlMatcherFactoryProvider', function($stateProvider, $urlRouterProvider, $urlMatcherFactoryProvider) {
    // allow trailing slashes
    $urlMatcherFactoryProvider.strictMode(false);

    $stateProvider
        // Home route
        .state('index', {
            url: '',
            templateUrl: 'index.html',
            controller: 'MainCtrl',
        })
    ;
    // default route preventing possibility of infinite digest loop
    // You can read more about why this is preferable to just $urlRouterProvider.otherwise('/') here
    // http://stackoverflow.com/a/31269197
    $urlRouterProvider.otherwise(function($injector) {
        var $state = $injector.get('$state');
        $state.go('home');
    });
}]);
