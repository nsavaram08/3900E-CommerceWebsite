import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class ll_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()


    def test_ll(self):
        user = "admin"
        pwd = "password"

        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000/admin")

        elem = driver.find_element(By.ID,"id_username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID,"id_password")
        elem.send_keys(pwd)
        time.sleep(3)
        elem.send_keys(Keys.RETURN)
        time.sleep(2)

        # Enter home page
        driver.get("http://127.0.0.1:8000")
        time.sleep(3)

        # Click on Item to see Description
        driver.find_element(By.XPATH, "//a[contains(., 'test')]").click()
        time.sleep(3)

        # Add item to cart
        driver.find_element(By.XPATH, "//input[@type='submit' and @value='Add to cart']").click()
        time.sleep(2)

        try:
            # attempt to find the 'Add to Cart' button - if found, pass
            elem = driver.find_element(By.XPATH, "//a[contains(., 'Remove')]")
            driver.close()
            assert True

        except NoSuchElementException:
            driver.close()
            self.fail("Item Description Failed - item may not exist")

        time.sleep(3)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(warnings='ignore')
