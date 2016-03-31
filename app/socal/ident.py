from flask import request, session, Blueprint, json

ident = Blueprint('ident', __name__)
from base import Usuario, Pagina, db, Sitio, Hilo, Publicacion
    
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
            break

    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)

@ident.route('/ident/ASalir', methods=['POST'])
def ASalir():
    params = request.get_json()
    results = [{'msg':['Cerraste sesión satisfactoriamente.']}, 
    {'msg':['No se pudo cerrar sesión.']} ]
    res = results[1]
    #Action code goes here, res should be a list with a label and a message
    if 'nombre_usuario' in session and params['idUsuario'] == session['nombre_usuario']:
        session.pop('nombre_usuario')
        res = results[0]
    else:
        res = results[1]
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
    pags = Sitio.query.all()
    paginas = [{
        'id':pag.id,
        'titulo':pag.titulo,
        'contenido':pag.contenido,
        'imagenes':pag.imagenes
        } for pag in pags
    ]
    res["paginas"] = paginas
    
    idPagina = 'principal'
    pag = Sitio.query.filter_by(id=idPagina).first()
    
    if pag is None:
        print("aqui")
        s = Sitio("principal",'')
        db.session.add(s)
        db.session.commit()
        h = Hilo(sitio=s)
        db.session.add(h)
        db.session.commit()
        p = Publicacion(s.titulo, s.titulo, hilo=h)
        db.session.add(p)
        db.session.commit()
        pag = Sitio.query.filter_by(id=idPagina).first()
    res['pag'] = {
        'hilo': pag.hilo.id, 'titulo': pag.titulo, 
        'contenido': pag.contenido, 'imagenes': pag.imagenes}
     
    if 'nombre_usuario' in session:
        res['idUsuario'] = session['nombre_usuario']
    #Action code ends here
    return json.dumps(res)

@ident.route('/ident/VSecundaria')
def VSecundaria():
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure
    idPagina = request.args['idPagina']
    pag = Sitio.query.filter_by(id=idPagina).first()
    if pag is None:
        res['pag'] = {
            'hilo':-1, 'titulo': 'Lo sentimos',
            'contenido': 'La página que busca no existe.', 'imagenes':''}
    else:
        res['pag'] = {
            'hilo': pag.hilo.id, 'titulo': pag.titulo, 
            'contenido': pag.contenido, 'imagenes': pag.imagenes}
    #Action code ends here
    if 'nombre_usuario' in session:
        res['idUsuario'] = session['nombre_usuario']
    return json.dumps(res)

@ident.route('/ident/VRegistro')
def VRegistro():
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure


    #Action code ends here
    return json.dumps(res)

@ident.route('/ident/VInicio')
def VInicio():
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure


    #Action code ends here
    return json.dumps(res)



#Use case code starts here


#Use case code ends here
