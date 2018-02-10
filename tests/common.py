# This python file is for common functionalities.
from configuration import config as cfg

class common_functionalities:
    def screenshot(self, api_session, id, desc):
        snapshot_hash = api_session.post(cfg.selenium_api_url + id + '/snapshots').json()['hash']
        api_session.put(cfg.selenium_api_url + id + '/snapshots/' + snapshot_hash, data={'description': desc})
    
    def set_status(self, api_session, id, result):
        api_session.put(cfg.selenium_api_url + id, 
        data={'action':'set_score', 'score':result})
    