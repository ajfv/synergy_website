from flask import request, session, Blueprint, json

foro = Blueprint('foro', __name__)
from sqlalchemy.orm import sessionmaker
from base import Foro, Hilo, db, Publicacion, Usuario, Paginasitio, Sitio, Comentario

#------------------------------------------------------------------------------#
#                   COMENTARIOS DE PAGINAS DE SITIO                            #
#------------------------------------------------------------------------------#

@foro.route('/foro/VComentariosPagina')
def VComentariosPagina():
    #GET parameter
    idPaginaSitio = request.args['idPaginaSitio']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
        res['usuario'] = {'nombre': session['nombre_usuario']}
    #Action code goes here, res should be a JSON structure
    
    res['idPaginaSitio'] = idPaginaSitio
    sitio = Sitio.query.filter_by(id = idPaginaSitio).first()
    
    res['comentarios'] = []
    if sitio.comentariosActivados:
        comentarios = Comentario.query.filter_by(pagina_id = idPaginaSitio)
        for c in comentarios:
            res['comentarios'] += [{'id':c.id,'autor':c.autor_id, 'contenido':c.contenido}]
            
    #Action code ends here
    return json.dumps(res)
#------------------------------------------------------------------------------#

@foro.route('/foro/AgregComentario', methods=['POST'])
def AgregComentario():
    #POST/PUT parameters
    params = request.get_json()
    results = [{'label':'/VComentariosPagina', 'msg':['Comentario agregado']}, {'label':'/VComentariosPagina', 'msg':['No se pudo agregar comentario']}, ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message

    sitio = Sitio.query.filter_by(id = session['idPaginaSitio']).first()
    sitio.comentariosActivados = True
   
    ultimo = Comentario.query.order_by(Comentario.id).all()
    if (ultimo):
        idNuevo = ultimo[len(ultimo) -1].id + 1
        nuevo = Comentario(idNuevo, session['idPaginaSitio'], params['texto'], session['nombre_usuario'], idNuevo - 1)
        res = results[0]
        
    else:
        idNuevo = 1;
        nuevo = Comentario(idNuevo, session['idPaginaSitio'], params['texto'], session['nombre_usuario'], idNuevo)
        res = results[0]
        
    
    db.session.add(nuevo)
    db.session.commit()
    res['label'] = res['label'] + '/' + str(session['idPaginaSitio'])
    
    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)

#------------------------------------------------------------------------------#

@foro.route('/foro/AEliminarComentario')
def AEliminarComentario():
    #GET parameter
    id = request.args['id']
    results = [{'label':'/VComentariosPagina', 'msg':['Comentario eliminado.']},{'label':'/VComentariosPagina', 'msg':['No se puede eliminar comentario.']}, ]
    res = results[1]
    #Action code goes here, res should be a JSON structure
    
    comentario = Comentario.query.filter_by(id = id).first()
    if (session['nombre_usuario'] == comentario.autor_id):
        db.session.delete(comentario)
        db.session.commit()
        res = results[0]
        
    res['label'] = res['label'] + '/' + str(session['idPaginaSitio'])
    
    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
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
    
    listaHilos = [{
        'id': h.id, 
        'titulo': h.raiz.titulo,
        'fecha': h.fecha_creacion,
        'autor': h.raiz.autor_id}
        for h in Hilo.query.filter_by(foro_id=idForo)]

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
    for ftitulo, ffecha,fautor in db.session.query(Foro.titulo, Foro.fecha_creacion,Foro.autor_id):
        listaForos.append({'titulo':ftitulo,'fecha': ffecha,'autor':fautor})

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
    
    foro_a_eliminar = Foro.query.filter_by(titulo=idForo).first()
    if foro_a_eliminar.autor_id == session['nombre_usuario']:
        db.session.delete(foro_a_eliminar)
        db.session.commit()
        res = results[0]
    else:
        res = results[1]

    return json.dumps(res)

#------------------------------------------------------------------------------#

@foro.route('/foro/AElimHilo')
def AElimHilo():
    res = {}
    idHilo = request.args['idHilo']
    results = [{'label':'/VForo/'+session['idForo'], 'msg':['Hilo eliminado']},
     {'label':'/VForo/'+session['idForo'], 'msg':['No se pudo eliminar el hilo']}, ]
    
    hilo_a_eliminar = Hilo.query.filter_by(id=idHilo).first()
    if hilo_a_eliminar.raiz.autor_id == session['nombre_usuario']:
        db.session.delete(hilo_a_eliminar)
        db.session.commit()
        res = results[0]
    else:
        res = results[1]

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

    res = {}
    idPublicacion = request.args['idPublicacion']
    publicacion_a_eliminar = Publicacion.query.filter_by(id=idPublicacion).first()
    idHilo = publicacion_a_eliminar.hilo_id
    results = [{'label':'/VHilos/'+str(idHilo), 'msg':['Publicacion eliminada']}, 
    {'label':'/VForo/'+str(idHilo), 'msg':['No se pudo eliminar la publicacion']}]
    
    if publicacion_a_eliminar.autor_id == session['nombre_usuario']:
        publicacion_a_eliminar.contenido = 'Esta publicación fue eliminada.'
        publicacion_a_eliminar.eliminada = True
        db.session.commit()
        res = results[0]
    else:
        res = results[1]
    
    return json.dumps(res)



