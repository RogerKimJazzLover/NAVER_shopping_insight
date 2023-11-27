#PLEASE READ THIS!!!!!
#THIS 'API_KEYS' IS A LOCAL PYTHON FILE OF MINE IN MY LOCAL PC THAT SOTERS MY PRIVATE API KEYS.
from API_KEYS import * #SO DELETE THIS LINE!!!!!

from tabulate import tabulate
import json, time, requests, pprint
import pandas as pd
import hashlib
import hmac
import base64

CUSTOMER_ID = ad_customer_id #type your own customer_id here. like,
#CUSTOMER_ID = "your_customer_id"
API_KEY = ad_licence_key #type your own licence_key here.
SECRET_KEY = ad_secret_key #type your own secret_key here.

BASE_URL = "https://api.naver.com"

def generate(timestamp, method, uri, secret_key):
    message = "{}.{}.{}".format(timestamp, method, uri)
    hash = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)
    
    hash.hexdigest()
    return base64.b64encode(hash.digest())
    
def get_header(method, uri, api_key, secret_key, customer_id):
	timestamp = str(round(time.time() * 1000))
	signature = generate(timestamp, method, uri, secret_key)

	return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': api_key, 'X-Customer': str(customer_id), 'X-Signature': signature}

class ResponseError(Exception):
	def __init__(self, message, value):
		self.messaage = message
		self.value = value

def get_keywordstool(keywords):
	global BASE_URL
	global CUSTOMER_ID
	global API_KEY
	global SECRET_KEY

	month = 1
	uri = '/keywordstool'
	method = 'GET'	
	query = {
		'siteId:': '',
		'biztpId':'',
		'hintKeywords':keywords,
		'event':'',
		'mont':month,
		'showDetail':"1"
	}	
	response = requests.get(BASE_URL + uri, params=query, headers=get_header(method,uri, api_key=API_KEY, secret_key=SECRET_KEY, customer_id=CUSTOMER_ID))
       
	if response.status_code == 200:
		data_response = response.json()
		data_response = data_response['keywordList'][:5]
		return data_response
	else:
		raise ResponseError("Response Error: ", response.status_code)

def add_numSearch(table):
	arr = []
	for i in range(5, 121, 5):
		keywords = table["Keywords"][i-5:i]
		data = get_keywordstool(keywords)
		for k in range(5):
			arr.append(data[k]["monthlyMobileQcCnt"] + data[k]["monthlyPcQcCnt"])
	table["Num_search"] = arr

def main():       
	time_period = 'd'
	table = pd.read_csv(f"./data/{time_period}_top10_keywords.csv", encoding="euc-kr")

	add_numSearch(table)

	print(tabulate(table, headers='keys', tablefmt='psql'))

	table.to_csv(f"./data/{time_period}_top10_keywords.csv", encoding="euc-kr")

if __name__ == "__main__":
      main()