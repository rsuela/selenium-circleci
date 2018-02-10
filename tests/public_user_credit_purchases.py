from appium import webdriver
from configuration import config as cfg
import unittest
import requests
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
    
    def test_validate_usd_purchase_pkg1(self):
        '''Validate public user purchase with USD currency and using VISA credit card'''
        try:
            self.driver.get("%s"%cfg.test_url)
            self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/header/div/div/div/i").click()
            self.driver.find_element_by_link_text("Log in").click()
            self.cf.screenshot(self.api_session, self.id, "initial screenshot")
            self.test_result = 'pass'

        except AssertionError as e:
            self.test_result = 'fail'
            raise

    def tearDown(self):
        self.cf.screenshot(self.api_session, self.id, "Teardown")
        print("\n\tDone with session.")
        self.driver.quit()
        if self.test_result is not None:
            self.cf.set_status(self.api_session, self.driver.session_id, self.test_result)


if __name__ == '__main__':
    unittest.main()