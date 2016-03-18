from flask import request, session, Blueprint, json
from sqlalchemy.orm import sessionmaker
from base import Usuario, Pagina, db, Grupo,Chat, Mensaje, Amigo

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
    results = [{'label':'/VGrupo', 'msg':['Miembro eliminado']},{'label':'/VGrupo', 'msg':['No se puede eliminar miembro']}, ]
    res = results[1]
    #Action code goes here, res should be a list with a label and a message

    admin = Usuario.query.filter_by(nombre_usuario = session.get('nombre_usuario')).first()
    grupo = Grupo.query.filter_by(id = session.get('idGrupo')).first()

    if(grupo.admin == admin):
        #Se obtiene el usuario a eliminar.
        usuarioElim = Usuario.query.filter_by(nombre_usuario = id).first()
        grupo.miembros.remove(usuarioElim)
        db.session.add(grupo)
        db.session.commit()
        res = results[0]

    #URL después de eliminar.
    res['label'] = res['label'] + '/' + str(grupo.id)

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
    texto = params['texto']

    idChat = session['idChat']
    usuarioActual = session['nombre_usuario']

    results = [{'label':'/VChat', 'msg':['Enviado']}, {'label':'/VChat', 'msg':['No se pudo enviar mensaje']}, ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message
    res['label'] = res['label'] + '/' + session['idChat']

    chat = Chat.query.filter_by(id = idChat).first()

    mensaje = Mensaje(usuarioActual,texto,idChat)
    db.session.add(mensaje)
    db.session.commit()

    chat.mensaje = mensaje
    db.session.commit()

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

    nombreUsuario = session.get('nombre_usuario')
    usuario = Usuario.query.filter_by(nombre_usuario = nombreUsuario).first()
    id_grupo = session.get('idGrupo')

    grupo = Grupo.query.filter_by(id = id_grupo).first()
    grupo.miembros.remove(usuario)

    #Si era la única persona en el grupo debe eliminarse de la tabla.
    if (len(grupo.miembros) == 0):
        db.session.delete(grupo)
    else:
        #Si el usuario es administrador, la administración se le otorga a otra persona.
        if (grupo.admin == usuario):
            grupo.admin = grupo.miembros[0]
        db.session.add(grupo)

    db.session.commit()

    #Para regresarse a la vista anterior siendo el mismo usuario.
    res['label'] = res['label'] + '/' + nombreUsuario

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

    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)


@chat.route('/chat/AgregGrupo')
def AgregGrupo():
    results = [{'label':'/VAdminContactos', 'msg':['Grupo agregado']}, {'label':'/VAdminContactos', 'msg':['Error al crear grupo']}, ]
    #GET parameter
    #idUsuario = request.args['idUsuario']
    idUsuario = session.get('nombre_usuario')
    res = results[0]
    #Action code goes here, res should be a list with a label and a message

    res['label'] = res['label'] + '/' + idUsuario
    #El usuario que agrega el grupo sera el administrador
    admin = Usuario.query.filter_by(nombre_usuario=idUsuario).first()

    # Se crea un nuevo chat:
    nuevoChat = Chat()
    db.session.add(nuevoChat)
    db.session.commit()

    #Se obtiene el id del último grupo en la tabla para establecer el nombre del grupo.
    ultimoGrupo = Grupo.query.order_by(Grupo.id).all()
    if (ultimoGrupo):
        idNuevoGrupo = ultimoGrupo[len(ultimoGrupo) -1].id + 1
    else:
        idNuevoGrupo = 1;
    nombreNuevoGrupo = "Grupo Synergy " + str(idNuevoGrupo)
    nuevoGrupo = Grupo(nombreNuevoGrupo,admin,nuevoChat)
    nuevoGrupo.miembros.append(admin)
    db.session.add(nuevoGrupo)
    db.session.commit()

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

    nombreUsuario = params['nombre']
    usuario = Usuario.query.filter_by(nombre_usuario = nombreUsuario).first()
    id_grupo = session.get('idGrupo')
    res['label'] = res['label'] + '/' + id_grupo
    #Descomentar lo de abajo cuando se tenga la especificación de crear grupos.
    grupo = Grupo.query.filter_by(id = id_grupo).first()
    grupo.miembros.append(usuario)
    db.session.add(grupo)

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

    #Ahora, se añade la información de los grupos del usuario. y se guarda en data2.
    usuarioID = Usuario.query.filter_by(nombre_usuario = idUsuario).first()
    listaGrupos = []

    if(usuarioID.grupos):
        for i in usuarioID.grupos:
            listaGrupos += [ {'idContacto':i.id,'nombre':i.nombre,'tipo':'grupo'} ]

    res['data2'] = listaGrupos

    nombres = Usuario.query.all()

    opciones_usuarios = []
    for i in nombres:
        if(i.nombre_usuario!= idUsuario and i.nombre_usuario not in amigos):
            opciones_usuarios += [{'key':i.nombre_usuario,'value':i.nombre_usuario}]



    res['fContacto_opcionesNombre'] = opciones_usuarios


    #Action code ends here
    return json.dumps(res)


@chat.route('/chat/VChat')
def VChat():
    #GET parameter
    idChat = request.args['idChat']
    session['idChat'] = idChat
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure

    res['idChat'] = idChat
    res['idUsuario'] = session['nombre_usuario']

    usuarioActual = session['nombre_usuario']

    chat = Chat.query.filter_by(id = idChat).first()
    mensaje = chat.mensajes
    mensaje = reversed(chat.mensajes)

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
        listaAmigos += [{'idContacto':i.chat_id,'nombre':i.amigo2, 'tipo':'usuario'}]

    usuarioID = Usuario.query.filter_by(nombre_usuario = idUsuario).first()


    if(usuarioID.grupos):
        for i in usuarioID.grupos:
            listaAmigos += [ {'idContacto':i.chat_id,'nombre':i.nombre,'tipo':'grupo'} ]

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

    #Para que el botón de regresar cuando se modifique un grupo funcione.
    res['idUsuario'] = session['nombre_usuario']
    session['idGrupo']=idGrupo
    res['idGrupo'] = idGrupo


    #En data3 van los miembros del grupo.
    grupoModificar = Grupo.query.filter_by(id = idGrupo).first()
    miembrosGrupo = []
    idMiembros =[]
    if (grupoModificar.miembros):
        for miembro in grupoModificar.miembros:
            if(miembro.nombre_usuario != session['nombre_usuario']):
                miembrosGrupo += [ {
                    'idContacto':miembro.nombre_usuario,
                    'nombre':miembro.nombre_usuario,
                    'tipo':'usuario'
                    } ]
            idMiembros += [miembro.nombre_usuario]
    usuario = Usuario.query.filter_by(nombre_usuario=session['nombre_usuario']).first()
    Amigos = Amigo.query.filter_by(amigo1=session['nombre_usuario']).all()
    posibles_miembros = []
    if Amigos != None:
        for i in Amigos:
            if i.amigo2 not in idMiembros:
                posibles_miembros += [{'key':i.amigo2,'value':i.amigo2}]

    res['data3'] = miembrosGrupo
    res['fMiembro_opcionesNombre'] = posibles_miembros

    #Action code ends here
    return json.dumps(res)
