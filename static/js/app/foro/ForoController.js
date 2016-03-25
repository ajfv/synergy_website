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
            });
}]);

socialModule.controller('VComentariosPaginaController', 
   ['$scope', '$location', '$route', '$timeout', 'flash', '$routeParams', 'foroService','identService',
    function ($scope, $location, $route, $timeout, flash, $routeParams, foroService, identService) {
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
