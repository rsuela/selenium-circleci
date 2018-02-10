import unittest
#from selenium import webdriver
from appium import webdriver
import requests
import time

class PublicWebsite(unittest.TestCase):

    def screenshot(self):
        snapshot_hash = self.api_session.post('https://crossbrowsertesting.com/api/v3/selenium/' + self.driver.session_id + '/snapshots').json()['hash']
        self.api_session.put('https://crossbrowsertesting.com/api/v3/selenium/' + self.driver.session_id + '/snapshots/' + snapshot_hash,
            data={'description':"screenshot"})

    def setUp(self):

        # Put your username and authey below
        # You can find your authkey at crossbrowsertesting.com/account
        self.username = "jhudson.953bot@gmail.com"
        self.authkey  = "u6273fa5b70e34de"

        self.api_session = requests.Session()
        self.api_session.auth = (self.username,self.authkey)

        self.test_result = None

        caps = {}
        
        caps['name'] = 'Price Package Update'
        caps['build'] = '1.0'
        
        # caps['browserName'] = 'Chrome'
        # caps['deviceName'] = 'Galaxy S6'
        # caps['platformVersion'] = '5.0'
        # caps['platformName'] = 'Android'
        # caps['deviceOrientation'] = 'portrait'
        
        caps['browserName'] = 'Chrome'
        caps['deviceName'] = 'Galaxy S6'
        caps['platformVersion'] = '5.0'
        caps['platformName'] = 'Android'
        caps['deviceOrientation'] = 'portrait'

        self.driver = webdriver.Remote(
            desired_capabilities=caps,
            command_executor="http://%s:%s@hub.crossbrowsertesting.com:80/wd/hub"%(self.username,self.authkey)
        )
        
        # Data specific to 247friend
        self.testurl = "http://qa.247friend.org/"
        self.username = "admin-qa@247friend.org"
        self.password = "fTkYU7U)!yj1n1c%o&usCp5"

        # start the remote browser on our server
        self.driver.implicitly_wait(20)

    def test_select_package_and_buy_credit(self):
        print("\n\t[ 16.2 Select Package & \"Buy Credit\" (\"Buy Time\") ]")
        print("\n\tBuy credit pop up 36 package prices, controlled by Admin (6 packages for each of the 6 currencies)")
        try:
        
        # Data for Price Package
            package1 = {"USD": "88", "AUD":"87", "NZD":"86", "CAD":"85", "EUR":"84", "GBP":"83"}

            print("\n\t\t> Loading %s"%self.testurl)
            self.driver.get("%s"%self.testurl)
            print("\n\t\t> title: %s"%self.driver.title)
            print("\n\t\t> Click login link")
            self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/header/div/div/div/i").click()
            self.driver.find_element_by_link_text("Log in").click()
            print("\n\t\t> title: %s"%self.driver.title)

            print("\n\t\t> input email address: %s"%self.username)
            self.driver.find_element_by_id("email_address").send_keys(self.username)
            
            print("\n\t\t> input user password: %s"%self.password)
            self.driver.find_element_by_id("user_pass").send_keys(self.password)
            self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/section/div/div/form/div/div/div[1]/label").click()
            self.screenshot()
            self.driver.find_element_by_id("wp_submit").click()
            self.screenshot()
            print("\n\t\t> Navigating to Price Packages")
            self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/ul[1]/li[1]/a/span[1]").click()
            self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/ul/li[9]/a/div[3]").click()
            self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/ul/li[9]/ul/li[2]/a").click()
            self.screenshot()
            
            print("\n\t\t> Navigating to Edit Package1")
            print("\n\t\tTestData: %s"%str(package1))
            self.driver.find_element_by_id("delete-pp").click()
            self.screenshot()
            self.driver.find_element_by_name("edit_package_price").clear()
            self.driver.find_element_by_name("edit_package_price").send_keys(package1['USD'])
            
            self.driver.find_element_by_name("edit_aud_package_price").clear()
            self.driver.find_element_by_name("edit_aud_package_price").send_keys(package1['AUD'])
            
            self.driver.find_element_by_name("edit_nzd_package_price").clear()
            self.driver.find_element_by_name("edit_nzd_package_price").send_keys(package1['NZD'])
            
            self.driver.find_element_by_name("edit_cad_package_price").clear()
            self.driver.find_element_by_name("edit_cad_package_price").send_keys(package1['CAD'])
            
            self.driver.find_element_by_name("edit_eur_package_price").clear()
            self.driver.find_element_by_name("edit_eur_package_price").send_keys(package1['EUR'])
            
            self.driver.find_element_by_name("edit_gbp_package_price").clear()
            self.driver.find_element_by_name("edit_gbp_package_price").send_keys(package1['GBP'])
            
            self.screenshot()
            print("\n\t\t> Submitting changes.")
            self.driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/div[1]/div[5]/div/form/table/tbody/tr[2]/td[1]/h3").click()
            self.driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/div[1]/div[5]/div/form/table/tbody/tr[3]/td[2]/button").click()
            
            print("\n\t\t> Logging out as Admin")
            self.driver.get("%s"%self.testurl)
            self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/header/div/div/div/i").click()
            self.screenshot()
            self.driver.find_element_by_link_text("Log out").click()
            self.screenshot()
            if len(self.driver.find_elements_by_link_text("log out")) != 0:
                self.driver.find_element_by_link_text("log out").click()
                self.screenshot()
            
            self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/header/div/a[1]/img").click()
            self.screenshot()
            time.sleep(1)
            self.driver.get("%s"%self.testurl)
            self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/header/div/a[1]/img").click()
            time.sleep(2)
            print("\n\t\t> Testing Package1 \"Buy Package\" USD")
            print("\t\t> Expected USD package: %s %s"%(package1['USD'], "USD"))
            print("\t\t> Live USD package: %s"%(self.driver.find_element_by_xpath("//div[@class='modal-body']/div[1]/div[1]/a").text.encode('ascii', 'ignore')))
            self.assertEqual("%s %s"%(package1['USD'], "USD"), self.driver.find_element_by_xpath("//div[@class='modal-body']/div[1]/div[1]/a").text.encode('ascii', 'ignore'))
            self.screenshot()
            
            self.driver.find_element_by_link_text("$AUD").click()
            time.sleep(2)
            print("\n\t\t> Testing Package1 \"Buy Package\" AUD")
            print("\t\t> Expected AUD package: %s %s"%(package1['AUD'], "AUD"))
            print("\t\t> Live AUD package: %s"%(self.driver.find_element_by_xpath("//div[@class='modal-body']/div[1]/div[1]/a").text.encode('ascii', 'ignore')))
            self.assertEqual("%s %s"%(package1['AUD'], "AUD"), self.driver.find_element_by_xpath("//div[@class='modal-body']/div[1]/div[1]/a").text.encode('ascii', 'ignore'))
            self.screenshot()
            
            self.driver.find_element_by_link_text("$NZD").click()
            time.sleep(2)
            print("\n\t\t> Testing Package1 \"Buy Package\" NZD")
            print("\t\t> Expected NZD package: %s %s"%(package1['NZD'], "NZD"))
            print("\t\t> Live NZD package: %s"%(self.driver.find_element_by_xpath("//div[@class='modal-body']/div[1]/div[1]/a").text.encode('ascii', 'ignore')))
            
            self.assertEqual("%s %s"%(package1['NZD'], "NZD"), self.driver.find_element_by_xpath("//div[@class='modal-body']/div[1]/div[1]/a").text.encode('ascii', 'ignore'))
            self.screenshot()
            
            self.driver.find_element_by_link_text("$CAD").click()
            time.sleep(2)
            print("\n\t\t> Testing Package1 \"Buy Package\" CAD")
            print("\t\t> Expected CAD package: %s %s"%(package1['CAD'], "CAD"))
            print("\t\t> Live CAD package: %s"%(self.driver.find_element_by_xpath("//div[@class='modal-body']/div[1]/div[1]/a").text.encode('ascii', 'ignore')))

            self.assertEqual("%s %s"%(package1['CAD'], "CAD"), self.driver.find_element_by_xpath("//div[@class='modal-body']/div[1]/div[1]/a").text.encode('ascii', 'ignore'))
            self.screenshot()
            
            self.driver.get("https://qa.247friend.org/login/?currency=EUR&trig=packagesModal")
            time.sleep(2)
            print("\n\t\t> Testing Package1 \"Buy Package\" EUR")
            print("\t\t> Expected EUR package: %s %s"%(package1['EUR'], "EUR"))
            print("\t\t> Live EUR package: %s"%(self.driver.find_element_by_xpath("//div[@class='modal-body']/div[1]/div[1]/a").text.encode('ascii', 'ignore')))
            self.assertEqual("%s %s"%(package1['EUR'], "EUR"), self.driver.find_element_by_xpath("//div[@class='modal-body']/div[1]/div[1]/a").text.encode('ascii', 'ignore'))
            self.screenshot()
            
            self.driver.get("https://qa.247friend.org/login/?currency=GBP&trig=packagesModal")
            time.sleep(2)
            print("\n\t\t> Testing Package1 \"Buy Package\" GBP")
            print("\t\t> Expected GBP package: %s %s"%(package1['GBP'], "GBP"))
            print("\t\t> Live GBP package: %s"%(self.driver.find_element_by_xpath("//div[@class='modal-body']/div[1]/div[1]/a").text.encode('ascii', 'ignore')))
            self.assertEqual("%s %s"%(package1['GBP'], "GBP"), self.driver.find_element_by_xpath("//div[@class='modal-body']/div[1]/div[1]/a").text.encode('ascii', 'ignore'))
            self.screenshot()
            
            print("\n\t\t> changes in all currency in package1 verified!")
            print("\t\t> Test Passed.")
            self.screenshot()
            # if we are still in the try block after all of our assertions that 
            # means our test has had no failures, so we set the status to "pass"
            self.test_result = 'pass'

        except AssertionError as e:

            # if any assertions are false, we take a snapshot of the screen, log 
            # the error message, and set the score to "during tearDown()".

            snapshot_hash = self.api_session.post('https://crossbrowsertesting.com/api/v3/selenium/' + self.driver.session_id + '/snapshots').json()['hash']
            self.api_session.put('https://crossbrowsertesting.com/api/v3/selenium/' + self.driver.session_id + '/snapshots/' + snapshot_hash,
                data={'description':"AssertionError: " + str(e)})
            self.test_result = 'fail'
            raise

    def tearDown(self):
        self.screenshot()
        print("Done with session %s" % self.driver.session_id)
        self.driver.quit()
        # Here we make the api call to set the test's score.
        # Pass it it passes, fail if an assertion fails, unset if the test didn't finish
        if self.test_result is not None:
            self.api_session.put('https://crossbrowsertesting.com/api/v3/selenium/' + self.driver.session_id, 
                data={'action':'set_score', 'score':self.test_result})


if __name__ == '__main__':
    unittest.main()