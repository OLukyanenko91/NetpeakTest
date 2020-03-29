import os
import time
import unittest
import subprocess
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

HOME_URL = "https://netpeak.ua/"
CAREER_URL = "https://career.netpeak.ua/"
HIRING_URL = "https://career.netpeak.ua/hiring/"
RED_COLOR = "rgba(255, 0, 0, 1)"
SUBPROCESS_CMD = "FileUpload.exe {}\\picture.bmp"
DELAY = 5
TIMEOUT = 10


class ProfileTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(HOME_URL)
        time.sleep(DELAY)

    def testBase(self):
        # open 'career' page
        self.driver.find_element_by_class_name("blog").click()
        WebDriverWait(self.driver, TIMEOUT).until(lambda d: d.current_url == CAREER_URL)

        # open 'hiring' page
        self.driver.find_element_by_css_selector(".btn.green-btn").click()
        WebDriverWait(self.driver, TIMEOUT).until(lambda d: d.current_url == HIRING_URL)

        # upload incorrect file
        self.__uploadFile()
        WebDriverWait(self.driver, TIMEOUT).until(lambda d: d.find_elements_by_css_selector(
            "div[class='form-group has-error']"))

        # fill personal data
        self.__fillPersonalData()

        # send profile
        self.driver.find_element_by_id("submit").click()

        # check warning color
        warning = self.driver.find_element_by_class_name("warning-fields")
        assert warning.value_of_css_property("color") == RED_COLOR

        # open home page
        self.driver.find_element_by_class_name("logo-block").click()
        WebDriverWait(self.driver, TIMEOUT).until(lambda d: d.current_url == HOME_URL)

    def tearDown(self):
        self.driver.quit()

    def __uploadFile(self):
        path = os.path.abspath(os.getcwd())
        self.driver.find_element_by_id("upload").click()
        time.sleep(DELAY)
        subprocess.call(SUBPROCESS_CMD.format(path))

    def __fillPersonalData(self):
        self.driver.find_element_by_id("inputName").send_keys("test")
        self.driver.find_element_by_id("inputLastname").send_keys("test")
        self.driver.find_element_by_id("inputEmail").send_keys("test")
        self.driver.find_element_by_id("inputPhone").send_keys("0000")
        self.driver.find_element_by_name("bd").send_keys("1")
        self.driver.find_element_by_name("bm").send_keys("1")
        self.driver.find_element_by_name("by").send_keys("1")


def main():
    unittest.main(exit=False)
    os.system("pause")


if __name__ == "__main__":
    main()
