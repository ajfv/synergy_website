from flask import request, session, Blueprint, json

##############################################################
#   Codigo para la base de datos del usuario                 #
##############################################################
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker

from app.socal.ident import Usuario

engine = create_engine('sqlite:///base_de_datos.db', echo=True)
Base_dec = declarative_base()

class Pagina(Base_dec):
    
    __tablename__ = "Pagina"
    
    titulo = Column(String)
    contenido = Column(String)
    id_usuario = Column(String, primary_key=True)


Base_dec.metadata.create_all(engine)
Sesion = sessionmaker(bind=engine)
##############################################################

paginas = Blueprint('paginas', __name__)


@paginas.route('/paginas/AModificarPagina', methods=['POST'])
def AModificarPagina():
    #POST/PUT parameters
    params = request.get_json()
    results = [{'label':'/VPagina', 'msg':['Cambios almacenados']}, ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message

    res['label'] = res['label'] + '/' + session['nombre_usuario']

    print(session['nombre_usuario'])
    nueva_sesion = Sesion()

    pagina_ya_existe = False

    for titulo,id_usuario in nueva_sesion.query(Pagina.titulo, Pagina.id_usuario) :
        if id_usuario == session['nombre_usuario'] :
            
            pagina_existente = nueva_sesion.query(Pagina).filter_by(id_usuario=session['nombre_usuario']).first()
            
            if 'contenido' in params :
                pagina_existente.contenido = params['contenido']
            else :
                pagina_existente.contenido = ""
            
            pagina_existente.titulo = params['titulo']
            pagina_ya_existe = True
            break

    if not pagina_ya_existe :
        nueva_pagina = Pagina(titulo=params['titulo'], contenido=params['contenido'], id_usuario=session['nombre_usuario'])
    
        nueva_sesion.add(nueva_pagina)
    
    nueva_sesion.commit()

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
    
    nueva_sesion = Sesion()
    
    pagina_existente = nueva_sesion.query(Pagina).filter_by(id_usuario=idUsuario).first()
    
    #res={'titulo':pagina_existente.titulo,'contenido':pagina_existente.contenido}
    
    #return pagina_existente.contenido

    #Action code ends here
    return json.dumps(res)





#Use case code starts here


#Use case code ends here

