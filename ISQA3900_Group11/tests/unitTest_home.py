import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import warnings

class ll_ATS(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Safari()
        warnings.simplefilter('ignore', ResourceWarning)
        time.sleep(20)
        def test_ll(self):
            driver = self.driver
            driver.maximize_window()
            driver.get("http://127.0.0.1:800")
            time.sleep(10)
                # look for home in navbar
            elem= driver.find_element(By.XPATH,'//*[@id="myNavbar"]/ul[1]/li[2]/a').click()
            time.sleep(8)

            try:  #look for order now buttom
                elem = driver.find_element(By.XPATH,'//*[@id="app-layout"]/div/div[2]/div/div[2]/div[1]/a/button')
                print("Test passed- Home page displayed")
                assert True
            except NoSuchElementException:
                self.fail("Home page does not apper- test failed")
def tearDown(self):
    self.driver.close()
if __name__ == "__main__":
    unittest.main()