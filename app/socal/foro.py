from flask import request, session, Blueprint, json

foro = Blueprint('foro', __name__)
from sqlalchemy.orm import sessionmaker
from base import Foro, Hilo, db, Publicacion, Usuario, Sitio

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
    #Action code goes here, res should be a JSON structure
    
    listaHilos = [{
        'id': h.id, 
        'titulo': h.raiz.titulo,
        'fecha': h.fecha_creacion,
        'autor': h.raiz.autor_id}
        for h in Hilo.query.filter_by(foro_id=idForo)]

    if 'nombre_usuario' in session:
        res['idUsuario'] = session['nombre_usuario']

    res['data'] = listaHilos

    #Action code ends here
    return json.dumps(res)

#------------------------------------------------------------------------------#

@foro.route('/foro/VForos')
def VForos():
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure
    listaForos = []
    for ftitulo, ffecha,fautor in db.session.query(Foro.titulo, Foro.fecha_creacion,Foro.autor_id):
        listaForos.append({'titulo':ftitulo,'fecha': ffecha,'autor':fautor})

    res['data'] = listaForos    

    if 'nombre_usuario' in session:
        res['idUsuario'] = session['nombre_usuario']

    #Action code ends here
    return json.dumps(res)

#------------------------------------------------------------------------------#

@foro.route('/foro/AgregForo', methods=['POST'])
def AgregForo():
    params = request.get_json()
    results = [{'label':'/VForos', 'msg':['Foro Agregado']}, 
    {'label':'/VForos', 'msg':['No se pudo agregar el nuevo foro']}]

    titulo_nuevo_foro = params['texto']
    foro_ya_existe = Foro.query.filter_by(titulo=titulo_nuevo_foro).first()

    res = results[1]
    if foro_ya_existe is None:
        if 'nombre_usuario' in session:
            nuevo_foro = Foro(titulo=titulo_nuevo_foro, nombre_usuario=session['nombre_usuario'])
            db.session.add(nuevo_foro)
            db.session.commit()
            res = results[0]

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
    #Action code goes here, res should be a JSON structure

    hilo = Hilo.query.filter_by(id=idHilo).first()
    raiz = hilo.raiz
    if hilo.sitio is None:
        res['foroPadre'] =  hilo.foro_id
    res['tituloNuevaPublicacion'] = "RE: " + raiz.titulo
    res['publicacion'] = raiz.a_diccionario()

    if 'nombre_usuario' in session:
        res['idUsuario'] = session['nombre_usuario']

    #Action code ends here
    return json.dumps(res)

#------------------------------------------------------------------------------#

@foro.route('/foro/AgregHilo', methods=['POST'])
def AgregHilo():
    params = request.get_json()
    results = [{'label':'/VForo/'+session['idForo'], 'msg':['Hilo Agregado']}, 
    {'label':'/VForos/'+session['idForo'], 'msg':['No se pudo agregar el nuevo hilo']}]

    if 'nombre_usuario' not in session:
        return json.dump(results[1])
    titulo_publicacion  = params['titulo']
    contenido_publicacion = params['contenido']

    # Se crean hilos
    foro_actual = Foro.query.filter_by(titulo=session['idForo']).first()

    nuevo_hilo = Hilo(foro=foro_actual)
    db.session.add(nuevo_hilo)
    db.session.commit()

    # Crear nueva publicacion:
    nueva_publicacion = Publicacion(titulo_publicacion,contenido_publicacion,
                                    session['nombre_usuario'],nuevo_hilo)

    db.session.add(nueva_publicacion)
    db.session.commit()

    res = results[0]
    return json.dumps(res)

#------------------------------------------------------------------------------#

@foro.route('/foro/AElimForo')
def AElimForo():
    res = {}
    idForo = request.args['idForo']
    results = [{'label':'/VForos', 'msg':['Foro eliminado']},
     {'label':'/VForos', 'msg':['No se pudo eliminar el foro']}, ]
    
    if 'nombre_usuario' not in session:
        return json.dump(results[1])
    
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
    
    if 'nombre_usuario' not in session:
        return json.dump(results[1])
        
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

@foro.route('/foro/AgregPublicacion',methods=['POST'])
def AgregPublicacion():
    #GET parameter
    params = request.get_json()
    results = [{'msg':['Respuesta enviada']},{'msg':['No se pudo enviar la respuesta']}]
    
    if 'nombre_usuario' not in session:
        return json.dump(results[1])
        
    idPadre = params['id']
    titulo = params['titulo']
    contenido = params['contenido']

    padre = Publicacion.query.filter_by(id=idPadre).first()
    if padre is None or padre.eliminada:
        res = results[1]
    else:
        # Crear nueva publicacion hijo
        nueva_publicacion = Publicacion(
            titulo, contenido, session['nombre_usuario'], padre.hilo,padre
        )
        db.session.add(nueva_publicacion)
        db.session.commit()
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
    results = [{'msg':['Publicacion eliminada']}, {'msg':['No se pudo eliminar la publicacion']}]
    
    if 'nombre_usuario' not in session:
        return json.dump(results[1])
    
    if publicacion_a_eliminar.autor_id == session['nombre_usuario']:
        if publicacion_a_eliminar.hijos == []:
            db.session.delete(publicacion_a_eliminar)
        else:
            publicacion_a_eliminar.contenido = 'Esta publicación fue eliminada.'
            publicacion_a_eliminar.eliminada = True
        db.session.commit()
        res = results[0]
    else:
        res = results[1]
    
    return json.dumps(res)
