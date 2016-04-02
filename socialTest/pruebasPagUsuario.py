# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class PruebasPagUsuario(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://rsocialfl-prmm95.c9users.io/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_pruebas_pag_usuario(self):
        driver = self.driver
        driver.get(self.base_url + "/#/VRegistro")
        actions = ActionChains(self.driver)
        
######################## Crea Usuario y se conecta #############################################          
        driver.find_element_by_id("fUsuario_nombre").clear()
        driver.find_element_by_id("fUsuario_nombre").send_keys("Nombre")
        driver.find_element_by_id("fUsuario_usuario").clear()
        driver.find_element_by_id("fUsuario_usuario").send_keys("UsuarioNuevo")
        driver.find_element_by_id("fUsuario_clave").clear()
        driver.find_element_by_id("fUsuario_clave").send_keys("aaaaaaaa")
        driver.find_element_by_id("fUsuario_clave2").clear()
        driver.find_element_by_id("fUsuario_clave2").send_keys("aaaaaaaa")
        driver.find_element_by_id("fUsuario_correo").clear()
        driver.find_element_by_id("fUsuario_correo").send_keys("nombre@mail.com")  
        driver.find_element_by_xpath("//button[@id='botonRegistro']").click()
        time.sleep(1)
        driver.find_element_by_id("fLogin_usuario").clear()
        driver.find_element_by_id("fLogin_usuario").send_keys("UsuarioNuevo")
        time.sleep(.5)
        driver.find_element_by_id("fLogin_clave").clear()
        driver.find_element_by_id("fLogin_clave").send_keys("aaaaaaaa")
        time.sleep(.5)
        driver.find_element_by_xpath("//button[@id='conectate']").click()
        time.sleep(3)
        
######################## Prueba Pagina Vacia y Sin titulo #############################################         
        driver.find_element_by_xpath("//span[@ng-bind='idUsuario']").click()
        time.sleep(.5)
        driver.find_element_by_xpath("//a[@ng-click='VMiPagina(idUsuario)']").click()
        time.sleep(.5)
        driver.find_element_by_xpath("//img[@id='perfil']").click()
        time.sleep(.5)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(.5)
        driver.find_element_by_xpath("//span[@ng-bind='usuario.nombre']").click()
        time.sleep(.5)
        driver.find_element_by_xpath("//a[@ng-click='__ayuda()']").click()
        time.sleep(1)
        
        actions.key_down(Keys.CONTROL)
        actions.send_keys('r')
        actions.key_up(Keys.CONTROL)
        actions.perform()
        time.sleep(.5)

        driver.find_element_by_id("taTextElement").send_keys("Mi Pagina ") 
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(.5)
        actions.key_down(Keys.CONTROL)
        actions.send_keys('r')
        actions.key_up(Keys.CONTROL)
        actions.perform()
        time.sleep(.5)
        
######################## Prueba opciones y Crea Pagina #############################################         
        driver.find_element_by_id("fPagina_titulo").clear()
        driver.find_element_by_id("fPagina_titulo").send_keys("Mi pagina de Usuario")
        driver.find_element_by_id("taTextElement").click()
        driver.find_element_by_id("taTextElement").send_keys("Mi Pagina ") 
        time.sleep(.5)
        driver.find_element_by_name("h1").click()
        driver.find_element_by_id("taTextElement").send_keys("Mi Pagina")
        time.sleep(.5)
        driver.find_element_by_name("h2").click()
        driver.find_element_by_id("taTextElement").send_keys("a")
        time.sleep(.5)
        driver.find_element_by_name("h3").click()
        driver.find_element_by_id("taTextElement").send_keys("Mi Pagina")
        time.sleep(.5)
        driver.find_element_by_name("h4").click()
        driver.find_element_by_id("taTextElement").send_keys("Mi Pagina")
        time.sleep(.5)
        driver.find_element_by_name("h5").click()
        driver.find_element_by_id("taTextElement").send_keys("Mi Pagina")
        time.sleep(.5)
        driver.find_element_by_name("h6").click()
        driver.find_element_by_id("taTextElement").send_keys("Mi Pagina")
        time.sleep(.5)
        driver.find_element_by_name("pre").click()
        driver.find_element_by_id("taTextElement").send_keys("la ")
        time.sleep(.5)
        driver.find_element_by_name("quote").click()
        driver.find_element_by_id("taTextElement").send_keys("mejor ")
        time.sleep(.5)
        driver.find_element_by_name("bold").click()
        driver.find_element_by_id("taTextElement").send_keys("Mi ")
        time.sleep(.5)
        driver.find_element_by_name("italics").click()
        driver.find_element_by_id("taTextElement").send_keys("Pagina ")
        time.sleep(.5)
        driver.find_element_by_name("underline").click()
        driver.find_element_by_id("taTextElement").send_keys("es")
        time.sleep(.5)  
        driver.find_element_by_name("ol").click()
        driver.find_element_by_id("taTextElement").send_keys("la")      
        time.sleep(.5)
        driver.find_element_by_name("ul").click()
        driver.find_element_by_id("taTextElement").send_keys("mejor")      
        time.sleep(.5)
        driver.find_element_by_name("undo").click()      
        time.sleep(.5)
        driver.find_element_by_name("redo").click()   
        time.sleep(.5)
        driver.find_element_by_name("clear").click()
        time.sleep(.5)
        driver.find_element_by_name("justifyCenter").click()
        driver.find_element_by_id("taTextElement").send_keys("a")
        time.sleep(.5)
        driver.find_element_by_name("justifyRight").click()
        driver.find_element_by_id("taTextElement").send_keys("b")
        time.sleep(.5)
        driver.find_element_by_name("justifyLeft").click()
        driver.find_element_by_id("taTextElement").send_keys("c")
        time.sleep(.5)
        driver.find_element_by_name("html").click()
        time.sleep(.5)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(5)
        driver.find_element_by_xpath("//img[@ng-click='VInicio()']").click()
        time.sleep(5)
        driver.find_element_by_xpath("//a[@ng-click='VPrincipal()']").click()
        time.sleep(2)
        driver.find_element_by_xpath("//span[@ng-bind='idUsuario']").click()
        time.sleep(.5)

        
        driver.find_element_by_xpath("//a[@ng-click='VMiPagina(idUsuario)']").click()
        
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
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
