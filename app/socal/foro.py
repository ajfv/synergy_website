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
    
    res['data'] = [{'titulo':'Mi_Hilo', 'fecha': '10/10/10'}, {'titulo':'Mi_Hilo2', 'fecha': '10/10/11'}]
    
    #Action code ends here
    return json.dumps(res)



@foro.route('/foro/VForos')
def VForos():
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure
    
    res['data'] = [{'titulo':'Mi_Foro', 'fecha': '10/10/10'}, {'titulo':'Mi_Foro2', 'fecha': '10/10/11'}]

    #Action code ends here
    return json.dumps(res)



@foro.route('/foro/VPublicacion')
def VPublicacion():
    #GET parameter
    idForo = request.args['idForo']
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
    res = results[0]
    print("TEST AGREG FORO: ",params)
    return json.dumps(res)


@foro.route('/foro/AgregHilo', methods=['POST'])
def AgregHilo():
    params = request.get_json()
    results = [{'label':'/VForo/'+session['idForo'], 'msg':['Hilo Agregado']}, {'label':'/VForo', 'msg':['No se pudo agregar el nuevo hilo']}]
    res = results[0]
    print("TEST AGREG HILO: ",params)
    return json.dumps(res)




#Use case code starts here


#Use case code ends here

