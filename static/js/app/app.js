// Creación del módulo de la aplicación
var socialModule = angular.module('social', ['ngRoute', 'ngAnimate', 'ngTable', 'textAngular', 'ngDialog', 'ngSanitize', 'flash']);
socialModule.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
        .when('/', {
                controller: 'VInicioController',
                templateUrl: 'app/ident/VInicio.html'
            });
}]);
socialModule.controller('socialController_',  ['$scope', '$http', '$location', "chatService",'ngTableParams',
function($scope, $http, $location, chatService, ngTableParams) {
    $scope.title = "Social";
    $scope.verContactos = function(idUsuario) {
        document.getElementById('invisible').style.display = 'table';
        chatService.VContactos({"idUsuario":idUsuario}).then(function (object) {
            $scope.res = object.data;
            for (var key in object.data) {
                $scope[key] = object.data[key];
            }

                  var VChat1Data = $scope.res.data1;
                  if(typeof VChat1Data === 'undefined') VChat1Data=[];
                  $scope.tableParams1 = new ngTableParams({
                      page: 1,            // show first page
                      count: 10           // count per page
                  }, {
                      total: VChat1Data.length, // length of data
                      getData: function($defer, params) {
                          $defer.resolve(VChat1Data.slice((params.page() - 1) * params.count(), params.page() * params.count()));
                      }
                  });
    });};
    $scope.ocultarContactos = function () {
        document.getElementById('invisible').style.display = 'none';
    };
    $scope.VAdminContactos = function (idUsuario) {
        $location.path('/VAdminContactos/' + idUsuario);
    };
    $scope.VMiPagina = function (idUsuario) {
        $location.path('/VMiPagina/' + idUsuario);
    };
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

socialModule.service('navegador', 
    ['$location', 'identService', 'flash', '$route',
    function($location, identService, flash, $route) {

    this.agregarBotones = function (scope) {
        scope.VInicio = function() {
            $location.path('/');
        };
        scope.VPrincipal = function() {
          $location.path('/VPrincipal');
        };
        scope.VRegistro = function() {
          $location.path('/VRegistro');
        };
        scope.VForos = function(){
          $location.path('/VForos');
        };
        scope.VLogin = function() {
          $location.path('/VLogin');
        };
        scope.VContactos = function(idUsuario) {
          $location.path('/VContactos/'+idUsuario);
        };
        scope.VMiPagina = function(idUsuario) {
          $location.path('/VMiPagina/'+idUsuario);
        };
        scope.ASalir = function(id) {
            identService.ASalir({'idUsuario': id}).then( function (object){
                var msg = object.data["msg"];
                if (msg) flash(msg);
                $location.path('/');
                $route.reload();
            });
        };
    }
}]);
