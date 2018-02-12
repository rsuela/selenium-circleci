from selenium.webdriver.support.ui import Select
from configuration import config as cfg
from appium import webdriver
from testdata import data as td
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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
            print "Assert package \nExpected: %s %s \nLive: %s" %(td.test_pkg1['USD'], "USD", package1.text.encode('ascii', 'ignore'))
            self.assertEqual("%s %s"%(td.test_pkg1['USD'], "USD"), package1.text.encode('ascii', 'ignore'))
            self.cf.screenshot(self.api_session, self.id, "Package1 Dialog")
            
            package1.click()
            self.cf.screenshot(self.api_session, self.id, "Checkout Page")
            
            # Checkout page
            print "Checkout page"
            print "First name: %s"%(td.user1['name'])
            self.driver.find_element_by_id("user_first_name").send_keys(td.user1['name'])
            print "Surname: %s"%(td.user1['surname'])
            self.driver.find_element_by_id("user_last_name").send_keys(td.user1['surname'])
            print "Email Address: %s"%(td.user1['email'])
            self.driver.find_element_by_id("email_address").send_keys(td.user1['email'])
            self.cf.screenshot(self.api_session, self.id, "Email Address")
            self.driver.find_element_by_id("email_re").send_keys(td.user1['email'])
            self.cf.screenshot(self.api_session, self.id, "Confirm Email Address")
            print "Mobile: %s"%(td.user1['mobile'])
            self.driver.find_element_by_id("phoneNumber").send_keys(td.user1['mobile'])
            self.cf.screenshot(self.api_session, self.id, "Checkout Page with details")
            
            
            self.driver.find_element_by_id("countries_timezones2").click()
            for country in self.driver.find_elements_by_xpath("//div[@class='bfh-selectbox-options']/div/ul/li/a"):
                if country.text.encode('ascii', 'ignore').lower() == td.user1['country'].lower():
                    print "Selected %s"%(country.text.encode('ascii', 'ignore').lower())
                    country.click()
                    time.sleep(1) # to populate the timezone
                    break
            
            self.driver.find_element_by_id("timezone").click()
            for timezone in self.driver.find_elements_by_xpath("//div[@id='timezone']/div[@class='bfh-selectbox-options']/div/ul/li/a"):
                if td.user1['timezone'].lower() in timezone.text.encode('ascii', 'ignore').lower():
                    print "Selected %s"%(timezone.text.encode('ascii', 'ignore'))
                    timezone.click()
                    break
            self.cf.screenshot(self.api_session, self.id, "Checkout Page with details")
            self.driver.find_element_by_id("suburb").send_keys(td.user1['suburb'])
            self.driver.find_element_by_id("user_city").send_keys(td.user1['city'])
            self.driver.find_element_by_id("card_number").send_keys(td.user1['creditcard'])
            self.driver.find_element_by_id("card_name").send_keys("%s %s"%(td.user1['name'], td.user1['surname']))
            self.driver.find_element_by_id("cvv").send_keys(td.user1['cvv'])
            self.driver.find_element_by_id("terms").click()
            print "Submitting form"
            self.driver.find_element_by_id("check_out_buy_now_button").click()
            
            self.cf.wait_till_visible(self.driver.find_elements_by_id("checkoutResultSucess"))
            result_msg = "Thank you for your purchase. Please check your email inbox for further details."
            print "Result Message: %s"%(self.driver.find_element_by_xpath("//span[@id='Seamless_ReportBugForm_expected_results']/span[@class='seamless-view msgForNonLoggedIn']").text.encode('ascii', 'ignore'))
            self.assertEqual(result_msg, self.driver.find_element_by_xpath("//span[@id='Seamless_ReportBugForm_expected_results']/span[@class='seamless-view msgForNonLoggedIn']").text.encode('ascii', 'ignore'))
            
            # go to admin and check balance
            
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