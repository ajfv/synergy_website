socialModule.service('paginasService', ['$q', '$http', function($q, $http) {

    this.AModificarPagina = function(fPagina) {
        return  $http({
          url: "paginas/AModificarPagina",
          data: fPagina,
          method: 'POST',
        });
    //    var labels = ["/VPagina", ];
    //    var res = labels[0];
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

    this.APagina = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'paginas/APagina',
          method: 'GET',
          params: args
        });
    //    var labels = ["/VPagina", "/VMiPagina", ];
    //    var res = labels[0];
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };
    this.VMiPagina = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'paginas/VMiPagina',
          method: 'GET',
          params: args
        });
    //    var res = {};
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

    this.VPagina = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'paginas/VPagina',
          method: 'GET',
          params: args
        });
    //    var res = {};
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

}]);