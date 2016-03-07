// Creación del módulo de la aplicación
var socialModule = angular.module('social', ['ngRoute', 'ngAnimate', 'ngTable', 'textAngular', 'ngDialog', 'ngSanitize', 'flash']);
socialModule.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
        .when('/', {
                controller: 'VLoginController',
                templateUrl: 'app/ident/VLogin.html'
            });
}]);
socialModule.controller('socialController_',  ['$scope', '$http', '$location',
function($scope) {
    $scope.title = "Social";
}]);
socialModule.directive('sameAs', [function () {
    return {
        restrict: 'A',
        scope:true,
        require: 'ngModel',
        link: function (scope, elem , attrs, control) {
            var checker = function () {
                //get the value of the this field
                var e1 = scope.$eval(attrs.ngModel); 
 
                //get the value of the other field
                var e2 = scope.$eval(attrs.sameAs);
                return e1 == e2;
            };
            scope.$watch(checker, function (n) {
 
                //set the form control to valid if both 
                //fields are the same, else invalid
                control.$setValidity("unique", n);
            });
        }
    };
}]);
