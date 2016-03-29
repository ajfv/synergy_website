from flask import request, session, Blueprint, json

ident = Blueprint('ident', __name__)
from base import Usuario, Pagina, db, Sitio


@ident.route('/ident/APaginaSitio')

def APaginaSitio():
    #GET parameter
    idPaginaSitio = request.args['idPaginaSitio']
    
    res={}
    res['label'] = 'VPrincipal/'+idPaginaSitio
    session.pop('idPaginaSitio')
    session['idPaginaSitio'] = idPaginaSitio
    
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)

    
@ident.route('/ident/AIdentificar', methods=['POST'])
def AIdentificar():
    #POST/PUT parameters
    params = request.get_json()
    results = [{'label':'/VPrincipal', 'msg':['Bienvenido usuario'], "actor":"duenoProducto"}, {'label':'/VLogin', 'msg':['Datos de identificación incorrectos']}, ]
    res = results[1]
    #Action code goes here, res should be a list with a label and a message

    for nombre_usuario, clave in db.session.query(Usuario.nombre_usuario, Usuario.clave) :
        if nombre_usuario == params['usuario'] and clave == params['clave'] :
            res = results[0]
            session['nombre_usuario']=params['usuario']
            
            session['idPaginaSitio'] = " "
            res['idPaginaSitio'] = " "
            break

    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)



@ident.route('/ident/ARegistrar', methods=['POST'])
def ARegistrar():
    #POST/PUT parameters
    params = request.get_json()
    results = [{'label':'/VLogin', 'msg':['Felicitaciones, Ya estás registrado en la aplicación']}, {'label':'/VRegistro', 'msg':['Error al tratar de registrarse']}, ]
    res = results[1]

    # Se verifica si el usuario existe en la base de datos
    usuarioExistente = Usuario.query.filter_by(nombre_usuario=\
                                    params['usuario']).first()

    if not(usuarioExistente):
        res = results[0]
        nuevo_usuario = Usuario(nombre_completo=params['nombre']
                                ,nombre_usuario=params['usuario']
                                ,clave=params['clave']
                                ,correo=params['correo'])

        db.session.add(nuevo_usuario)

        db.session.commit()

    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)



@ident.route('/ident/VLogin')
def VLogin():
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure

    session.pop('nombre_usuario', None)

    #Action code ends here
    return json.dumps(res)



@ident.route('/ident/VPrincipal')
def VPrincipal():
    
    
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure

    res['idUsuario'] = session['nombre_usuario']
    res["usuario"] = {"nombre":res['idUsuario']}
    if (session['idPaginaSitio'] == " "):
        pags = Sitio.query.all()
        paginas = []
        for pag in pags:
            paginas.append({'id':pag.id,'titulo':pag.titulo,'contenido':pag.contenido,'imagenes':pag.imagenes})
        res["paginas"] = paginas
        res["pag"] = {"id": True,'titulo': "Hola " + session['nombre_usuario']}
        res['principal'] = 1
        
    else:
        idPaginaSitio = session['idPaginaSitio']
        pagina = Sitio.query.filter_by(id = idPaginaSitio ).first()
        res['pag'] = {"id":pagina.id,"titulo":pagina.titulo,"contenido":pagina.contenido,"imagenes":pagina.imagenes}
        res['principal'] = 0
    print(session)
    #Action code ends here
    return json.dumps(res)




@ident.route('/ident/VRegistro')
def VRegistro():
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure


    #Action code ends here
    return json.dumps(res)





#Use case code starts here


#Use case code ends here
