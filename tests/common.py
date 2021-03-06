# This python file is for common functionalities.
from configuration import config as cfg
import time

class common_functionalities:
    def wait_till_visible(self, element):
        max_wait = 10
        while(len(element) > 0):
            time.sleep(0.5)
            if max_wait == 0:
                break
            max_wait -= 1
        print "Element now visible"

    def screenshot(self, api_session, id, desc):
        snapshot_hash = api_session.post(cfg.selenium_api_url + id + '/snapshots').json()['hash']
        api_session.put(cfg.selenium_api_url + id + '/snapshots/' + snapshot_hash, data={'description': desc})
    
    def set_status(self, api_session, id, result):
        api_session.put(cfg.selenium_api_url + id, 
        data={'action':'set_score', 'score':result})
    
    def login(self, driver, username, password):
        print "- Login using %s" %(username)
        driver.find_element_by_xpath("//header[@id='header']/div/div/div/i").click()
        driver.find_element_by_link_text("Log in").click()
        print "-- email address %s" %(username)
        driver.find_element_by_id("email_address").send_keys(username)
        print "-- password %s" %(password)
        driver.find_element_by_id("user_pass").send_keys(password)
        driver.find_element_by_xpath("//form[@id='loginform']/div/div/div[1]/label").click()
        driver.find_element_by_id("wp_submit").click()
    
    def logout(self, driver):
        print "- Logging out"
        driver.find_element_by_xpath("//header[@id='header']/div/div/div/i").click()
        
        driver.find_element_by_link_text("Log out").click()
        if len(driver.find_elements_by_link_text("log out")) != 0:
            driver.find_element_by_link_text("log out").click()

    def change_price_pkg(self, driver, pkg):
        print "- Changing package price"
        driver.get(pkg['PKGURL'])
        
        if len(driver.find_elements_by_xpath("//form[@name='add_new_package']/table")) > 0:
            time.sleep(2)
        print "-- USD: %s" %(pkg['USD'])
        driver.find_element_by_name("edit_package_price").clear()
        driver.find_element_by_name("edit_package_price").send_keys(pkg['USD'])
        print "-- AUD: %s" %(pkg['AUD'])
        driver.find_element_by_name("edit_aud_package_price").clear()
        driver.find_element_by_name("edit_aud_package_price").send_keys(pkg['AUD'])
        print "-- NZD: %s" %(pkg['NZD'])
        driver.find_element_by_name("edit_nzd_package_price").clear()
        driver.find_element_by_name("edit_nzd_package_price").send_keys(pkg['NZD'])
        print "-- CAD: %s" %(pkg['CAD'])
        driver.find_element_by_name("edit_cad_package_price").clear()
        driver.find_element_by_name("edit_cad_package_price").send_keys(pkg['CAD'])
        print "-- EUR: %s" %(pkg['EUR'])
        driver.find_element_by_name("edit_eur_package_price").clear()
        driver.find_element_by_name("edit_eur_package_price").send_keys(pkg['EUR'])
        print "-- GBP: %s" %(pkg['GBP'])
        driver.find_element_by_name("edit_gbp_package_price").clear()
        driver.find_element_by_name("edit_gbp_package_price").send_keys(pkg['GBP'])
        print "-- update complete"
        driver.find_element_by_xpath("//table[@id='price_fields']/tbody/tr[2]/td[1]/h3").click()
        driver.find_element_by_xpath("//table[@id='price_fields']/tbody/tr[3]/td[2]/button").click()
        
    def read_email():
        print "Accessing email account"
        
    def navigate_to_clients(self, driver, search):
        client_info = {}
        current_url = driver.current_url
        driver.get(current_url + "admin.php?page=client-users")
        driver.find_element_by_xpath("//div[@id='example_filter']/label/input").send_keys(search)
        for client in driver.find_elements_by_xpath("//table[@id='example']/tbody/tr"):
            client_info['name'] = client.find_element_by_xpath(".//td[1]").text.encode('ascii', 'ignore')
            client_info['email'] = client.find_element_by_xpath(".//td[2]").text.encode('ascii', 'ignore')
            client_info['balance'] = client.find_element_by_xpath(".//td[3]").text.encode('ascii', 'ignore')
        
        return client_info