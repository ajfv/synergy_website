# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class PruebasIniSesion(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "localhost:8080"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_pruebas_ini_sesion(self):
        driver = self.driver
        driver.get(self.base_url + "/#/VLogin")
        actions = ActionChains(self.driver)
        alert = Alert(self.driver)
        
        driver.find_element_by_id("fLogin_usuario").clear()
        driver.find_element_by_id("fLogin_usuario").send_keys("Usuario")
        time.sleep(.5)
        driver.find_element_by_id("fLogin_clave").clear()
        driver.find_element_by_id("fLogin_clave").send_keys("aaaaaaaa")
        time.sleep(.5)
        driver.find_element_by_xpath("//button[@id='conectate']").click()
        time.sleep(2)
        
######################## Ayuda y Foro sin titulo #############################################   
      
        driver.find_element_by_xpath("//a[@ng-click='VForos()']").click()
        time.sleep(2)
        driver.find_element_by_xpath("//a[@id='config']").click()
        time.sleep(.5)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(1)
        
        '''
        driver.find_element_by_xpath("//span[@ng-bind='idUsuario']").click()
        time.sleep(.5)
        driver.find_element_by_xpath("//a[@ng-click='__ayuda()']").click()
        time.sleep(1)
        
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        '''
######################## Creacion de Foro #############################################         
        
        driver.find_element_by_id("fForo_texto").send_keys("Foro Prueba")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(1)
        
        
######################## Prueba Foro con mismo nombre #############################################         
        '''
        driver.find_element_by_xpath("//button[@id='config']").click()
        time.sleep(.5)
        driver.find_element_by_id("fForo_texto").send_keys("Nuevo ForoR")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(1)
        
        actions.key_down(Keys.CONTROL)
        actions.send_keys('r')
        actions.key_up(Keys.CONTROL)
        actions.perform()
        time.sleep(.5)
        '''
######################## Hilo sin titulo ni contenido y ayuda ############################################# 
        
        driver.find_element_by_link_text("Foro Prueba").click()
        '''
        driver.find_element_by_xpath("//span[@ng-bind='idUsuario']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//a[@ng-click='__ayuda()']").click()
        time.sleep(1)
        '''
        actions.key_down(Keys.CONTROL)
        actions.send_keys('r')
        actions.key_up(Keys.CONTROL)
        actions.perform()
        time.sleep(.5)
        
        driver.find_element_by_xpath("//a[@id='config']").click()
        time.sleep(.5)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(1)
        '''
        driver.find_element_by_xpath("//span[@ng-bind='idUsuario']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//a[@ng-click='__ayuda()']").click()
        time.sleep(1)
        
        actions.key_down(Keys.CONTROL)
        actions.send_keys('r')
        actions.key_up(Keys.CONTROL)
        actions.perform()
        time.sleep(.5)
        '''
######################## Hilo sin titulo ############################################# 
        
        driver.find_element_by_xpath("//a[@id='config']").click()
        time.sleep(.5)
        driver.find_element_by_id("fHilo_contenido").clear()
        driver.find_element_by_id("fHilo_contenido").send_keys("Nuevo Contenido")
        time.sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(1)

######################## Hilo sin contenido ############################################# 
        
        driver.find_element_by_xpath("//a[@id='config']").click()
        time.sleep(.5)
        driver.find_element_by_id("fHilo_titulo").clear()
        driver.find_element_by_id("fHilo_titulo").send_keys("Nuevo Hilo")
        driver.find_element_by_id("fHilo_contenido").clear()
        time.sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(1)


######################## Creacion Hilo ############################################# 
        
        driver.find_element_by_xpath("//a[@id='config']").click()
        time.sleep(.5)
        driver.find_element_by_id("fHilo_titulo").clear()
        driver.find_element_by_id("fHilo_titulo").send_keys("Nuevo Hilo")
        driver.find_element_by_id("fHilo_contenido").clear()
        driver.find_element_by_id("fHilo_contenido").send_keys("Nuevo Contenido")
        time.sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(1)
        

######################## Creacion Hilo Existente ############################################# 
        '''
        driver.find_element_by_xpath("//a[@id='config']").click()
        time.sleep(.5)
        driver.find_element_by_id("fHilo_titulo").clear()
        driver.find_element_by_id("fHilo_titulo").send_keys("Nuevo Hilo")
        driver.find_element_by_id("fHilo_contenido").clear()
        driver.find_element_by_id("fHilo_contenido").send_keys("Nuevo Contenido")
        time.sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(1)
        '''
######################## Publicacion sin contenido y ayuda ############################################# 
        
        driver.find_element_by_link_text("Nuevo Hilo").click() 
        time.sleep(1)
        
        actions.key_down(Keys.CONTROL)
        actions.send_keys('r')
        actions.key_up(Keys.CONTROL)
        actions.perform()
        time.sleep(.5)
        
        driver.find_element_by_xpath("//button[@id='btnForos']").click()
        
        #driver.find_element_by_xpath("//span[@class='glyphicon glyphicon-info-sign']").click() ###### AYUDA #######################################
        time.sleep(1)
        

        
######################## Publicacion sin titulo ############################################# 
        
        driver.find_element_by_id("fpublicacion_titulo").clear()
        driver.find_element_by_id("fpublicacion_titulo").send_keys("")
        driver.find_element_by_id("fpublicacion_texto").clear()
        driver.find_element_by_id("fpublicacion_texto").send_keys("Nuevo Contenido")
        time.sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(1)
        
        
######################## Publicacion Vacia ############################################# 
        
        driver.find_element_by_id("fpublicacion_titulo").clear()
        driver.find_element_by_id("fpublicacion_titulo").send_keys("")
        time.sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(1)
        
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
######################## Crear Publicacion ############################################# 
        
        driver.find_element_by_id("fpublicacion_texto").clear()
        driver.find_element_by_id("fpublicacion_texto").send_keys("Nuevo Texto")
        time.sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(1)
        
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
        
######################## Publicacion nuevo titulo ############################################# 
        
        driver.find_element_by_id("fpublicacion_titulo").clear()
        driver.find_element_by_id("fpublicacion_titulo").send_keys("Nueva Titulo")
        driver.find_element_by_id("fpublicacion_texto").clear()
        driver.find_element_by_id("fpublicacion_texto").send_keys("Nuevo Comentario")
        time.sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(1)
        
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
        
######################## Publicacion "duplicada" ############################################# 
        
        driver.find_element_by_id("fpublicacion_titulo").clear()
        driver.find_element_by_id("fpublicacion_titulo").send_keys("Nueva Titulo")
        driver.find_element_by_id("fpublicacion_texto").clear()
        driver.find_element_by_id("fpublicacion_texto").send_keys("Nuevo Comentario")
        time.sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(1)
        
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
        
######################## Publicaciones Anidadas ############################################# 
        
        driver.find_element_by_xpath("(//a[@ng-click='responderPublicacion(publicacion)'])[2]").click()
        
        driver.find_element_by_xpath("(//textarea[@id='fpublicacion_texto'])[2]").clear()
        driver.find_element_by_xpath("(//textarea[@id='fpublicacion_texto'])[2]").send_keys("Nuevo Comentario 2")
        time.sleep(1)
        driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        time.sleep(1)
        
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
                
        driver.find_element_by_xpath("(//a[@ng-click='responderPublicacion(publicacion)'])[3]").click()
        
        driver.find_element_by_xpath("(//textarea[@id='fpublicacion_texto'])[2]").clear()
        driver.find_element_by_xpath("(//textarea[@id='fpublicacion_texto'])[2]").send_keys("Nuevo Comentario 3")
        time.sleep(1)
        driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        time.sleep(1)
        
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
        driver.find_element_by_xpath("(//a[@ng-click='responderPublicacion(publicacion)'])[2]").click()
        
        driver.find_element_by_xpath("(//textarea[@id='fpublicacion_texto'])[2]").clear()
        driver.find_element_by_xpath("(//textarea[@id='fpublicacion_texto'])[2]").send_keys("Nuevo Comentario 2.2")
        time.sleep(1)
        driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        time.sleep(1)
        
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
######################## Eliminar Publicaciones ############################################# 
        
        driver.find_element_by_xpath("(//a[@ng-click='AElimPublicacion1(publicacion.id)'])[3]").click()
        time.sleep(0.5)
        alert.accept()
        time.sleep(.5)   
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
        driver.find_element_by_xpath("(//a[@ng-click='AElimPublicacion1(publicacion.id)'])[2]").click()
        time.sleep(0.5)
        alert.accept()
        time.sleep(.5)
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
        driver.find_element_by_xpath("(//a[@ng-click='AElimPublicacion1(publicacion.id)'])[6]").click()
        time.sleep(0.5)
        alert.accept()
        time.sleep(.5)
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
        driver.find_element_by_xpath("(//a[@ng-click='AElimPublicacion1(publicacion.id)'])[5]").click()
        time.sleep(0.5)
        alert.accept()
        time.sleep(.5)       
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
        driver.find_element_by_xpath("(//a[@ng-click='AElimPublicacion1(publicacion.id)'])[4]").click()
        time.sleep(0.5)
        alert.accept()
        time.sleep(.5)
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
######################## Eliminar Hilos ############################################# 
        actions.send_keys(Keys.ALT)
        actions.send_keys(Keys.ARROW_LEFT)
        actions.perform()
        
        driver.find_element_by_xpath("(//a[contains(@ng-click,'AElimHilo1')])[1]").click() 
        time.sleep(0.5)
        alert.accept()
        time.sleep(.5)
        
        actions.send_keys(Keys.ALT)
        actions.send_keys(Keys.ARROW_LEFT)
        actions.perform()
        
######################## Eliminar Foro #############################################         
        
        
        driver.find_element_by_xpath("(//a[contains(@ng-click,'AElimForo1')])[last()]").click() 
        time.sleep(0.5)
        alert.accept()
        time.sleep(.5)
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
        driver.find_element_by_xpath("//img[@ng-click='VInicio()']").click()
        
        
        
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        #self.driver.quit()
        #self.assertEqual([], self.verificationErrors)
        pass

if __name__ == "__main__":
    unittest.main()
