from email import header
import os
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

        self.base_store_data_path = "./flask_app/store_data/"
    
    def get(self, *args, **argv):
        res = self.session.get(*args, **argv) # todo: requests cache bug, same bytes but always 400.

        # if res.status_code != 200:
        #     print("res.from_cache: ", res.from_cache)

        assert res.status_code == 200 
        return res
    
    def post(self, *args, **argv):
        res = self.session.post(*args, **argv)
        assert res.status_code == 200
        return res
    
    def save_download_file(self, filename, content):
        filepath = self.base_store_data_path + filename
        if os.path.exists(filepath):
            pass
        else:
            with open(filepath, "wb") as f:
                f.write(content)
        
        return filepath
        