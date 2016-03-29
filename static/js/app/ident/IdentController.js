socialModule.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/VLogin', {
                controller: 'VLoginController',
                templateUrl: 'app/ident/VLogin.html'
            }).when('/VPrincipal', {
                controller: 'VPrincipalController',
                templateUrl: 'app/ident/VPrincipal.html'
            }).when('/VPrincipal/:idPaginaSitio', {
                controller: 'VPrincipalController',
                templateUrl: 'app/ident/VPrincipal.html'
            }).when('/VRegistro', {
                controller: 'VRegistroController',
                templateUrl: 'app/ident/VRegistro.html'
            });
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
      $scope.VRegistro1 = function() {
        $location.path('/VRegistro');
      };

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
   ['$scope', '$location', '$route', '$timeout', 'flash', 'chatService', 'identService', 'paginasService', 'foroService', 'ngDialog',
    function ($scope, $location, $route, $timeout, flash, chatService, identService, paginasService, foroService, ngDialog) {
      $scope.msg = '';
      $scope.pag = {}; 
      $scope.principal = ''
      $scope.paginas = [];
      identService.VPrincipal().then(function (object) {
        $scope.res = object.data;
        $scope.paginas = object.data['pag'];
        $scope.paginas = object.data['pags'];
        $scope.principal = object.data['principal'];
        for (var key in object.data) {
            $scope[key] = object.data[key];
        }
        if ($scope.logout) {
            $location.path('/');
        }


      });
      $scope.VLogin0 = function() {
        $location.path('/VLogin');
      };
      $scope.APagina1 = function(idPagina) {
         
        paginasService.APagina({"idPagina":((typeof idPagina === 'object')?JSON.stringify(idPagina):idPagina)}).then(function (object) {
          var msg = object.data["msg"];
          if (msg) flash(msg);
          var label = object.data["label"];
          $location.path(label);
          $route.reload();
        });};
      $scope.VContactos2 = function(idUsuario) {
        $location.path('/VContactos/'+idUsuario);
      };
      
      $scope.VForos = function(){
        foroService.VForos().then(function (object){
          $location.path('/VForos');
        });
      };
      $scope.VPrincipal4 = function(idPaginaSitio){
        
          identService.APaginaSitio({"idPaginaSitio":((typeof idPaginaSitio === 'object')?JSON.stringify(idPaginaSitio):idPaginaSitio)}).then(function (object) {
              var msg = object.data["msg"];
              if (msg) flash(msg);
              var label = object.data["label"];
              $location.path(label);
              $route.reload();
          });
      
      };
$scope.VComentariosPagina5 = function (idPaginaSitio) {
        
        $location.path("/VComentariosPagina/"+idPaginaSitio);
        ngDialog.openConfirm({ template: 'temp' ,controller:'VComentariosPaginaController'});
        
    };   

    }]);
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
      $scope.VLogin1 = function() {
        $location.path('/VLogin');
      };

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
