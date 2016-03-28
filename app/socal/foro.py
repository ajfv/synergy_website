from flask import request, session, Blueprint, json

foro = Blueprint('foro', __name__)
from sqlalchemy.orm import sessionmaker
from base import Foro, Hilo, db, Publicacion, Usuario, Paginasitio

@foro.route('/foro/VComentariosPagina')
def VComentariosPagina():
    #GET parameter
    idPaginaSitio = request.args['idPaginaSitio']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
        res['usuario'] = {'nombre': session['nombre_usuario']}
    #Action code goes here, res should be a JSON structure


    #Action code ends here
    return json.dumps(res)

#------------------------------------------------------------------------------#
#                                    FORO                                      #
#------------------------------------------------------------------------------#

@foro.route('/foro/VForo')
def VForo():
    #GET parameter
    idForo = request.args['idForo']
    session['idForo'] = idForo
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
        res['usuario'] = {'nombre': session['nombre_usuario']}
    #Action code goes here, res should be a JSON structure
    
    listaHilos = []
    for h in Hilo.query.filter_by(foro_id=idForo):
        listaHilos += [{'id':h.id, 'titulo':h.raiz.titulo,'fecha': h.fecha_creacion}]

    res['data'] = listaHilos

    #Action code ends here
    return json.dumps(res)

#------------------------------------------------------------------------------#

@foro.route('/foro/VForos')
def VForos():
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
        res['usuario'] = {'nombre': session['nombre_usuario']}
    #Action code goes here, res should be a JSON structure
    listaForos = []
    for ftitulo, ffecha in db.session.query(Foro.titulo, Foro.fecha_creacion):
        listaForos += [ {'titulo':ftitulo,'fecha': ffecha} ]

    res['data'] = listaForos

    #Action code ends here
    return json.dumps(res)

#------------------------------------------------------------------------------#

@foro.route('/foro/AgregForo', methods=['POST'])
def AgregForo():
    params = request.get_json()
    results = [{'label':'/VForos', 'msg':['Foro Agregado']}, 
    {'label':'/VForos', 'msg':['No se pudo agregar el nuevo foro']}]

    titulo_nuevo_foro = params['texto']
    nuevo_foro = Foro(titulo=titulo_nuevo_foro, nombre_usuario=session['nombre_usuario'])
    db.session.add(nuevo_foro)
    db.session.commit()

    res = results[0]
    print("TEST AGREG FORO: ",params)
    return json.dumps(res)

#------------------------------------------------------------------------------#
#                                    HILO                                      #
#------------------------------------------------------------------------------#

@foro.route('/foro/VHilos')
def VHilos():
    #GET parameter
    res = {}
    idHilo = request.args['idHilo']
    if "actor" in session:
        res['actor']=session['actor']
        res['usuario'] = {'nombre': session['nombre_usuario']}
    #Action code goes here, res should be a JSON structure

    hilo = Hilo.query.filter_by(id=idHilo).first()
    raiz = hilo.raiz
    res['foroPadre'] =  hilo.foro_id
    res['tituloNuevaPublicacion'] = "RE: " + raiz.titulo
    res['publicaciones'] = raiz.a_diccionario()

    #Action code ends here
    return json.dumps(res)

#------------------------------------------------------------------------------#

@foro.route('/foro/AgregHilo', methods=['POST'])
def AgregHilo():
    params = request.get_json()
    results = [{'label':'/VForo/'+session['idForo'], 'msg':['Hilo Agregado']}, 
    {'label':'/VForos/'+session['idForo'], 'msg':['No se pudo agregar el nuevo hilo']}]

    titulo_publicacion  = params['titulo']
    contenido_publicacion = params['contenido']

    # Siento que esto no va
    pagina_sitio_test = Paginasitio.query.filter_by(url="www").first()
    if pagina_sitio_test is None :
        pagina_sitio_test = Paginasitio(url="www",
            usuario=Usuario.query.filter_by(nombre_usuario=session['nombre_usuario']).first())
        db.session.add(pagina_sitio_test)
        db.session.commit()


    # Se crean hilos
    foro_actual = Foro.query.filter_by(titulo=session['idForo']).first()

    nuevo_hilo = Hilo(foro=foro_actual,pagina_sitio=pagina_sitio_test)
    db.session.add(nuevo_hilo)
    db.session.commit()

    # Crear nueva publicacion:
    nueva_publicacion = Publicacion(titulo_publicacion,contenido_publicacion,
                                    session['nombre_usuario'],nuevo_hilo)

    db.session.add(nueva_publicacion)
    db.session.commit()

    res = results[0]
    print("TEST AGREG FORO: ",params)
    return json.dumps(res)

#------------------------------------------------------------------------------#

@foro.route('/foro/AElimForo')
def AElimForo():
    res = {}
    idForo = request.args['idForo']
    results = [{'label':'/VForos', 'msg':['Foro eliminado']},
     {'label':'/VForos', 'msg':['No se pudo eliminar el foro']}, ]
    res = results[0]

    foro_a_eliminar = Foro.query.filter_by(titulo=idForo).first()
    db.session.delete(foro_a_eliminar)
    db.session.commit()

    return json.dumps(res)

#------------------------------------------------------------------------------#

@foro.route('/foro/AElimHilo')
def AElimHilo():
    res = {}
    idHilo = request.args['idHilo']
    results = [{'label':'/VForo/'+session['idForo'], 'msg':['Hilo eliminado']},
     {'label':'/VForo/'+session['idForo'], 'msg':['No se pudo eliminar el hilo']}, ]
    res = results[0]

    hilo_a_eliminar = Hilo.query.filter_by(id=idHilo).first()
    db.session.delete(hilo_a_eliminar)
    db.session.commit()

    return json.dumps(res)

#------------------------------------------------------------------------------#
#                                 PUBLICACIÒN                                  #
#------------------------------------------------------------------------------#

@foro.route('/foro/VPublicacion')
def VPublicacion():
    #GET parameter
    idForo = request.args['idHilo']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
        res['usuario'] = {'nombre': session['nombre_usuario']}
    #Action code goes here, res should be a JSON structure


    #Action code ends here
    return json.dumps(res)

@foro.route('/foro/AgregPublicacion',methods=['POST'])
def AgregPublicacion():
    #GET parameter
    params = request.get_json()
    
    idPadre = params['id']
    titulo = params['titulo']
    contenido = params['contenido']

    padre = Publicacion.query.filter_by(id=idPadre).first()
    
    # Crear nueva publicacion hijo
    nueva_publicacion = Publicacion(titulo,contenido,session['nombre_usuario'],
                                    padre.hilo,padre)
    db.session.add(nueva_publicacion)
    db.session.commit()

    results = [{'label':'/VHilos/'+str(padre.hilo_id), 'msg':['Respuesta enviada']},
    {'label':'/VHilos/'+str(padre.hilo_id), 'msg':['No se pudo enviar la respuesta']}]
    res = results[0]
    #Action code ends here
    return json.dumps(res)

#------------------------------------------------------------------------------#

@foro.route('/foro/AElimPublicacion')
def AElimPublicacion():

    print("no llego aca")
    res = {}
    idPublicacion = request.args['idPublicacion']
    
    publicacion_a_eliminar = Publicacion.query.filter_by(id=idPublicacion).first()
    
    idHilo = publicacion_a_eliminar.hilo_id

    results = [{'label':'/VHilos/'+str(idHilo), 'msg':['Publicacion eliminada']}, {'label':'/VForo/'+str(idHilo), 'msg':['No se pudo eliminar la publicacion']}, ]
    res = results[0]

    publicacion_a_eliminar.contenido = 'Esta publicación fue eliminada.'
    publicacion_a_eliminar.eliminada = True
    db.session.commit()

    return json.dumps(res)
