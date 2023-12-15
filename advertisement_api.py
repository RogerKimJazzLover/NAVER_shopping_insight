import hashlib, hmac, base64
from API_KEYS import *
import time

class AdAPI():
    def __init__(self) -> None:
        self.CUSTOMER_ID = ad_customer_id #type your own customer_id here. like,
        #CUSTOMER_ID = "your_customer_id"
        self.API_KEY = ad_licence_key #type your own licence_key here.
        self.SECRET_KEY = ad_secret_key #type your own secret_key here.

        self.BASE_URL = "https://api.naver.com"

    def generate(self, timestamp, method, uri):
        '''
        Default function provided by NAVER, that is required in order to use this API. (I have no idea what it does)
        '''
        message = "{}.{}.{}".format(timestamp, method, uri)
        hash = hmac.new(bytes(self.SECRET_KEY, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)

        hash.hexdigest()
        return base64.b64encode(hash.digest())
        
    def get_header(self, method, uri):
        '''
        Default function provided by NAVER, that is required in order to use this API. (I have no idea what it does)
        '''
        timestamp = str(round(time.time() * 1000))
        signature = self.generate(timestamp, method, uri)

        return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': self.API_KEY, 'X-Customer': str(self.CUSTOMER_ID), 'X-Signature': signature}
