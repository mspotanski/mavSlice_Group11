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
        time.sleep(15)
        def test_ll(self):
            driver = self.driver
            driver.maximize_window()
            driver.get("http://127.0.0.1:800")
            time.sleep(15)
                # look for Cart in navbar
            elem= driver.find_element(By.XPATH, '//*[@id="myNavbar"]/ul[1]/li[4]/a').click()
            time.sleep(15)

            try:  #look for Continue shopping now buttom
                elem = driver.find_element(By.XPATH, '//*[@id="app-layout"]/div/div[2]/div/a[1]')
                print("Test passed- Cart page displayed")
                assert True
            except NoSuchElementException:
                self.fail("Cart page does not apper- test failed")
def tearDown(self):
    self.driver.close()
if __name__ == "__main__":
    unittest.main()