from appium import webdriver
from configuration import config as cfg
from testdata import data as td
import unittest
import requests
import logging
import common
import time
import sys

class PublicUserPurchaseTransactions(unittest.TestCase):
    cf =  common.common_functionalities()
    
    
    def setUp(self):
        self.api_session = requests.Session()
        self.api_session.auth = (cfg.cbt_username,cfg.cbt_authkey)
        self.test_result = None
        cfg.caps['name'] = "Public User Purchase transactions"
        self.driver = webdriver.Remote(
            desired_capabilities=cfg.caps,
            command_executor="http://%s:%s@hub.crossbrowsertesting.com:80/wd/hub"%(cfg.cbt_username,cfg.cbt_authkey)
        )

        # start the remote browser on our server
        self.driver.implicitly_wait(20)
        self.id = self.driver.session_id
        logging.basicConfig(filename="%s.log"%(self.__class__.__name__),level=logging.DEBUG,format="%(asctime)s:%(levelname)s:%(message)s")
        
    def test_validate_usd_purchase_pkg1(self):
        '''Validate public user purchase with USD currency and using VISA credit card'''
        try:
            # We need to make sure that price packages are set based on test data
            self.driver.get("%s"%td.test_url)
            self.cf.login(self.driver, td.test_admin_username, td.test_admin_password)
            self.cf.change_price_pkg(self.driver, td.test_pkg1)
            self.cf.screenshot(self.api_session, self.id, "Change of package1")
            self.driver.get("%s"%td.test_url)
            self.cf.logout(self.driver)
            
            self.driver.get("%s"%td.test_url)
            self.driver.find_element_by_xpath("//header[@id='footer']/div/a[1]/img").click()
            self.cf.screenshot(self.api_session, self.id, "Home screen")
            
            if len(self.driver.find_elements_by_xpath("//div[@class='modal-content']")) > 0:
                time.sleep(2)
            
            package1 = self.driver.find_element_by_xpath("//div[@class='modal-content']/div[@class='modal-body']/div/div[1]/a")
            print package1.text
            self.cf.screenshot(self.api_session, self.id, "Package1 Dialog")
            
            
            self.test_result = 'pass'

        except AssertionError as e:
            self.test_result = 'fail'
            raise

    def tearDown(self):
        self.cf.screenshot(self.api_session, self.id, "Teardown")
        print("Done with session.")
        self.driver.quit()
        if self.test_result is not None:
            self.cf.set_status(self.api_session, self.driver.session_id, self.test_result)


if __name__ == '__main__':
    unittest.main()