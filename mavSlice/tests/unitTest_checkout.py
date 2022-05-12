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
        fname = "bryson"  # must be a valid username for the application
        lname = "cash"
        email = "george@gmail.com"
        Bld = "1"
        Add = "1234 st"
        City = "Omaha"
        St = "NE"
        Zip = "68022"

        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000")
        time.sleep(1)
        elem = driver.find_element(By.XPATH, '//*[@id="navbardrop"]').click()
        time.sleep(1)
        elem = driver.find_element(By.XPATH, '//*[@id="myNavbar"]/ul[1]/li[1]/div/a[1]').click()
        time.sleep(1)
        #add to cart
        elem = driver.find_element(By.XPATH, '//*[@id="app-layout"]/div/div[2]/div/div/div/div/div/div/p/a').click()
        time.sleep(1)
        #add to cart again
        elem = driver.find_element(By.XPATH, '//*[@id="app-layout"]/div/div[2]/div/div/form/input[3]').click()
            # look for Cart in navbar
 #       elem = driver.find_element(By.XPATH, '//*[@id="myNavbar"]/ul[1]/li[2]/a').click()
        time.sleep(1)
        #click on checkout button
        elem = driver.find_element(By.XPATH, '//*[@id="app-layout"]/div/div[2]/div/a[2]').click()
        time.sleep(1)
        #fill out chceckout
        elem = driver.find_element(By.XPATH, '//*[@id="id_first_name"]')
        elem.send_keys(fname)
        elem = driver.find_element(By.XPATH, '//*[@id="id_last_name"]')
        elem.send_keys(lname)
        elem = driver.find_element(By.XPATH, '//*[@id="id_email"]')
        elem.send_keys(email)
        elem = driver.find_element(By.XPATH, '//*[@id="id_address"]')
        elem.send_keys(Add)
        elem = driver.find_element(By.XPATH, '//*[@id="id_state"]')
        elem.send_keys(St)
        elem = driver.find_element(By.XPATH, '//*[@id="id_city"]')
        elem.send_keys(City)
        elem = driver.find_element(By.XPATH, '//*[@id="id_zip"]')
        elem.send_keys(Zip)
        elem = driver.find_element(By.XPATH, '//*[@id="id_braintree_id"]')
        elem.send_keys(Bld)
        time.sleep(2)
        elem.send_keys(Keys.RETURN)

        # try:  #look for Continue shopping now buttom
        #     elem = driver.find_element(By.XPATH, '//*[@id="app-layout"]/div/div[2]/div/a[1]')
        #     print("Test passed- Cart page displayed")
        #     assert True
        # except NoSuchElementException:
        #     self.fail("Cart page does not apper- test failed")
def tearDown(self):
    self.driver.close()
if __name__ == "__main__":
    unittest.main()