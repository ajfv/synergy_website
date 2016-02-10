from flask import request, session, Blueprint, json

##############################################################
#   Codigo para la base de datos del usuario                 #
##############################################################
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///base_de_datos.db', echo=True)
Base_dec = declarative_base()

class Usuario(Base_dec):
    
    __tablename__ = "Usuario"
    
    clave = Column(String)
    nombre_completo = Column(String)
    correo = Column(String)
    nombre_usuario = Column(String, primary_key=True)
    
    def __repr__(self):
        return "< Usuario(nombre completo='%s', nombre de usuario='%s',correo='%s',clave='%s')>" %(self.nombre_completo, self.nombre_usuario, self.correo, self.clave)

Base_dec.metadata.create_all(engine)
Sesion = sessionmaker(bind=engine)
##############################################################


ident = Blueprint('ident', __name__)

@ident.route('/ident/AIdentificar', methods=['POST'])
def AIdentificar():
    #POST/PUT parameters
    params = request.get_json()
    results = [{'label':'/VPrincipal', 'msg':['Bienvenido usuario'], "actor":"duenoProducto"}, {'label':'/VLogin', 'msg':['Datos de identificación incorrectos']}, ]
    res = results[1] #Estaba en 0
    #Action code goes here, res should be a list with a label and a message

    nueva_sesion = Sesion()
    
    for nombre_usuario, clave in nueva_sesion.query(Usuario.nombre_usuario, Usuario.clave) :
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



@ident.route('/ident/ARegistrar', methods=['POST'])
def ARegistrar():
    #POST/PUT parameters
    params = request.get_json()
    results = [{'label':'/VLogin', 'msg':['Felicitaciones, Ya estás registrado en la aplicación']}, {'label':'/VRegistro', 'msg':['Error al tratar de registrarse']}, ]
    res = results[0]
    #Action code goes here, res should be a list with a label and a message
    
    nuevo_usuario = Usuario(nombre_completo=params['nombre']
                            ,nombre_usuario=params['usuario']
                            ,clave=params['clave']
                            ,correo=params['correo'])
    
    nueva_sesion = Sesion()
    
    nueva_sesion.add(nuevo_usuario)
    
    nueva_sesion.commit()
    
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

    #session.pop('nombre_usuario')
    
    #Action code ends here
    return json.dumps(res)



@ident.route('/ident/VPrincipal')
def VPrincipal():
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure

    res['idUsuario'] = session['nombre_usuario']
    
    #print("En VPrincipal ")
    #print(session)
    
    #Action code ends here
    return json.dumps(res)



@ident.route('/ident/VRegistro')
def VRegistro():
    res = {}
    if "actor" in session:
        res['actor']=session['actor']
    #Action code goes here, res should be a JSON structure

    #print("En VRegistro ")
    #print(session)
    
    #Action code ends here
    return json.dumps(res)





#Use case code starts here


#Use case code ends here

