socialModule.service('foroService', ['$q', '$http', function($q, $http) {

    this.VComentariosPagina = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'foro/VComentariosPagina',
          method: 'GET',
          params: args
        });
    //    var res = {};
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

    this.VForo = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'foro/VForo',
          method: 'GET',
          params: args
        });
    //    var res = {};
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

    this.VForos = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'foro/VForos',
          method: 'GET',
          params: args
        });
    //    var res = {};
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

    this.VPublicacion = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'foro/VPublicacion',
          method: 'GET',
          params: args
        });
    //    var res = {};
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };
    
    this.AgregForo = function(fForo) {
        return  $http({
          url: "foro/AgregForo",
          data: fForo,
          method: 'POST'
        });
    };
    
    this.AgregHilo = function(fHilo) {
        return  $http({
          url: "foro/AgregHilo",
          data: fHilo,
          method: 'POST'
        });
    };

}]);