socialModule.service('identService', ['$q', '$http', function($q, $http) {

    this.AIdentificar = function(fLogin) {
        return  $http({
          url: "ident/AIdentificar",
          data: fLogin,
          method: 'POST',
        });
    //    var labels = ["/VPrincipal", "/VLogin", ];
    //    var res = labels[0];
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

    this.ARegistrar = function(fUsuario) {
        return  $http({
          url: "ident/ARegistrar",
          data: fUsuario,
          method: 'POST',
        });
    //    var labels = ["/VLogin", "/VRegistro", ];
    //    var res = labels[0];
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

    this.VLogin = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'ident/VLogin',
          method: 'GET',
          params: args
        });
    //    var res = {};
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

    this.VPrincipal = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'ident/VPrincipal',
          method: 'GET',
          params: args
        });
    //    var res = {};
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

    this.VRegistro = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'ident/VRegistro',
          method: 'GET',
          params: args
        });
    //    var res = {};
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

}]);