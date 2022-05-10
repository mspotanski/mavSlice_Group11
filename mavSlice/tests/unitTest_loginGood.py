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

    def test_11(self):
        user = "kandel"
        pwd = "kandel"

        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:800")
        elem = driver.fint_element(By.XPATH,'//*[@id="myNavbar"]/ul[3]/li/a').click()
        time.sleep(6)

        elem = driver.find_element(By.NAME, "username")
        elem.send_keys(user)
        elem = driver.find_element(By.NAME, "password")
        elem.send_keys(pwd)
        time.sleep(8)
        elem.send_keys(Keys.RETURN)
        time.sleep(8)
        elem = driver.find_element(By.XPATH, '//*[@id="app-layout"]/div/div[2]/div/div[3]/div[1]/a/button')
        time.sleep(8)

        try:
            elem = driver.find_element(By.XPATH,'//*[@id="app-layout"]/div/div[2]/div/div[3]/div[1]/a/button' )
            print("Test Passed -Valid user is logged in sucessfully")
            assert True
        except NoSuchElementException:
            self.fail("Login Failed- user may not exist")

    def tearDown(self):
        self.driver.close()

    if __name__ == "__main__":
        unittest.main()


