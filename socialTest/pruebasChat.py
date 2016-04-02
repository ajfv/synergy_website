# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Test3(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://rsocialfl-prmm95.c9users.io/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_3(self):
        driver = self.driver
        driver.get(self.base_url + "/#/VLogin")
        actions = ActionChains(self.driver)
        driver.find_element_by_id("fLogin_usuario").clear()
        driver.find_element_by_id("fLogin_usuario").send_keys("Usuario")
        driver.find_element_by_id("fLogin_clave").clear()
        driver.find_element_by_id("fLogin_clave").send_keys("aaaaaaaa")
        driver.find_element_by_id("conectate").click()
        driver.find_element_by_xpath("//a[@ng-show='idUsuario']").click()
        driver.find_element_by_xpath("(//img[@alt='chat'])[1]").click()
        
        driver.find_element_by_id("fChat_texto").clear()
        driver.find_element_by_id("fChat_texto").send_keys("Probando")
        time.sleep(1)
        driver.find_element_by_id("btnHilos").click()
        time.sleep(1)
        actions.send_keys(Keys.ESCAPE)
        actions.perform()
        time.sleep(.5)
        driver.find_element_by_xpath("//span[@ng-bind='idUsuario']").click()
        time.sleep(.5)
        driver.find_element_by_xpath("//a[@ng-click='ASalir(idUsuario)']").click()
        time.sleep(.5)
        actions.send_keys(Keys.CONTROL)
        actions.send_keys('r')
        actions.perform()
        time.sleep(.5)
        
        driver.get(self.base_url + "/#/VLogin")
        driver.find_element_by_id("fLogin_usuario").clear()
        driver.find_element_by_id("fLogin_usuario").send_keys("Usuario1")
        driver.find_element_by_id("fLogin_clave").clear()
        driver.find_element_by_id("fLogin_clave").send_keys("aaaaaaaa")
        driver.find_element_by_id("conectate").click()
        driver.find_element_by_xpath("//a[@ng-show='idUsuario']").click()
        driver.find_element_by_xpath("(//img[@alt='chat'])[1]").click()
        
        driver.find_element_by_id("fChat_texto").clear()
        driver.find_element_by_id("fChat_texto").send_keys("Prueba aceptada")
        time.sleep(1)
        driver.find_element_by_id("btnHilos").click()
        time.sleep(1)
        actions.send_keys(Keys.ESCAPE)
        actions.perform()
        time.sleep(.5)
        driver.find_element_by_xpath("//span[@ng-bind='idUsuario']").click()
        time.sleep(.5)
        driver.find_element_by_xpath("//a[@ng-click='ASalir(idUsuario)']").click()
        time.sleep(.5)

        
        
        
        
    
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
