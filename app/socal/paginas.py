from flask import request, session, Blueprint, json

paginas = Blueprint('paginas', __name__)
from base import Usuario, Pagina, db

@paginas.route('/paginas/AModificarPagina', methods=['POST'])
def AModificarPagina():
    #POST/PUT parameters
    params = request.get_json()
    results = [{'label':'/VPagina', 'msg':['Cambios almacenados']}, ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message

    res['label'] = res['label'] + '/' + db.session['nombre_usuario']

    pagina = (db.session.query(Pagina)
        .filter_by(id_usuario=db.session['nombre_usuario'])
        .first())
    if pagina is None:
        pagina = Pagina(titulo=params['titulo'],
            contenido=params['contenido'],
            id_usuario=session['nombre_usuario'])
        db.session.add(pagina)
    else:
        pagina.titulo = params['titulo']
        pagina.contenido = "" if 'contenido' not in params else params['contenido']

    db.session.commit()

    #Action code ends here
    if "actor" in res:
        if res['actor'] is None:
            session.pop("actor", None)
        else:
            session['actor'] = res['actor']
    return json.dumps(res)



@paginas.route('/paginas/VPagina')
def VPagina():
    #GET parameter
    idUsuario = request.args['idUsuario']
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure

    pagina_existente = db.session.query(Pagina).filter_by(id_usuario=idUsuario).first()

    #res={'titulo':pagina_existente.titulo,'contenido':pagina_existente.contenido}

    #return pagina_existente.contenido

    #Action code ends here
    return json.dumps(res)





#Use case code starts here


#Use case code ends here
