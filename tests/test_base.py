#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import base
from flask import Flask, json, current_app, session, request




class BaseTestCase(unittest.TestCase):

    def setUp(self):
        
        
        self.app = base.app.test_client()
        self.app.testing = True
        self.db = base.db
        
        usuarioExistente_john = base.Usuario.query.filter_by(nombre_usuario=\
                                    "johngalt").first()

        if not(usuarioExistente_john):
            nuevo_usuario_john = base.Usuario(nombre_completo='johngalt'
                                ,nombre_usuario='johngalt'
                                ,clave='johngalt'
                                ,correo='john@gmail.com')
            
            self.db.session.add(nuevo_usuario_john)
            
            self.db.session.commit()
            
        usuarioExistente_RL = base.Usuario.query.filter_by(nombre_usuario=\
                                    "RL").first()
        
        if not(usuarioExistente_RL):
            nuevo_usuario_RL = base.Usuario(nombre_completo='RL Mayer'
                                ,nombre_usuario='RL'
                                ,clave='rlmayerrlmayer'
                                ,correo='RL@gmail.com')
            
            self.db.session.add(nuevo_usuario_RL)
            
            self.db.session.commit()
            
        
        amistad = base.Amigo.query.filter_by(amigo1=\
                                    "RL").first()
        
        if not(amistad):
            
            nuevo_chat = base.Chat()
            self.db.session.add(nuevo_chat)
            self.db.session.commit()
            self.amigos1 = base.Amigo("johngalt","RL",nuevo_chat.id)
            self.amigos2 = base.Amigo("RL","johngalt",nuevo_chat.id)
            
            self.db.session.add(self.amigos1)
            self.db.session.add(self.amigos2)
            self.db.session.commit()
    
    
    
    
    def tearDown(self):
        pass
    
    
    def test_app_exists(self):
        self.assertFalse(current_app is None)
    
    
    def test_app_is_testing(self):
        with base.app.app_context():
            self.assertTrue(current_app.config['TESTING'])
    
    
    
    def test_1VLogin(self):
        result = self.app.get('/ident/VLogin')
        self.assertEqual(result.status_code, 200)
    
    
    def test_2AIdentificar(self):
        #result = self.app.post('/ident/AIdentificar',data=dict(usuario='johngalt',clave='johngalt'),follow_redirects=True)
        #self.assertTrue(result.status_code == 302)
        res = self.app.post('/ident/AIdentificar', data=json.dumps({
            'usuario': 'johngalt',
            'clave': 'johngalt'
        }), content_type='application/json;charset=utf-8', follow_redirects=True)
        print(res.status_code)
        self.assertTrue(res.status_code == 200)
        self.assertTrue(bytes('/VPrincipal', 'UTF-8') in res.data) # True si esta registrado
    
    
    def test_3ARegistrar(self):
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
    
    
    
    def test_4VPrincipal(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'franc'
            res = contexto.get('/ident/VPrincipal')
        self.assertEqual(res.status_code,200)
    
    
    def test_5APagina_no_tiene(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'franc'
            res = contexto.get('paginas/APagina?idPagina=franc')
        self.assertEqual(res.status_code,200)
        self.assertTrue(bytes('/VPagina', 'UTF-8') in res.data) #True si usuario no tiene pagina
    
    
    def test_6APagina_si_tiene(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
            res = contexto.get('paginas/APagina?idPagina=johngalt')
        self.assertEqual(res.status_code,200)
        self.assertTrue(bytes('/VMiPagina', 'UTF-8') in res.data) #True si usuario tiene pagina
    
    
    def test_7AModificarPagina(self):
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
    
    
    def test_8VMiPagina(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
            res = contexto.get('/paginas/VMiPagina?idUsuario=johngalt')
        self.assertEqual(res.status_code,200) # True si tiene si usuario tiene pagina
    
    
    def test_9VContactos(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
            res = contexto.get('/chat/VContactos?idUsuario=johngalt')
        self.assertEqual(res.status_code,200) # True si tiene si usuario tiene contactos
        self.assertTrue(bytes('data1', 'UTF-8') in res.data)
    
    
    
    def test_10VAdminContactos(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
            res = contexto.get('/chat/VAdminContactos?idUsuario=johngalt')
        self.assertEqual(res.status_code,200) # True si tiene si usuario tiene contactos
        self.assertTrue(bytes('data1', 'UTF-8') in res.data)
    
    
    def test_11AgregContacto(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
    
            res = self.app.post('/chat/AgregContacto', data=json.dumps({
                'nombre': 'RL',
                'opcionesNombre': 'RL'
            }), content_type='application/json;charset=utf-8', follow_redirects=True)
    
            self.assertTrue(bytes('/VAdminContactos', 'UTF-8') in res.data)
            self.assertTrue(bytes('Contacto agregado', 'UTF-8') in res.data) # True si contacto existe
    
    #Esta en el API, pero bueno...
    """
    #def test_AgregContacto_no_existe(self):
    #    with self.app as contexto:
    #        with contexto.session_transaction() as sesion_actual:
    #            sesion_actual['nombre_usuario'] = 'johngalt'
    #
    #        res = self.app.post('/chat/AgregContacto', data=json.dumps({
    #            'nombre': 'no existo',
    #            'opcionesNombre': 'no_existo'
    #        }), content_type='application/json;charset=utf-8', follow_redirects=True)
    #
    #        self.assertTrue(bytes('/VAdminContactos', 'UTF-8') in res.data)
    #        self.assertTrue(bytes('No se pudo agregar contacto', 'UTF-8') in res.data) # True si contacto existe
    """
    
    def test_12AElimContacto(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
            res = contexto.get('/chat/AElimContacto?id=RL')
        self.assertEqual(res.status_code,200)
        self.assertTrue(bytes('/VAdminContactos', 'UTF-8') in res.data)
        self.assertTrue(bytes('Contacto eliminado', 'UTF-8') in res.data) # True si tiene si usuario tenia contacto
    
    #Esta en el API, pero no puede ocurrir y por ahora no se prueba
    """
    #def test_AElimContacto_no_existe(self):
    #    with self.app as contexto:
    #        with contexto.session_transaction() as sesion_actual:
    #            sesion_actual['nombre_usuario'] = 'johngalt'
    #        res = contexto.get('/chat/AElimContacto?id=no_existo')
    #    self.assertEqual(res.status_code,200)
    #    self.assertTrue(bytes('/VAdminContactos', 'UTF-8') in res.data)
    #    self.assertTrue(bytes('No se pudo eliminar contacto', 'UTF-8') in res.data) # True si tiene si usuario no tenia contacto
    """
    
    """
    #def test_AEscribir(self):
    #    with self.app as contexto:
    #        with contexto.session_transaction() as sesion_actual:
    #            sesion_actual['nombre_usuario'] = 'johngalt'
    #            sesion_actual['amigo'] = 'RL'
    #            sesion_actual['idChat'] = base.Amigo.query.filter_by(amigo1='johngalt').first().chat_id
    #
    #        res = self.app.post('/chat/AEscribir', data=json.dumps({
    #            'texto': 'HOLA HOLA'
    #        }), content_type='application/json;charset=utf-8', follow_redirects=True)
    #
    #        self.assertTrue(bytes('/VChat', 'UTF-8') in res.data)
    #        self.assertTrue(bytes('Enviado', 'UTF-8') in res.data)
    #        self.assertTrue(base.Mensaje.query.filter_by(contenido='HOLA HOLA' #True si se guarda en la base de datos
    #                                                    , usuario_origen='johngalt').first() is not None)
    
    """
    #Esta en el API
    """
    #def test_AEscribir_falla(self)
    #    with self.app as contexto:
    #        with contexto.session_transaction() as sesion_actual:
    #            sesion_actual['nombre_usuario'] = 'johngalt'
    #            sesion_actual['amigo'] = 'no_existo'
    #        res = self.app.post('/chat/AEscribir', data=json.dumps({
    #            'texto': 'HOLA HOLA HOLA'
    #        }), content_type='application/json;charset=utf-8', follow_redirects=True)
    #
    #        self.assertTrue(bytes('/VChat', 'UTF-8') in res.data)
    #        self.assertTrue(bytes('No se pudo enviar mensaje', 'UTF-8') in res.data) #True si el amigo no existe
    """
    
    def test_13AgregGrupo(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
            res = contexto.get('/chat/AgregGrupo')
        self.assertEqual(res.status_code,200) # True si puede ver el grupo
        self.assertTrue(bytes('Grupo agregado', 'UTF-8') in res.data)
    
    
    def test_14VGrupo(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
                id_grupo = base.Usuario.query.filter_by(nombre_usuario="johngalt").first().grupos.filter(True).first().id
                sesion_actual['idGrupo'] = id_grupo
            res = contexto.get('/chat/VGrupo?idGrupo='+str(id_grupo))
        self.assertEqual(res.status_code,200) # True si puede ver el grupo este usuario
        self.assertTrue(bytes('johngalt', 'UTF-8') in res.data)
    
    
    
    def test_15ASalirGrupo(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
                id_grupo = base.Usuario.query.filter_by(nombre_usuario="johngalt").first().grupos.filter(True).first().id
                sesion_actual['idGrupo'] = id_grupo
            res = contexto.get('/chat/ASalirGrupo?idGrupo='+str(id_grupo))
        self.assertEqual(res.status_code,200)
        self.assertTrue(bytes('/VAdminContactos', 'UTF-8') in res.data)
        #self.assertTrue(bytes('Ya no estás en ese grupo', 'UTF-8') in res.data) # True si el usuario se elimina
    
    
    
    def test_16AgregMiembro(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
                sesion_actual['amigo'] = 'RL'
                id_grupo = base.Usuario.query.filter_by(nombre_usuario="johngalt").first().grupos.filter(True).first().id
                sesion_actual['idGrupo'] = str(id_grupo)
            res = self.app.post('/chat/AgregMiembro', data=json.dumps({
                'nombre': 'RL',
                'opcionesNombre':'RL'
    
            }), content_type='application/json;charset=utf-8', follow_redirects=True)
    
            self.assertTrue(bytes('/VGrupo', 'UTF-8') in res.data)
            self.assertTrue(bytes('Nuevo miembro agregado', 'UTF-8') in res.data)
            #self.assertTrue(base.Grupo.miembrosGrupo.query.filter_by(nombre_usuario="johngalt").first() is not None) #True si se agrega
    
    
    def test_17AgregGrupo(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
            res = contexto.get('/chat/AgregGrupo')
        self.assertEqual(res.status_code,200) # True si puede ver el grupo
        self.assertTrue(bytes('Grupo agregado', 'UTF-8') in res.data)
    
    
    def test_18VForo(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
                id_foro = base.Foro.query.filter_by(autor_id="johngalt").first().titulo
            res = contexto.get('/foro/VForo?idForo='+str(id_foro))
        self.assertEqual(res.status_code,200) # True si puede ver el foro de este usuario
        
    
    def test_19VForos(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
            res = contexto.get('/foro/VForos')
        self.assertEqual(res.status_code,200) # True si puede ver los foros
     
     
    def test_20AgregForo(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
                numero_foros = len(base.Foro.query.filter_by(autor_id="johngalt").all())
                nombre_foro = "johngalt nuevo foro "+str(numero_foros)
            res = self.app.post('/foro/AgregForo', data=json.dumps({
                'texto': nombre_foro
            }), content_type='application/json;charset=utf-8', follow_redirects=True)

            self.assertTrue(bytes('/VForos', 'UTF-8') in res.data)
            self.assertTrue(bytes('Foro Agregado', 'UTF-8') in res.data)
            
    
    def test_21AgregHilo(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
                numero_foros = len(base.Foro.query.filter_by(autor_id="johngalt").all())
                nombre_foro = "johngalt nuevo foro "+str(numero_foros-1)
                sesion_actual['idForo'] = nombre_foro
            res = self.app.post('/foro/AgregHilo', data=json.dumps({
                'titulo': "Hilo",
                'contenido':"HOLA HILO"
            }), content_type='application/json;charset=utf-8', follow_redirects=True)
            
            self.assertTrue(bytes('/VForo', 'UTF-8') in res.data)
            self.assertTrue(bytes('Hilo Agregado', 'UTF-8') in res.data)
            
    
    def test_22VHilos(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
                numero_foros = len(base.Foro.query.filter_by(autor_id="johngalt").all())
                nombre_foro = "johngalt nuevo foro "+str(numero_foros-1)
                sesion_actual['idForo'] = nombre_foro
                id_hilo = base.Hilo.query.filter_by(foro_id=nombre_foro).first().id
            res = contexto.get('/foro/VHilos?idHilo='+str(id_hilo))
        self.assertEqual(res.status_code,200) # True si puede ver los foros
        self.assertTrue(bytes(nombre_foro, 'UTF-8') in res.data)
    
    
    def test_23AgregPublicacion(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
                numero_foros = len(base.Foro.query.filter_by(autor_id="johngalt").all())
                nombre_foro = "johngalt nuevo foro "+str(numero_foros-1)
                sesion_actual['idForo'] = nombre_foro
                hilo_actual = base.Hilo.query.filter_by(foro_id=nombre_foro).first()
                datos_pub_raiz = hilo_actual.raiz.a_diccionario()
            res = self.app.post('/foro/AgregPublicacion', data=json.dumps({
                'id':datos_pub_raiz['id'],
                'titulo': "Hilo",
                'contenido':"HOLA HILO"
            }), content_type='application/json;charset=utf-8', follow_redirects=True)
            
            self.assertTrue(bytes('/VHilos', 'UTF-8') in res.data)
            self.assertTrue(bytes('Respuesta enviada', 'UTF-8') in res.data)
    
    
    def test_24AElimPublicacion(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
                numero_foros = len(base.Foro.query.filter_by(autor_id="johngalt").all())
                nombre_foro = "johngalt nuevo foro "+str(numero_foros-1)
                sesion_actual['idForo'] = nombre_foro
                hilo_actual = base.Hilo.query.filter_by(foro_id=nombre_foro).first()
                datos_pub_raiz = hilo_actual.raiz.a_diccionario()
            res = contexto.get('/foro/AElimPublicacion?idPublicacion='+str(datos_pub_raiz['id']))
        self.assertEqual(res.status_code,200) # True si puede eliminar el foro de este usuario
        self.assertTrue(bytes('Publicacion eliminada', 'UTF-8') in res.data)
    
    
    def test_26AElimHiloMal(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'RL'
                numero_foros = len(base.Foro.query.filter_by(autor_id="johngalt").all())
                nombre_foro = "johngalt nuevo foro "+str(numero_foros-1)
                sesion_actual['idForo'] = nombre_foro
                id_hilo = base.Hilo.query.filter_by(foro_id=nombre_foro).first().id
            res = contexto.get('/foro/AElimHilo?idHilo='+str(id_hilo))
        self.assertEqual(res.status_code,200)
        self.assertTrue(bytes('No se pudo eliminar el hilo', 'UTF-8') in res.data)
    
    
    def test_27AElimHilo(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
                numero_foros = len(base.Foro.query.filter_by(autor_id="johngalt").all())
                nombre_foro = "johngalt nuevo foro "+str(numero_foros-1)
                sesion_actual['idForo'] = nombre_foro
                id_hilo = base.Hilo.query.filter_by(foro_id=nombre_foro).first().id
            res = contexto.get('/foro/AElimHilo?idHilo='+str(id_hilo))
        self.assertEqual(res.status_code,200) # True si puede eliminar el foro de este usuario
        self.assertTrue(bytes('Hilo eliminado', 'UTF-8') in res.data)
        
    
    def test_28AElimHiloForoMal(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'RL'
                numero_foros = len(base.Foro.query.filter_by(autor_id="johngalt").all())
                nombre_foro = "johngalt nuevo foro "+str(numero_foros-1)
            res = contexto.get('/foro/AElimForo?idForo='+nombre_foro)
        self.assertEqual(res.status_code,200) # True si puede eliminar el foro de este usuario
        self.assertTrue(bytes('No se pudo eliminar el foro', 'UTF-8') in res.data)
    
    def test_20AgregForo(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
                numero_foros = len(base.Foro.query.filter_by(autor_id="johngalt").all())
                nombre_foro = "johngalt nuevo foro "+str(numero_foros-1)
            res = self.app.post('/foro/AgregForo', data=json.dumps({
                'texto': nombre_foro
            }), content_type='application/json;charset=utf-8', follow_redirects=True)

            self.assertTrue(bytes('/VForos', 'UTF-8') in res.data)
            self.assertTrue(bytes('No se pudo agregar el nuevo foro', 'UTF-8') in res.data)
            
    
    
    def test_29AElimHiloForo(self):
        with self.app as contexto:
            with contexto.session_transaction() as sesion_actual:
                sesion_actual['nombre_usuario'] = 'johngalt'
                numero_foros = len(base.Foro.query.filter_by(autor_id="johngalt").all())
                nombre_foro = "johngalt nuevo foro "+str(numero_foros-1)
            res = contexto.get('/foro/AElimForo?idForo='+nombre_foro)
        self.assertEqual(res.status_code,200) # True si puede eliminar el foro de este usuario
        self.assertTrue(bytes('Foro eliminado', 'UTF-8') in res.data)
    
    
    
    
    
    

if __name__ == '__main__':
    unittest.main()
