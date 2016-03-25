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
    #Action code goes here, res should be a JSON structure


    #Action code ends here
    return json.dumps(res)



@foro.route('/foro/VForo')
def VForo():
    #GET parameter
    idForo = request.args['idForo']
    session['idForo'] = idForo
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure
    
    
    listaHilos = []
    for htitulo, hfecha, hforo_id in db.session.query(Hilo.titulo, Hilo.fecha_creacion, Hilo.foro_id):
        if hforo_id == session['idForo']:
            listaHilos += [ {'titulo':htitulo,'fecha': hfecha} ]
    
    res['data'] = listaHilos
    
    #Action code ends here
    return json.dumps(res)



@foro.route('/foro/VForos')
def VForos():
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure
    
    #res['data'] = [{'titulo':'Mi_Foro', 'fecha': '10/10/10'}, {'titulo':'Mi_Foro2', 'fecha': '10/10/11'}]
    
    listaForos = []
    for ftitulo, ffecha in db.session.query(Foro.titulo, Foro.fecha_creacion):
        listaForos += [ {'titulo':ftitulo,'fecha': ffecha} ]
    
    res['data'] = listaForos
    
    #Action code ends here
    return json.dumps(res)



@foro.route('/foro/VPublicacion')
def VPublicacion():
    #GET parameter
    idForo = request.args['idHilo']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure


    #Action code ends here
    return json.dumps(res)


@foro.route('/foro/AgregForo', methods=['POST'])
def AgregForo():
    params = request.get_json()
    results = [{'label':'/VForos', 'msg':['Foro Agregado']}, {'label':'/VForos', 'msg':['No se pudo agregar el nuevo foro']}]
    
    titulo_nuevo_foro = params['texto']
    nuevo_foro = Foro(titulo=titulo_nuevo_foro, nombre_usuario=session['nombre_usuario'])
    db.session.add(nuevo_foro)
    db.session.commit()
    
    res = results[0]
    print("TEST AGREG FORO: ",params)
    return json.dumps(res)


@foro.route('/foro/AgregHilo', methods=['POST'])
def AgregHilo():
    params = request.get_json()
    results = [{'label':'/VForo/'+session['idForo'], 'msg':['Hilo Agregado']}, {'label':'/VForos/'+session['idForo'], 'msg':['No se pudo agregar el nuevo hilo']}]
    
    titulo_nuevo_hilo = params['texto']
    
    pagina_sitio_test = Paginasitio.query.filter_by(url="www").first()
    if pagina_sitio_test is None :
        pagina_sitio_test = Paginasitio(url="www", usuario=Usuario.query.filter_by(nombre_usuario=session['nombre_usuario']).first())
        db.session.add(pagina_sitio_test)
        db.session.commit()
    
    
    foro_actual = Foro.query.filter_by(titulo=session['idForo']).first()
    
    nuevo_hilo = Hilo(titulo=titulo_nuevo_hilo, foro=foro_actual, pagina_sitio=pagina_sitio_test)
    db.session.add(nuevo_hilo)
    db.session.commit()
    
    res = results[0]
    print("TEST AGREG FORO: ",params)
    return json.dumps(res)


@foro.route('/foro/AElimForo')
def AElimForo():
    res = {}
    idForo = request.args['idForo']
    results = [{'label':'/VForos', 'msg':['Foro eliminado']}, {'label':'/VForos', 'msg':['No se pudo eliminar el foro']}, ]
    res = results[0]
    
    foro_a_eliminar = Foro.query.filter_by(titulo=idForo).first()
    db.session.delete(foro_a_eliminar)
    db.session.commit()
    
    return json.dumps(res)


@foro.route('/foro/AElimHilo')
def AElimHilo():
    res = {}
    idHilo = request.args['idHilo']
    results = [{'label':'/VForo/'+session['idForo'], 'msg':['Hilo eliminado']}, {'label':'/VForo/'+session['idForo'], 'msg':['No se pudo eliminar el hilo']}, ]
    res = results[0]
    
    hilo_a_eliminar = Hilo.query.filter_by(titulo=idHilo).first()
    db.session.delete(hilo_a_eliminar)
    db.session.commit()
    
    return json.dumps(res)

#Use case code starts here


#Use case code ends here

