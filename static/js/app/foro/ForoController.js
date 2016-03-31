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
            }).when('/VPublicacion/:idHilo', {
                controller: 'VPublicacionController',
                templateUrl: 'app/foro/VPublicacion.html'
            }).when('/VHilos/:idHilo', {
                controller: 'VHilosController',
                templateUrl: 'app/foro/VHilos.html'
            });
}]);

socialModule.controller('VForoController',
   ['$scope', '$location', '$route', '$timeout', 'flash', '$routeParams', 'foroService', 'ngTableParams',
    function ($scope, $location, $route, $timeout, flash, $routeParams, foroService, ngTableParams) {
      $scope.msg = '';
      foroService.VForo({"idForo":$routeParams.idForo}).then(function (object) {
        $scope.res = object.data;
        for (var key in object.data) {
            $scope[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }

        $scope.VForos1 = function(isValid){
          $location.path('/VForos');
        };

        $scope.idForo = $routeParams.idForo;

        var VHilo2Data = $scope.res.data;
        if(typeof VHilo2Data === 'undefined') VHilo2Data=[];
        $scope.tableParams1 = new ngTableParams({
                  page: 1,            // show first page
                  count: 10           // count per page
              }, {
                  total: VHilo2Data.length, // length of data
                  getData: function($defer, params) {
                      $defer.resolve(VHilo2Data.slice((params.page() - 1) * params.count(), params.page() * params.count()));
                  }
        });

        $scope.__ayuda = function() {
            ngDialog.open({ template: 'ayuda_VForo.html',
            showClose: true, closeByDocument: true, closeByEscape: true});
        };

        $scope.fHiloSubmitted = false;
        $scope.AgregHilo3 = function(isValid) {
            $scope.fHiloSubmitted = true;
            if (isValid) {

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
   ['$scope', '$location', '$route', '$timeout', 'flash', 'foroService', 'ngTableParams',
    function ($scope, $location, $route, $timeout, flash, foroService, ngTableParams) {
      $scope.msg = '';
      foroService.VForos().then(function (object) {
        $scope.res = object.data;
        for (var key in object.data) {
            $scope[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }

        var VForo2Data = $scope.res.data;
        if(typeof VForo2Data === 'undefined') VForo2Data=[];
        $scope.tableParams1 = new ngTableParams({
                  page: 1,            // show first page
                  count: 10           // count per page
              }, {
                  total: VForo2Data.length, // length of data
                  getData: function($defer, params) {
                      $defer.resolve(VForo2Data.slice((params.page() - 1) * params.count(), params.page() * params.count()));
                  }
        });

      $scope.VPrincipal0 = function() {
        $location.path('/VPrincipal');
      };
      $scope.__ayuda = function() {
        ngDialog.open({ template: 'ayuda_VForos.html',
        showClose: true, closeByDocument: true, closeByEscape: true});
      };

      $scope.fForoSubmitted = false;
      $scope.AgregForo3 = function(isValid) {
        $scope.fForoSubmitted = true;
        if (isValid) {

          foroService.AgregForo($scope.fForo).then(function (object) {
              var msg = object.data["msg"];
              if (msg) flash(msg);
              var label = object.data["label"];
              $location.path(label);
              $route.reload();
          });
        }
      };

      $scope.VForo0 = function(idForo){
          $location.path('/VForo/'+idForo);
      };


      $scope.AElimForo1 = function(idForo) {
          //var tableFields = [["idForo","id"],["titulo","Titulo"],["fecha","Fipo"]];
          var arg = {};
          //arg[tableFields[0][1]] = ((typeof id === 'object')?JSON.stringify(id):id);
          arg['idForo'] = ((typeof id === 'object')?JSON.stringify(idForo):idForo);
          foroService.AElimForo(arg).then(function (object) {
              var msg = object.data["msg"];
              if (msg) flash(msg);
              var label = object.data["label"];
              $location.path(label);
              $route.reload();
          });
      };

      });
    }]);
    
socialModule.controller('VHilosController',
   ['$scope', '$location', '$route', '$timeout', 'flash', 'ngDialog', '$routeParams', 'foroService',
    function ($scope, $location, $route, $timeout, flash, ngDialog, $routeParams, foroService) {
      $scope.msg = '';
      foroService.VHilos({"idHilo":$routeParams.idHilo}).then(function (object) {
        $scope.res = object.data;
        for (var key in object.data) {
            $scope[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }

        $scope.VForo1 = function(){
          $location.path('/VForo/' + $scope.foroPadre);
        };
      
        $scope.AElimPublicacion1 = function(idPublicacion) {
          //var tableFields = [["idForo","id"],["titulo","Titulo"],["fecha","Fipo"]];
          var arg = {};
          //arg[tableFields[0][1]] = ((typeof id === 'object')?JSON.stringify(id):id);
          arg['idPublicacion'] = ((typeof id === 'object')?JSON.stringify(idPublicacion):idPublicacion);
          foroService.AElimPublicacion(arg).then(function (object) {
              var msg = object.data["msg"];
              if (msg) flash(msg);
              $route.reload();
          });
      };
        
      
        $scope.fpublicacion = { titulo: $scope.res['tituloNuevaPublicacion']};
        $scope.fpublicacionFormSubmitted = false;
        $scope.error = false;
        var agregarPublicacion = function(scope, isValid, idPublicacion) {
          if (scope.fpublicacionFormSubmitted)
            return;
          scope.fpublicacionFormSubmitted = true;
          if (isValid) {
            args = {}
            args['id'] = idPublicacion;
            args['titulo'] = scope.fpublicacion.titulo;
            args['contenido'] = scope.fpublicacion.texto;
            foroService.AgregPublicacion(args).then(function (object) {
                var msg = object.data["msg"];
                if (msg) flash(msg);
                ngDialog.closeAll();
                $route.reload();
            });
        } else{
            scope.error = true;
            scope.fpublicacionFormSubmitted = false;
        }
        };
        
        $scope.AgregPublicacion3 = function(isValid, id) {
            agregarPublicacion($scope, isValid, id);
        };
        
        $scope.responderPublicacion = function(publicacion) {
            var nuevoScope = $scope.$new(true);
            nuevoScope.publicacion = publicacion;
            nuevoScope.fpublicacion = {titulo: "RE: " + publicacion.titulo};
            nuevoScope.fpublicacionFormSubmitted = false;
            nuevoScope.error = false;
            nuevoScope.AgregPublicacion3 = function(isValid, id) {
                agregarPublicacion(nuevoScope, isValid, id);
            };
            ngDialog.open({ template: 'responder_Publicacion.html',
            showClose: true, closeByDocument: true, closeByEscape: true,
            scope: nuevoScope
            });
        };
        
        $scope.colapsar = function (id) {
            var element = document.getElementById('publicacion' + id);
            var boton = document.getElementById('boton' + id);
            if (element.style.display == 'none') {
                element.style.display = 'initial';
                boton.innerHTML = "[-]";
            } else {
                element.style.display = 'none';
                boton.innerHTML = "[+]";
            }
        };

      });
    }]);
