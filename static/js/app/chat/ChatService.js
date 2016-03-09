socialModule.service('chatService', ['$q', '$http', function($q, $http) {

    this.AElimContacto = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'chat/AElimContacto',
          method: 'GET',
          params: args
        });
    //    var labels = ["/VAdminContactos", "/VAdminContactos", ];
    //    var res = labels[0];
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };
    this.AElimMiembro = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'chat/AElimMiembro',
          method: 'GET',
          params: args
        });
    //    var labels = ["/VGrupo", ];
    //    var res = labels[0];
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };
    this.AEscribir = function(fChat) {
        return  $http({
          url: "chat/AEscribir",
          data: fChat,
          method: 'POST',
        });
    //    var labels = ["/VChat", "/VChat", ];
    //    var res = labels[0];
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

    this.ASalirGrupo = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'chat/ASalirGrupo',
          method: 'GET',
          params: args
        });
    //    var labels = ["/VAdminContactos", "/VGrupo", ];
    //    var res = labels[0];
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };
    this.AgregContacto = function(fContacto) {
        return  $http({
          url: "chat/AgregContacto",
          data: fContacto,
          method: 'POST',
        });
    //    var labels = ["/VAdminContactos", "/VAdminContactos", ];
    //    var res = labels[0];
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

    this.AgregMiembro = function(fMiembro) {
        return  $http({
          url: "chat/AgregMiembro",
          data: fMiembro,
          method: 'POST',
        });
    //    var labels = ["/VGrupo", "/VGrupo", ];
    //    var res = labels[0];
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

    this.VAdminContactos = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'chat/VAdminContactos',
          method: 'GET',
          params: args
        });
    //    var res = {};
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

    this.VChat = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'chat/VChat',
          method: 'GET',
          params: args
        });
    //    var res = {};
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

    this.VContactos = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'chat/VContactos',
          method: 'GET',
          params: args
        });
    //    var res = {};
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

    this.VGrupo = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'chat/VGrupo',
          method: 'GET',
          params: args
        });
    //    var res = {};
    //    var deferred = $q.defer();
    //    deferred.resolve(res);
    //    return deferred.promise;
    };

}]);