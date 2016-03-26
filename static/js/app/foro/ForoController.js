socialModule.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/VComentariosPagina/:idPaginaSitio', {
                controller: 'VComentariosPaginaController',
                templateUrl: 'app/foro/VComentariosPagina.html'
            }).when('/VForo/:idForo', {
                controller: 'VForoController',
                templateUrl: 'app/foro/VForo.html'
            }).when('/VForos', {
                controller: 'VForosController',
                templateUrl: 'app/foro/VForos.html'
            }).when('/VPublicacion/:idForo', {
                controller: 'VPublicacionController',
                templateUrl: 'app/foro/VPublicacion.html'
            }).when('/VHilos/:idHilo', {
                controller: 'VForoController',
                templateUrl: 'app/foro/VHilos.html'
            });
}]);

socialModule.controller('VComentariosPaginaController', 
   ['$scope', '$location', '$route', '$timeout', 'flash', '$routeParams', 'foroService',
    function ($scope, $location, $route, $timeout, flash, $routeParams, foroService) {
      $scope.msg = '';
      foroService.VComentariosPagina({"idPaginaSitio":$routeParams.idPaginaSitio}).then(function (object) {
        $scope.res = object.data;
        for (var key in object.data) {
            $scope[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }


      });
    }]);
socialModule.controller('VForoController', 
   ['$scope', '$location', '$route', '$timeout', 'flash', '$routeParams', 'foroService',
    function ($scope, $location, $route, $timeout, flash, $routeParams, foroService) {
      $scope.msg = '';
      foroService.VForo({"idForo":$routeParams.idForo}).then(function (object) {
        $scope.res = object.data;
        for (var key in object.data) {
            $scope[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }

                foroService.AgregHilo($scope.fHilo).then(function (object) {
                var msg = object.data["msg"];
                if (msg) flash(msg);
                var label = object.data["label"];
                $location.path(label);
                $route.reload();
          });
        }
      };
      
      $scope.AElimHilo1 = function(idHilo) {
          //var tableFields = [["idForo","id"],["titulo","Titulo"],["fecha","Fipo"]];
          var arg = {};
          //arg[tableFields[0][1]] = ((typeof id === 'object')?JSON.stringify(id):id);
          arg['idHilo'] = ((typeof id === 'object')?JSON.stringify(idHilo):idHilo);
          foroService.AElimHilo(arg).then(function (object) {
              var msg = object.data["msg"];
              if (msg) flash(msg);
              var label = object.data["label"];
              $location.path(label);
              $route.reload();
          });
      };
      
      $scope.VHilo0 = function(idHilo){
          $location.path('/VHilos/'+idHilo);
      };
      
     // $scope.VHilo0 = function(idHilo) {
     //   $location.path('/VForo');
     // };
        

      });
    }]);
socialModule.controller('VForosController', 
   ['$scope', '$location', '$route', '$timeout', 'flash', 'foroService',
    function ($scope, $location, $route, $timeout, flash, foroService) {
      $scope.msg = '';
      foroService.VForos().then(function (object) {
        $scope.res = object.data;
        for (var key in object.data) {
            $scope[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }


      });
    }]);
socialModule.controller('VPublicacionController', 
   ['$scope', '$location', '$route', '$timeout', 'flash', '$routeParams', 'foroService',
    function ($scope, $location, $route, $timeout, flash, $routeParams, foroService) {
      $scope.msg = '';
      foroService.VPublicacion({"idForo":$routeParams.idForo}).then(function (object) {
        $scope.res = object.data;
        for (var key in object.data) {
            $scope[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }


      });
    }]);
