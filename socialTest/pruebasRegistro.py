# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class PruebasRegistro(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://rsocialfl-prmm95.c9users.io/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_pruebas_registro(self):
        driver = self.driver
        driver.get(self.base_url + "/#/VRegistro")
        actions = ActionChains(self.driver)
        
######################## Claves de 7 caracteres #############################################        
            
        driver.find_element_by_id("fUsuario_nombre").clear()
        driver.find_element_by_id("fUsuario_nombre").send_keys("Test Nombre")
        driver.find_element_by_id("fUsuario_usuario").clear()
        driver.find_element_by_id("fUsuario_usuario").send_keys("Test Usuario")
        driver.find_element_by_id("fUsuario_clave").clear()
        driver.find_element_by_id("fUsuario_clave").send_keys("aaaaaaa")
        driver.find_element_by_id("fUsuario_clave2").clear()
        driver.find_element_by_id("fUsuario_clave2").send_keys("aaaaaaa")
        driver.find_element_by_id("fUsuario_correo").clear()
        driver.find_element_by_id("fUsuario_correo").send_keys("nombre@mail.com")  
        driver.find_element_by_xpath("//button[@id='botonRegistro']").click()
        time.sleep(.5)
        
        try: driver.find_element_by_xpath("//button[@id='botonRegistro']")
        except: raise SyntaxError("Se creo un usuario con clave de menos de 8 caracteres.")
        
########################  Claves diferenes #################################################          
        
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
        driver.find_element_by_id("fUsuario_nombre").clear()
        driver.find_element_by_id("fUsuario_nombre").send_keys("Test Nombre")
        driver.find_element_by_id("fUsuario_usuario").clear()
        driver.find_element_by_id("fUsuario_usuario").send_keys("Test Usuario")
        driver.find_element_by_id("fUsuario_clave").clear()
        driver.find_element_by_id("fUsuario_clave").send_keys("aaaaaaaa")
        driver.find_element_by_id("fUsuario_clave2").clear()
        driver.find_element_by_id("fUsuario_clave2").send_keys("aaaaaaab")
        driver.find_element_by_id("fUsuario_correo").clear()
        driver.find_element_by_id("fUsuario_correo").send_keys("nombre@mail.com")
        driver.find_element_by_id("botonRegistro").click()
        time.sleep(.5)
        
        try: driver.find_element_by_xpath("//button[@id='botonRegistro']")
        except: raise SyntaxError("Se creo un usuario con verificacion de clave erronea.")
        
########################  Mail Invalido ####################################################          
        
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
        driver.find_element_by_id("fUsuario_nombre").clear()
        driver.find_element_by_id("fUsuario_nombre").send_keys("Test Nombre")
        driver.find_element_by_id("fUsuario_usuario").clear()
        driver.find_element_by_id("fUsuario_usuario").send_keys("Test Usuario")
        driver.find_element_by_id("fUsuario_clave").clear()
        driver.find_element_by_id("fUsuario_clave").send_keys("aaaaaaaa")
        driver.find_element_by_id("fUsuario_clave2").clear()
        driver.find_element_by_id("fUsuario_clave2").send_keys("aaaaaaaa")
        driver.find_element_by_id("fUsuario_correo").clear()
        driver.find_element_by_id("fUsuario_correo").send_keys("mail")
        driver.find_element_by_id("botonRegistro").click()
        time.sleep(.5)
        
        try: driver.find_element_by_xpath("//button[@id='botonRegistro']")
        except: raise SyntaxError("Se creo un usuario con email invalido.")
        
########################  Nombre Vacio ####################################################          
        
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
        driver.find_element_by_id("fUsuario_usuario").clear()
        driver.find_element_by_id("fUsuario_usuario").send_keys("Test Usuario")
        driver.find_element_by_id("fUsuario_clave").clear()
        driver.find_element_by_id("fUsuario_clave").send_keys("aaaaaaaa")
        driver.find_element_by_id("fUsuario_clave2").clear()
        driver.find_element_by_id("fUsuario_clave2").send_keys("aaaaaaaa")
        driver.find_element_by_id("fUsuario_correo").clear()
        driver.find_element_by_id("fUsuario_correo").send_keys("nombre@mail.com")
        driver.find_element_by_id("botonRegistro").click()
        time.sleep(.5)
        
        try: driver.find_element_by_xpath("//button[@id='botonRegistro']")
        except: raise SyntaxError("Se creo un usuario con nombre vacio.")
        
########################  Usuario Vacio ####################################################         
        
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
        driver.find_element_by_id("fUsuario_nombre").clear()
        driver.find_element_by_id("fUsuario_nombre").send_keys("Test Nombre")
        driver.find_element_by_id("fUsuario_clave").clear()
        driver.find_element_by_id("fUsuario_clave").send_keys("aaaaaaaa")
        driver.find_element_by_id("fUsuario_clave2").clear()
        driver.find_element_by_id("fUsuario_clave2").send_keys("aaaaaaaa")
        driver.find_element_by_id("fUsuario_correo").clear()
        driver.find_element_by_id("fUsuario_correo").send_keys("nombre@mail.com")
        driver.find_element_by_id("botonRegistro").click()
        time.sleep(.5)
        
        try: driver.find_element_by_xpath("//button[@id='botonRegistro']")
        except: raise SyntaxError("Se creo un usuario con usuario vacio.")
        
########################  Usuario Ocupado ####################################################         
        
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
        driver.find_element_by_id("fUsuario_nombre").clear()
        driver.find_element_by_id("fUsuario_nombre").send_keys("Test Nombre")
        driver.find_element_by_id("fUsuario_usuario").clear()
        driver.find_element_by_id("fUsuario_usuario").send_keys("Test Usuario")
        driver.find_element_by_id("fUsuario_clave").clear()
        driver.find_element_by_id("fUsuario_clave").send_keys("aaaaaaaa")
        driver.find_element_by_id("fUsuario_clave2").clear()
        driver.find_element_by_id("fUsuario_clave2").send_keys("aaaaaaaa")
        driver.find_element_by_id("fUsuario_correo").clear()
        driver.find_element_by_id("fUsuario_correo").send_keys("nombre@mail.com")
        driver.find_element_by_id("botonRegistro").click()
        time.sleep(.5)
        
        try: driver.find_element_by_xpath("//button[@id='botonRegistro']")
        except: raise SyntaxError("Se creo un usuario con usuario vacio.")
        
########################  Clave 1 Vacia ####################################################         
        
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
        driver.find_element_by_id("fUsuario_nombre").clear()
        driver.find_element_by_id("fUsuario_nombre").send_keys("Test Nombre")
        driver.find_element_by_id("fUsuario_usuario").clear()
        driver.find_element_by_id("fUsuario_usuario").send_keys("Test Usuario")
        driver.find_element_by_id("fUsuario_clave2").clear()
        driver.find_element_by_id("fUsuario_clave2").send_keys("aaaaaaaa")
        driver.find_element_by_id("fUsuario_correo").clear()
        driver.find_element_by_id("fUsuario_correo").send_keys("nombre@mail.com")
        driver.find_element_by_id("botonRegistro").click()
        time.sleep(.5)     
        
        try: driver.find_element_by_xpath("//button[@id='botonRegistro']")
        except: raise SyntaxError("Se creo un usuario con clave vacia.")
           
########################  Clave 2 Vacia ####################################################         
        
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
        driver.find_element_by_id("fUsuario_nombre").clear()
        driver.find_element_by_id("fUsuario_nombre").send_keys("Test Nombre")
        driver.find_element_by_id("fUsuario_usuario").clear()
        driver.find_element_by_id("fUsuario_usuario").send_keys("Test Usuario")
        driver.find_element_by_id("fUsuario_clave").clear()
        driver.find_element_by_id("fUsuario_clave").send_keys("aaaaaaaa")
        driver.find_element_by_id("fUsuario_correo").clear()
        driver.find_element_by_id("fUsuario_correo").send_keys("nombre@mail.com")
        driver.find_element_by_id("botonRegistro").click()
        time.sleep(.5) 
        
        try: driver.find_element_by_xpath("//button[@id='botonRegistro']")
        except: raise SyntaxError("Se creo un usuario con verificacion de clave vacia.")
        
########################  Correo Vacio ####################################################         
        
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
        driver.find_element_by_id("fUsuario_nombre").clear()
        driver.find_element_by_id("fUsuario_nombre").send_keys("Test Nombre")
        driver.find_element_by_id("fUsuario_usuario").clear()
        driver.find_element_by_id("fUsuario_usuario").send_keys("Test Usuario")
        driver.find_element_by_id("fUsuario_clave").clear()
        driver.find_element_by_id("fUsuario_clave").send_keys("aaaaaaaa")
        driver.find_element_by_id("fUsuario_clave2").clear()
        driver.find_element_by_id("fUsuario_clave2").send_keys("aaaaaaaa")
        driver.find_element_by_id("botonRegistro").click()
        time.sleep(.5)    
        
        try: driver.find_element_by_xpath("//button[@id='botonRegistro']")
        except: raise SyntaxError("Se creo un usuario con correo vacio.")
        
########################  Todo Vacio ####################################################         
        
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
        driver.find_element_by_id("botonRegistro").click()
        time.sleep(.5)     
        
        try: driver.find_element_by_xpath("//button[@id='botonRegistro']")
        except: raise SyntaxError("Se creo un usuario con todos los campos vacios. Boo")        

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
        pass

if __name__ == "__main__":
    unittest.main()
