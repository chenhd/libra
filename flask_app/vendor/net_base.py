
import requests
import requests_cache

requests_cache.install_cache("requests_cache_Net_Base", backend='sqlite')

class Net_Base:
    def __init__(self) -> None:
        self.session = requests.session()
    
    def get(self, url):
        res = self.session.get(url, headers=self.headers)
        assert res.status_code == 200
        return res
        