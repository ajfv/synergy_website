# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class PruebasIniSesion(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://rsocialfl-prmm95.c9users.io/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_pruebas_ini_sesion(self):
        driver = self.driver
        driver.get(self.base_url + "/#/VLogin")
        actions = ActionChains(self.driver)
        alert = Alert(self.driver)
        
########################  Contrasenha Invalida #################################################### 
        driver.find_element_by_id("fLogin_usuario").clear()
        driver.find_element_by_id("fLogin_usuario").send_keys("Test Usuario")
        driver.find_element_by_id("fLogin_clave").clear()
        driver.find_element_by_id("fLogin_clave").send_keys("bbbbbbbb")
        driver.find_element_by_id("conectate").click()
        time.sleep(0.5)
        alert.accept()
        time.sleep(.5)
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
########################  Usuario no Existente #################################################### 
        driver.find_element_by_id("fLogin_usuario").clear()
        driver.find_element_by_id("fLogin_usuario").send_keys("UsuarioNoExiste")
        driver.find_element_by_id("fLogin_clave").clear()
        driver.find_element_by_id("fLogin_clave").send_keys("aaaaaaaa")
        driver.find_element_by_id("conectate").click()
        time.sleep(0.5)
        alert.accept()
        time.sleep(.5)
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
########################  Usuario Vacio #################################################### 
        driver.find_element_by_id("fLogin_clave").clear()
        driver.find_element_by_id("fLogin_clave").send_keys("aaaaaaaa")
        driver.find_element_by_id("conectate").click()
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
########################  Clave Vacia #################################################### 
        driver.find_element_by_id("fLogin_usuario").clear()
        driver.find_element_by_id("fLogin_usuario").send_keys("Test Usuario")
        driver.find_element_by_id("conectate").click()
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
########################  Todo Vacio #################################################### 
        driver.find_element_by_id("conectate").click()
    
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
