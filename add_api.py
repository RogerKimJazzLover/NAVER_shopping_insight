#PLEASE READ THIS!!!!!
#THIS 'API_KEYS' IS A LOCAL PYTHON FILE OF MINE IN MY LOCAL PC THAT SOTERS MY PRIVATE API KEYS.
from API_KEYS import * #SO DELETE THIS LINE!!!!!

import json, time, requests, pprint
import pandas as pd
import matplotlib.pyplot as plt

import hashlib
import hmac
import base64


def generate(timestamp, method, uri, secret_key):
    message = "{}.{}.{}".format(timestamp, method, uri)
    hash = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)
    
    hash.hexdigest()
    return base64.b64encode(hash.digest())
    
def get_header(method, uri, api_key, secret_key, customer_id):
	timestamp = str(round(time.time() * 1000))
	signature = generate(timestamp, method, uri, secret_key)

	return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': api_key, 'X-Customer': str(customer_id), 'X-Signature': signature}

def main():       
	CUSTOMER_ID = ad_customer_id #type your own customer_id here. like,
	#CUSTOMER_ID = "your_customer_id"
	API_KEY = ad_licence_key #type your own licence_key here.
	SECRET_KEY = ad_secret_key #type your own secret_key here.
        
	keywords = "행거"
	month = 1

	BASE_URL = "https://api.naver.com"
       
	uri = '/keywordstool'
	method = 'GET'	
	query = {
		'siteId:': '',
		'biztpId':'',
		'hintKeywords':keywords,
		'event':'',
		'mont':month,
		'showDetail':'1'
	}	
	response = requests.get(BASE_URL + uri, params=query, headers=get_header(method,uri, api_key=API_KEY, secret_key=SECRET_KEY, customer_id=CUSTOMER_ID))
       
	data_response = response.json()
	pprint.pprint(data_response['keywordList'][0])
              
	return 0

if __name__ == "__main__":
      main()