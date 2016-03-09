from flask import Flask, session
from flask.ext.script import Manager, Server
from random import SystemRandom
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__, static_url_path='')
manager = Manager(app)
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0', port = 8080)
)

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=45)
    session.modified = True

@app.route('/')
def root():
    return app.send_static_file('index.html')

#Application code starts here

# Código para la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://synergy:lacontraseña@localhost/ci3715_db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

#-------------------------------------------------------------------------------

amigos = db.Table('amigos', db.metadata,
    db.Column('usuario_id',
        db.String,db.ForeignKey('usuario.nombre_usuario'),primary_key=True),
    db.Column('amigo_id',
        db.String,db.ForeignKey('usuario.nombre_usuario'),primary_key=True)
)

#------------------------------------------------------------------------------

class Usuario(db.Model):
    __tablename__ = "usuario"
    nombre_usuario = db.Column(db.String, primary_key=True)
    nombre_completo = db.Column(db.String)
    correo = db.Column(db.String)
    clave = db.Column(db.String)
    amigos = db.relationship("Usuario",
        secondary=amigos,
        primaryjoin=nombre_usuario==amigos.c.usuario_id,
        secondaryjoin=nombre_usuario==amigos.c.amigo_id)

    @staticmethod
    def hacer_amigos(usuario1, usuario2):
        usuario1.amigos.push(usuario2)
        usuario2.amigos.push(usuario1)

    def __init__(self, nombre_usuario, nombre_completo, correo, clave):
        self.nombre_usuario = nombre_usuario
        self.nombre_completo = nombre_completo
        self.clave = clave
        self.correo = correo
        self.amigos = []

    def __repr__(self):
        return "<Usuario(nombre completo='%s', nombre de usuario='%s', correo='%s', clave='%s'>" %(
            self.nombre_completo, self.nombre_usuario, self.correo, self.clave)

#-------------------------------------------------------------------------------

class Pagina(db.Model):
    titulo = db.Column(db.String)
    contenido = db.Column(db.Text)
    id_usuario = db.Column(db.String, db.ForeignKey('usuario.nombre_usuario'), primary_key=True)
    usuario = db.relationship('Usuario',
        backref=db.backref('pagina', uselist=False), uselist=False)

    def __init__(self, titulo, contenido, usuario):
        self.titulo = titulo
        self.contenido = contenido
        self.id_usuario = usuario
        self.usuario = (db.session
            .query(Usuario)
            .filter_by(nombre_usuario=usuario)
            .first())

#-------------------------------------------------------------------------------

class Chat(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mensajes = db.relationship('Mensaje',
        backref=db.backref('chat',uselist=False),
        order_by=lambda: desc(Mensaje.creado))
    # mensaje = db.relationship('Mensaje',
    # backref=db.backref('chat', uselist=False) )


#-------------------------------------------------------------------------------

class Mensaje(db.Model):

    id = db.Column (db.Integer, primary_key=True, autoincrement=True)
    chat_id =  db.Column(db.Integer, db.ForeignKey('chat.id'))
    contenido = db.Column(db.Text)
    creado = db.Column(db.DateTime, server_default=db.func.now())
    usuario_origen = db.Column(db.String, db.ForeignKey('usuario.nombre_usuario'))

    # usuario_destino = db.relationship('Usuario', secondary=Usuario_destino,
    #     backref=db.backref('usuario_destino', lazy='dynamic'))

    def __init__(self,usuario_origen,contenido,chat):
        self.usuario_origen = usuario_origen.nombre_usuario
        self.chat_id = chat.id
        self.chat = chat
        self.contenido = contenido

#-------------------------------------------------------------------------------

miembrosGrupo = db.Table('miembrosGrupo', db.metadata,
    db.Column('grupo',db.String,db.ForeignKey('grupo.nombre')),
    db.Column('usuario',db.String,db.ForeignKey('usuario.nombre_usuario'))
)

class Grupo(db.Model):
    __tablename__ = 'grupo'
    nombre = db.Column(db.String, primary_key = True)  # Como se llama este id por defecto?
    id_admin = db.Column(db.String, db.ForeignKey('usuario.nombre_usuario'))
    admin = db.relationship('Usuario',
            backref=db.backref('admin_grupo'), uselist=False)
    miembros = db.relationship('Usuario',
               secondary=miembrosGrupo, # Hace que usen la tabla miembrosGrupo
               backref=db.backref('grupos'))
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    chat = db.relationship('Chat', uselist=False)

    def __init__(self,nombre,admin,chat):        # es de muchos a muchos
        self.nombre = nombre
        self.admin = admin
        self.admin_id = admin.nombre_usuario
        self.chat_id = chat.id
        self.chat = chat



"""
u1 = Usuario('samuel','Samuel Arleo','s@c.com','saar1312')
u2 = Usuario('alejandra','Alejandra C','s@c.com','alejandra')
u3 = Usuario('pedro','Pedro Perez','s@c.com','pedro')

db.session.add(u1)
db.session.add(u2)
db.session.add(u3)
db.session.commit()

#users = Usuario.query.all()
admin = Usuario.query.filter_by(nombre_usuario='alejandra').first()
admin2 = Usuario.query.filter_by(nombre_usuario='samuel').first()

g1 = Grupo('Mango',admin)
g2 = Grupo('Synergy',admin2)
db.session.add(g1)
db.session.add(g2)
db.session.commit()

mango = Grupo.query.filter_by(nombre='Mango').first()
synergy = Grupo.query.filter_by(nombre='Synergy').first()

alej = Usuario.query.filter_by(nombre_usuario='alejandra').first()
samuel = Usuario.query.filter_by(nombre_usuario='samuel').first()

mango.miembros.append(alej)
mango.miembros.append(samuel)
synergy.miembros.append(samuel)
db.session.commit()

"""

#-------------------------------------------------------------------------------

#Application code ends here

from app.socal.ident import ident
app.register_blueprint(ident)
from app.socal.paginas import paginas
app.register_blueprint(paginas)

from app.socal.chat import chat
app.register_blueprint(chat)


if __name__ == '__main__':
    app.config.update(
      SECRET_KEY = repr(SystemRandom().random())
    )
    manager.run()
