import unittest
import base
from flask import Flask, json, current_app, session, request




class BaseTestCase(unittest.TestCase):
    
    def setUp(self):
        
        #self.app = create_app('testing')
        #self.app_context = self.app.app_context()
        #self.app_context.push()
        #base.app.config['SECRET_KEY'] = 'sekrit!'
        self.app = base.app.test_client()
        self.app.testing = True
        self.db = base.db
        #manager.run()
        
    
    def tearDown(self):
        pass
        
    
    def test_app_exists(self):
        self.assertFalse(current_app is None)
    
    
    def test_app_is_testing(self):
        with base.app.app_context():
            self.assertTrue(current_app.config['TESTING'])
    
    
    
    def test_VLogin(self):
        result = self.app.get('/ident/VLogin') 
        self.assertEqual(result.status_code, 200)
    
    
    def test_AIdentificar(self):
        #result = self.app.post('/ident/AIdentificar',data=dict(usuario='johngalt',clave='johngalt'),follow_redirects=True)
        #self.assertTrue(result.status_code == 302)
        res = self.app.post('/ident/AIdentificar', data=json.dumps({
            'usuario': 'johngalt',
            'clave': 'johngalt'
        }), content_type='application/json;charset=utf-8', follow_redirects=True)
        print(res.status_code)
        self.assertTrue(res.status_code == 200)
        self.assertTrue(bytes('/VPrincipal', 'UTF-8') in res.data) # True si esta registrado
    
    
    def test_ARegistrar(self):
        res = self.app.post('/ident/ARegistrar', data=json.dumps({
            'nombre':'Francisco Danconia',
            'usuario': 'franc',
            'clave': 'franciscodanconia',
            'correo':'franc@gmail.com'
        }), content_type='application/json;charset=utf-8', follow_redirects=True)
        print(res.status_code)
        self.assertTrue(res.status_code == 200)
        self.assertTrue(base.Usuario.query.filter_by(nombre_usuario='franc').first() is not None)
        
        self.assertTrue(bytes('/VRegistro', 'UTF-8') in res.data) #Si ya esta registrado, assert true, sino false
        self.assertTrue(bytes('Error al tratar de registrarse', 'UTF-8') in res.data)
    
      
    
    def test_VPrincipal(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'franc'
            res = contexto.get('/ident/VPrincipal')
        self.assertEqual(res.status_code,200) 
    
    
    def test_APagina_no_tiene(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'franc'
            res = contexto.get('paginas/APagina?idPagina=franc')
        self.assertEqual(res.status_code,200)
        self.assertTrue(bytes('/VPagina', 'UTF-8') in res.data) #True si usuario no tiene pagina


    def test_APagina_si_tiene(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
            res = contexto.get('paginas/APagina?idPagina=johngalt')
        self.assertEqual(res.status_code,200)
        self.assertTrue(bytes('/VMiPagina', 'UTF-8') in res.data) #True si usuario tiene pagina
        
    
    def test_AModificarPagina(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
            
            res = self.app.post('/paginas/AModificarPagina', data=json.dumps({
                'titulo': 'pagina de johngalt',
                'contenido': '<p>HOLA HOLA<p>'
            }), content_type='application/json;charset=utf-8', follow_redirects=True)
        
        self.assertTrue(res.status_code == 200)
        self.assertTrue(base.Pagina.query.filter_by(id_usuario='johngalt').first() is not None) #True si tiene pagina
        self.assertTrue(bytes('Cambios almacenados', 'UTF-8') in res.data)
    
    
    def test_VMiPagina(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
            res = contexto.get('/paginas/VMiPagina?idUsuario=johngalt')
        self.assertEqual(res.status_code,200) # True si tiene si usuario tiene pagina
    
    
    def test_VContactos(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
            res = contexto.get('/chat/VContactos?idUsuario=johngalt')
        self.assertEqual(res.status_code,200) # True si tiene si usuario tiene contactos
        self.assertTrue(bytes('data1', 'UTF-8') in res.data)
    
    
    
    def test_VAdminContactos(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
            res = contexto.get('/chat/VAdminContactos?idUsuario=johngalt')
        self.assertEqual(res.status_code,200) # True si tiene si usuario tiene contactos
        self.assertTrue(bytes('data1', 'UTF-8') in res.data)
    
    
    def test_AgregContacto(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
            
            res = self.app.post('/chat/AgregContacto', data=json.dumps({
                'nombre': 'algo',
                'opcionesNombre': 'algo'
            }), content_type='application/json;charset=utf-8', follow_redirects=True)
            
            self.assertTrue(bytes('/VAdminContactos', 'UTF-8') in res.data) 
            self.assertTrue(bytes('Contacto agregado', 'UTF-8') in res.data) # True si contacto existe
    
    #Esta en el API, pero bueno...
    """
    def test_AgregContacto_no_existe(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
            
            res = self.app.post('/chat/AgregContacto', data=json.dumps({
                'nombre': 'no existo',
                'opcionesNombre': 'no_existo'
            }), content_type='application/json;charset=utf-8', follow_redirects=True)
            
            self.assertTrue(bytes('/VAdminContactos', 'UTF-8') in res.data) 
            self.assertTrue(bytes('No se pudo agregar contacto', 'UTF-8') in res.data) # True si contacto existe
    """
    
    def test_AElimContacto(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
            res = contexto.get('/chat/AElimContacto?id=algo')
        self.assertEqual(res.status_code,200) 
        self.assertTrue(bytes('/VAdminContactos', 'UTF-8') in res.data)
        self.assertTrue(bytes('Contacto eliminado', 'UTF-8') in res.data) # True si tiene si usuario tenia contacto
    
    #Esta en el API, pero bueno...
    """
    def test_AElimContacto_no_existe(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
            res = contexto.get('/chat/AElimContacto?id=no_existo')
        self.assertEqual(res.status_code,200)
        self.assertTrue(bytes('/VAdminContactos', 'UTF-8') in res.data)
        self.assertTrue(bytes('No se pudo eliminar contacto', 'UTF-8') in res.data) # True si tiene si usuario no tenia contacto
    """
    
    
    def test_AEscribir(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
                sesion_actual['amigo'] = 'algo'
            res = self.app.post('/chat/AEscribir', data=json.dumps({
                'texto': 'HOLA HOLA'
            }), content_type='application/json;charset=utf-8', follow_redirects=True)
            
            self.assertTrue(bytes('/VChat', 'UTF-8') in res.data) 
            self.assertTrue(bytes('Enviado', 'UTF-8') in res.data)
            self.assertTrue(base.Mensaje.query.filter_by(contenido='HOLA HOLA' #True si se guarda en la base de datos
                                                        , usuario_origen='johngalt').first() is not None)
    
    
    #Esta en el API       
    """  
    def test_AEscribir_falla(self)
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
                sesion_actual['amigo'] = 'no_existo'
            res = self.app.post('/chat/AEscribir', data=json.dumps({
                'texto': 'HOLA HOLA HOLA'
            }), content_type='application/json;charset=utf-8', follow_redirects=True)
            
            self.assertTrue(bytes('/VChat', 'UTF-8') in res.data) 
            self.assertTrue(bytes('No se pudo enviar mensaje', 'UTF-8') in res.data) #True si el amigo no existe
    """
    
    def test_ASalirGrupo(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
            res = contexto.get('/chat/ASalirGrupo?idUsuario=johngalt')
        self.assertEqual(res.status_code,200)
        self.assertTrue(bytes('/VAdminContactos', 'UTF-8') in res.data)
        self.assertTrue(bytes('Ya no estás en ese grupo', 'UTF-8') in res.data) # True si el usuario se elimina
    
    
    
if __name__ == '__main__':
    unittest.main()
