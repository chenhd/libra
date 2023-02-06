
import requests
import requests_cache
from datetime import timedelta

# requests cache 缓存设置
requests_cache.install_cache(
    cache_name="requests_cache_Net_Base", 
    backend='sqlite',
    expire_after=timedelta(days=30),
    allowable_methods=['GET', 'POST'],
    )

class Net_Base:
    def __init__(self) -> None:
        self.session = requests.session()
    
    def get(self, url):
        res = self.session.get(url, headers=self.headers)
        assert res.status_code == 200
        return res
        