socialModule.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/VLogin', {
                controller: 'VLoginController',
                templateUrl: 'app/ident/VLogin.html'
            }).when('/VInicio', {
                controller: 'VInicioController',
                templateUrl: 'app/ident/VInicio.html'
            }).when('/VPrincipal', {
                controller: 'VPrincipalController',
                templateUrl: 'app/ident/VPrincipal.html'
            }).when('/VRegistro', {
                controller: 'VRegistroController',
                templateUrl: 'app/ident/VRegistro.html'
            });
}]);

socialModule.controller('VInicioController', 
   ['$scope', '$location', '$route', '$timeout', 'flash', 'chatService', 'identService', 'paginasService',
    function ($scope, $location, $route, $timeout, flash, chatService, identService, paginasService) {

      $scope.VInicio = function() {
        $location.path('/VInicio');
      };

      $scope.VLogin = function() {
        $location.path('/VLogin');
      };

      $scope.VRegistro = function() {
        $location.path('/VRegistro');
      };

}]);

socialModule.controller('VLoginController', 
   ['$scope', '$location', '$route', '$timeout', 'flash', 'chatService', 'identService', 'paginasService',
    function ($scope, $location, $route, $timeout, flash, chatService, identService, paginasService) {
      $scope.msg = '';
      $scope.fLogin = {};

      identService.VLogin().then(function (object) {
        $scope.res = object.data;
        for (var key in object.data) {
            $scope[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }

      });

      $scope.VInicio0 = function() {
        $location.path('/VInicio');
      };

      $scope.VRegistro0 = function() {
        $location.path('/VRegistro');
      };

      $scope.reloadRoute = function() {
         $route.reload();
      }

      $scope.fLoginSubmitted = false;
      $scope.AIdentificar0 = function(isValid) {
        $scope.fLoginSubmitted = true;
        if (isValid) {
          
          identService.AIdentificar($scope.fLogin).then(function (object) {
              var msg = object.data["msg"];
              if (msg) flash(msg);
              var label = object.data["label"];
              $location.path(label);
              $route.reload();
          });
        }
      };

    }]);

socialModule.controller('VPrincipalController', 
   ['$scope', '$location', '$route', '$timeout', 'flash', 'ngDialog', 'chatService', 'identService', 'paginasService', 'foroService',
    function ($scope, $location, $route, $timeout, flash, ngDialog, chatService, identService, paginasService, foroService) {
      $scope.msg = '';
      identService.VPrincipal().then(function (object) {
        $scope.res = object.data;
        for (var key in object.data) {
            $scope[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }


      });
      $scope.VLogin1 = function() {
        $location.path('/VLogin');
      };
      $scope.VInicio1 = function() {
        $location.path('/VInicio');
      };
      $scope.APagina1 = function(idPagina) {
         
        paginasService.APagina({"idPagina":((typeof idPagina === 'object')?JSON.stringify(idPagina):idPagina)}).then(function (object) {
          var msg = object.data["msg"];
          if (msg) flash(msg);
          var label = object.data["label"];
          $location.path(label);
          $route.reload();
        });};

      $scope.VContactos2 = function(idUsuario) { // cambiar a VContactos1
        $location.path('/VContactos/'+idUsuario);
      };

      $scope.VMiPagina0 = function(idUsuario) {
        $location.path('/VMiPagina/'+idUsuario);
      };
      
      $scope.VForos = function(){ // Cambiar a VForos1
        foroService.VForos().then(function (object){
          $location.path('/VForos');
        });
      };

$scope.__ayuda = function() {
  ngDialog.open({ template: 'ayuda_VPrincipal.html',
        showClose: true, closeByDocument: true, closeByEscape: true});
}
    }]);

// Usar el 2 para identificar los "href" ($scope.VLogin2)
socialModule.controller('VRegistroController', 
   ['$scope', '$location', '$route', '$timeout', 'flash', 'chatService', 'identService', 'paginasService',
    function ($scope, $location, $route, $timeout, flash, chatService, identService, paginasService) {
      $scope.msg = '';
      $scope.fUsuario = {};

      identService.VRegistro().then(function (object) {
        $scope.res = object.data;
        for (var key in object.data) {
            $scope[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }


      });

      $scope.VInicio2 = function() {
        $location.path('/VInicio');
      };

      $scope.VLogin2 = function() {
        $location.path('/VLogin');
      };

      $scope.reloadRoute = function() {
         $route.reload();
      }

      $scope.fUsuarioSubmitted = false;
      $scope.ARegistrar0 = function(isValid) {
        $scope.fUsuarioSubmitted = true;
        if (isValid) {

          identService.ARegistrar($scope.fUsuario).then(function (object) {
              var msg = object.data["msg"];
              if (msg) flash(msg);
              var label = object.data["label"];
              $location.path(label);
              $route.reload();
          });
        }
      };

    }]);
