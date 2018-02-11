# This python file is for common functionalities.
from configuration import config as cfg
import time

class common_functionalities:
    def screenshot(self, api_session, id, desc):
        snapshot_hash = api_session.post(cfg.selenium_api_url + id + '/snapshots').json()['hash']
        api_session.put(cfg.selenium_api_url + id + '/snapshots/' + snapshot_hash, data={'description': desc})
    
    def set_status(self, api_session, id, result):
        api_session.put(cfg.selenium_api_url + id, 
        data={'action':'set_score', 'score':result})
    
    def login(self, driver, username, password):
        driver.find_element_by_xpath("//header[@id='header']/div/div/div/i").click()
        driver.find_element_by_link_text("Log in").click()
        driver.find_element_by_id("email_address").send_keys(username)
        driver.find_element_by_id("user_pass").send_keys(password)
        driver.find_element_by_xpath("//form[@id='loginform']/div/div/div[1]/label").click()
        driver.find_element_by_id("wp_submit").click()
    
    # def logout(self):
    
    
    
    def change_price_pkg(self, driver, pkg):
        driver.get(pkg['PKGURL'])
        
        if len(driver.find_elements_by_xpath("//form[@name='add_new_package']/table")) > 0:
            time.sleep(2)
        
        driver.find_element_by_name("edit_package_price").clear()
        driver.find_element_by_name("edit_package_price").send_keys(pkg['USD'])

        driver.find_element_by_name("edit_aud_package_price").clear()
        driver.find_element_by_name("edit_aud_package_price").send_keys(pkg['AUD'])

        driver.find_element_by_name("edit_nzd_package_price").clear()
        driver.find_element_by_name("edit_nzd_package_price").send_keys(pkg['NZD'])

        driver.find_element_by_name("edit_cad_package_price").clear()
        driver.find_element_by_name("edit_cad_package_price").send_keys(pkg['CAD'])

        driver.find_element_by_name("edit_eur_package_price").clear()
        driver.find_element_by_name("edit_eur_package_price").send_keys(pkg['EUR'])

        driver.find_element_by_name("edit_gbp_package_price").clear()
        driver.find_element_by_name("edit_gbp_package_price").send_keys(pkg['GBP'])
        
        driver.find_element_by_xpath("//table[@id='price_fields']/tbody/tr[2]/td[1]/h3").click()
        driver.find_element_by_xpath("//table[@id='price_fields']/tbody/tr[3]/td[2]/button").click()