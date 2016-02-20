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

class Usuario(db.Model):
    nombre_usuario = db.Column(db.String, primary_key=True)
    nombre_completo = db.Column(db.String)
    correo = db.Column(db.String)
    clave = db.Column(db.String)

    def __init__(self, nombre_usuario, nombre_completo, correo, clave):
        self.nombre_usuario = nombre_usuario
        self.nombre_completo = nombre_completo
        self.clave = clave
        self.correo = correo

    def __repr__(self):
        return "<Usuario(nombre completo='%s', nombre de usuario='%s', correo='%s', clave='%s'>" %(
            self.nombre_completo, self.nombre_usuario, self.correo, self.clave)

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

#Application code ends here

from app.socal.ident import ident
app.register_blueprint(ident)
from app.socal.paginas import paginas
app.register_blueprint(paginas)


if __name__ == '__main__':
    app.config.update(
      SECRET_KEY = repr(SystemRandom().random())
    )
    manager.run()
