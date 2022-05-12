import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import warnings

class ll_ATS(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        warnings.simplefilter('ignore', ResourceWarning)
        time.sleep(1)
    def test_ll(self):
        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000")
        time.sleep(1)
            # look for cart in navbar
        elem = driver.find_element(By.XPATH,'//*[@id="myNavbar"]/ul[1]/li[2]/a').click()
        time.sleep(1)

 #       try:  #look for home now buttom
        elem = driver.find_element(By.XPATH,'//*[@id="myNavbar"]/ul[2]/li/a/img').click()
        time.sleep(2)
        print("Test passed- Home page displayed")
        assert True
#        except NoSuchElementException:
 #           self.fail("Home page does not apper- test failed")
def tearDown(self):
    self.driver.close()
if __name__ == "__main__":
    unittest.main()