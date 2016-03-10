from flask import request, session, Blueprint, json

chat = Blueprint('chat', __name__)
from base import Grupo, miembrosGrupo, db
from sqlalchemy import create_engine
from sqlalchemy.sql import select, insert

@chat.route('/chat/AElimContacto')
def AElimContacto():
    #GET parameter
    id = request.args['id']
    results = [{'label':'/VAdminContactos', 'msg':['Contacto eliminado']}, {'label':'/VAdminContactos', 'msg':['No se pudo eliminar contacto']}, ]
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
    results = [{'label':'/VChat', 'msg':['Enviado']}, {'label':'/VChat', 'msg':['No se pudo enviar mensaje']}, ]
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

    res['label'] = res['label'] + '/' + repr(1)

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
    #En params está el ID de la persona a agregar.
    #Para hacer conexiones a la tabla miembrosGrupo.
    #conn = engine.connect()
    
    #Se verifica si la persona ya está en el grupo. Como miembrosGrupo es una tabla
    #no se pueden hacer queries sobre ella, sino que hay que aplicar SQL.
    #selectMiembros = select([miembrosGrupo])
    #for filas in conn.execute(selectMiembros):
    #    print(filas)
    #select(miembrosGrupo).where(usuario=params['nombre'],grupo=res['label'])
    #engine = create_engine('postgresql+psycopg2://synergy:lacontraseña@localhost/ci3715_db')
    #ins = insert(miembrosGrupo)\
    #    .values(grupo=res['label'],usuario=params['nombre'])
    #print(ins)
#    conn = engine.connect()
#    result = conn.execute(ins)
    #Se agrega el usuario a la tabla de miembrosGrupo.
    #miembroNuevo =  miembrosGrupo(grupo=res['label'],usuario=params['nombre'])
    #db.session.add(miembroNuevo)
    
    #db.session.commit()
    
    #Se ejecuta la inserción
    #result = conn.execute(ins)
    
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

    res['idContacto'] = 1
    res['data1'] = [
      {'idContacto':34, 'nombre':'ana', 'tipo':'usuario'},
      {'idContacto':23, 'nombre':'leo', 'tipo':'usuario'},
      {'idContacto':11, 'nombre':'distra', 'tipo':'usuario'},
      {'idContacto':40, 'nombre':'vane', 'tipo':'usuario'},
    ]
    res['data2'] = [
      {'idContacto':56, 'nombre':'Grupo Est. Leng.', 'tipo':'grupo'},
    ]
    res['idGrupo'] = 1
    res['fContacto_opcionesNombre'] = [
      {'key':1, 'value':'Leo'},
      {'key':2, 'value':'Lauri'},
      {'key':3, 'value':'Mara'},
    ]

    #Action code ends here
    return json.dumps(res)



@chat.route('/chat/VChat')
def VChat():
    #GET parameter
    idChat = request.args['idChat']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure

    res['idChat'] = 1
    res['idUsuario'] = 1
    res['mensajesAnt'] = [
      {'texto': '¿Me traes mi gato por la tarde?', 'usuario':'ana', 'fecha':'lun feb 29 09:08:17 VET 2016'},
      {'texto': '¡Hay! no lo encuentro, debió escaparse. Ahora salgo a buscarlo', 'usuario':'distra', 'fecha':'lun feb 29 09:09:17 VET 2016'},
      {'texto': 'Hola vane, ayer al pasar por tu casa dejé a naco mi anacondita..', 'usuario':'uri', 'fecha':'lun feb 29 09:09:17 VET 2016'},
      {'texto': 'La dejasete fue en mi casa. No la había visto porque está en un rincon, no se mueve y ... pareceira que tiene algo atragantado.', 'usuario':'distra', 'fecha':'lun feb 29 09:10:17 VET 2016'},
      {'texto': '¿Qué?', 'usuario':'ana', 'fecha':'lun feb 29 09:12:17 VET 2016'},
    ]

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
    res['data1'] = [
      {'idContacto':34, 'nombre':'ana', 'tipo':'usuario'},
      {'idContacto':23, 'nombre':'leo', 'tipo':'usuario'},
      {'idContacto':11, 'nombre':'distra', 'tipo':'usuario'},
      {'idContacto':40, 'nombre':'vane', 'tipo':'usuario'},
      {'idContacto':56, 'nombre':'Grupo Est. Leng.', 'tipo':'grupo'},
    ]
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

    res['idGrupo'] = 1
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
