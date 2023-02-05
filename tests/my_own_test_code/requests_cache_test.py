#!/usr/bin/env python
import time
# from urllib import request

from requests_cache import CachedSession
import requests_cache
import requests

requests_cache.install_cache("hello", backend='sqlite')

def main():
    session = requests.session()
    # session = CachedSession('example_cache', backend='sqlite')

    # # The real request will only be made once; afterward, the cached response is used
    # for i in range(5):
    #     response = session.get('http://httpbin.org/get')

    # # This is more obvious when calling a slow endpoint
    # for i in range(5):
    #     response = session.get('http://httpbin.org/delay/2')

    # # Caching can be disabled if we want to get a fresh page and not cache it
    # with session.cache_disabled():
    #     print(session.get('http://httpbin.org/ip').text)

    # # Get some debugging info about the cache
    # print(session.cache)
    # print('Cached URLS:')
    # print('\n'.join(session.cache.urls))

    test_url = "http://127.0.0.1:8000/"
    for i in range(10):
        res = session.get(test_url)
        print(res.content)


if __name__ == "__main__":
    t = time.time()
    main()
    print('Elapsed: %.3f seconds' % (time.time() - t))