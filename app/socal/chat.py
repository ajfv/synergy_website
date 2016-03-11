from flask import request, session, Blueprint, json
from base import Usuario, Pagina, db, Amigo, Chat, Mensaje
from sqlalchemy.orm import sessionmaker

chat = Blueprint('chat', __name__)
from base import Grupo, miembrosGrupo, db
from sqlalchemy import create_engine
from sqlalchemy.sql import select, insert

@chat.route('/chat/AElimContacto')
def AElimContacto():
    #GET parameter
    idContacto = request.args['id']
    results = [{'label':'/VAdminContactos', 'msg':['Contacto eliminado']}, {'label':'/VAdminContactos', 'msg':['No se pudo eliminar contacto']}, ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message

    res['label'] = res['label'] + '/' + session['nombre_usuario']


    usuarioActual = session['nombre_usuario']
    ContactoAEliminar = idContacto

    amistad1 = Amigo.query.filter_by(amigo1 = usuarioActual,amigo2 = ContactoAEliminar).first()
    amistad2 = Amigo.query.filter_by(amigo1 = ContactoAEliminar,amigo2 = usuarioActual,).first()

    db.session.delete(amistad1)
    db.session.delete(amistad2)

    db.session.commit()

    # nombre = params['nombre']
    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)


@chat.route('/chat/AElimMiembro')
def AElimMiembro():
    #GET parameter
    id = request.args['id']
    results = [{'label':'/VGrupo', 'msg':['Miembro eliminado']}, ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message

    res['label'] = res['label'] + '/' + repr(1)

    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)



@chat.route('/chat/AEscribir', methods=['POST'])
def AEscribir():
    #POST/PUT parameters
    params = request.get_json()
    print("PARAMS",params)
    #print("AMIGO",session['amigo'])
    texto = params['texto']

    amigo = session['amigo']
    usuarioActual = session['nombre_usuario']

    results = [{'label':'/VChat', 'msg':['Enviado']}, {'label':'/VChat', 'msg':['No se pudo enviar mensaje']}, ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message
    res['label'] = res['label'] + '/' + session['amigo'] 

    
    busqueda = Amigo.query.filter_by(amigo1=usuarioActual,amigo2=amigo).first()
    chat = Chat.query.filter_by(id = busqueda.chat_id).first()

    mensaje = Mensaje(usuarioActual,texto,busqueda.chat_id)
    db.session.add(mensaje)
    db.session.commit()

    chat.mensaje = mensaje
    db.session.commit()

    print("BUSQUEDA",busqueda.amigo1,busqueda.amigo2,busqueda.chat_id)


    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)



@chat.route('/chat/ASalirGrupo')
def ASalirGrupo():
    #POST/PUT parameters
    params = request.get_json()
    results = [{'label':'/VAdminContactos', 'msg':['Ya no estás en ese grupo']}, {'label':'/VGrupo', 'msg':['Sigues en el grupo']}, ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message

    res['label'] = res['label'] + '/' + repr(1)


    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)



@chat.route('/chat/AgregContacto', methods=['POST'])
def AgregContacto():
    #POST/PUT parameters
    params = request.get_json()
    results = [{'label':'/VAdminContactos', 'msg':['Contacto agregado']}, {'label':'/VAdminContactos', 'msg':['No se pudo agregar contacto']}, ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message

    res['label'] = res['label'] + '/' + session['nombre_usuario']



    usuarioActual = session['nombre_usuario']
    ContactoNuevo = params['nombre']

    # Se crea un nuevo chat:
    nuevoChat = Chat()
    db.session.add(nuevoChat)
    db.session.commit()

    # Se crean las relaciones de amigos:
    amigos1 = Amigo(usuarioActual,ContactoNuevo,nuevoChat.id)
    amigos2 = Amigo(ContactoNuevo,usuarioActual,nuevoChat.id)

    db.session.add(amigos1)
    db.session.add(amigos2)
    db.session.commit()


    # usuario1 = Usuario.query.filter_by(nombre_usuario = usuarioActual).first()
    # usuario2 = Usuario.query.filter_by(nombre_usuario = ContactoNuevo ).first()

    # nuevoChat = Chat()
    # db.session.add(nuevoChat)

    # usuario1.amigos.append(usuario2,nuevoChat.id)
    # usuario2.amigos.append(usuario1,nuevoChat.id)
    # db.session.commit()


    # Amigo = db.session.query(amigos).filter(amigos.c.usuario_id==usuarioActual).one()
    # print("AMIGO",Amigo.chat_id,Amigo.amigo_id)
    # Amigo.chat_id = AmigosnuevoChat.id



    # db.session.commit()

    print(ContactoNuevo)
    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)



@chat.route('/chat/AgregMiembro', methods=['POST'])
def AgregMiembro():
    #POST/PUT parameters
    params = request.get_json()
    results = [{'label':'/VGrupo', 'msg':['Nuevo miembro agregado']}, {'label':'/VGrupo', 'msg':['No se pudo agregar al nuevo miembro']}, ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message
    
    res['label'] = res['label'] + '/' + repr(1)
    id_grupo = res['label']
    usuario = params['nombre']
    
    grupo = Grupo.query.filter_by(nombre = id_grupo).first()
    usuario = Usuario.query.filter_by(nombre_usuario = usuario).first()
    
    
    grupo.miembrosGrupo.append([grupo,usuario])
    
    
    db.session.commit()
    
    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)



@chat.route('/chat/VAdminContactos')
def VAdminContactos():
    #GET parameter
    idUsuario = request.args['idUsuario']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure

    res['idContacto'] = idUsuario 
    Amistades = Amigo.query.filter_by(amigo1=idUsuario).all()
 
    listaAmigos = []
    amigos = []

    for i in Amistades:
        listaAmigos += [ {'idContacto':i.amigo2,'nombre':i.amigo2, 'tipo':'usuario'} ]
        amigos += [i.amigo2]

    res['data1'] = listaAmigos

    res['data2'] = [
      {'idContacto':56, 'nombre':'Grupo Est. Leng.', 'tipo':'grupo'},
    ]
    res['idGrupo'] = 'Grupo Est. Leng.'

    nombres = Usuario.query.all()

    opciones_usuarios = []
    for i in nombres:
        if(i.nombre_usuario!= idUsuario and i.nombre_usuario not in amigos):
            opciones_usuarios += [{'key':i.nombre_usuario,'value':i.nombre_usuario}]


    # res['fContacto_opcionesNombre'] = [
    #   {'key':'pepe', 'value':'Pepe'},
    #  {'key':'juana', 'value':'Juana'},
    #   {'key':'maria', 'value':'Maria'},
    # ]

    res['fContacto_opcionesNombre'] = opciones_usuarios


    #Action code ends here
    return json.dumps(res)



@chat.route('/chat/VChat')
def VChat():
    #GET parameter
    idChat = request.args['idChat']
    session['amigo'] = idChat
    print("ID CHAT",idChat)
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure

    res['idChat'] = idChat
    res['idUsuario'] = session['nombre_usuario']

    usuarioActual = session['nombre_usuario']
    amigo = idChat

    busqueda = Amigo.query.filter_by(amigo1=usuarioActual,amigo2=amigo).first()
    chat = Chat.query.filter_by(id = busqueda.chat_id).first()
    mensaje = chat.mensajes

    Lista = []

    for i in mensaje:
        Lista += [{'texto':i.contenido,'usuario':i.usuario_origen,'fecha':i.creado}]

    res['mensajesAnt'] = Lista

    #Action code ends here
    return json.dumps(res)



@chat.route('/chat/VContactos')
def VContactos():
    #GET parameter
    idUsuario = request.args['idUsuario']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure

    res['idContacto'] = 1

    listaAmigos = []

    User = Amigo.query.filter_by(amigo1=idUsuario).all()

    for i in User:
        listaAmigos += [{'idContacto':i.amigo2,'nombre':i.amigo2, 'tipo':'usuario'}]

    listaAmigos += [{'idContacto':'mango', 'nombre':'Grupo Est. Leng.', 'tipo':'grupo'}]
    res['data1'] = listaAmigos
    res['idUsuario'] = idUsuario # Esto arregla el botón del prof


    #Action code ends here
    return json.dumps(res)



@chat.route('/chat/VGrupo')
def VGrupo():
    #GET parameter
    idGrupo = request.args['idGrupo']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure
    
    res['idGrupo'] = 'Grupo Est. Leng.'
    res['fMiembro_opcionesNombre'] = [
      {'key':1, 'value':'Leo'},
      {'key':2, 'value':'Lauri'},
      {'key':3, 'value':'Mara'},
      
    ]
    res['data3'] = [
      {'idContacto':34, 'nombre':'ana', 'tipo':'usuario'},
      {'idContacto':23, 'nombre':'leo', 'tipo':'usuario'},
      {'idContacto':11, 'nombre':'distra', 'tipo':'usuario'},
      {'idContacto':40, 'nombre':'vane', 'tipo':'usuario'},
    ]

    #Action code ends here
    return json.dumps(res)


# @chat.route('/chat/VAgregarContacto')
# def VGrupo():
#     #GET parameter
#     idGrupo = request.args['idGrupo']
#     res = {}
#     if "actor" in session:
#         res['actor']=session['actor']
#     #Action code goes here, res should be a JSON structure

#     res['idGrupo'] = 1
#     res['fMiembro_opcionesNombre'] = [
#       {'key':1, 'value':'Leo'},
#       {'key':2, 'value':'Lauri'},
#       {'key':3, 'value':'Mara'},
#     ]

#     #Action code ends here
    # return json.dumps(res)





#Use case code starts here


#Use case code ends here
