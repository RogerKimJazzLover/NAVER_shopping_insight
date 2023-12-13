#PLEASE READ THIS!!!!!
#THIS 'API_KEYS' IS A LOCAL PYTHON FILE OF MINE IN MY LOCAL PC THAT SOTERS MY PRIVATE API KEYS.
from API_KEYS import * #SO DELETE THIS LINE!!!!!

from tabulate import tabulate
import hashlib, hmac, base64
import time, requests
import pandas as pd
import custom_exceptions

CUSTOMER_ID = ad_customer_id #type your own customer_id here. like,
#CUSTOMER_ID = "your_customer_id"
API_KEY = ad_licence_key #type your own licence_key here.
SECRET_KEY = ad_secret_key #type your own secret_key here.

BASE_URL = "https://api.naver.com"

def generate(timestamp, method, uri, secret_key):
	'''
	Default function provided by NAVER, that is required in order to use this API. (I have no idea what it does)
	'''
	message = "{}.{}.{}".format(timestamp, method, uri)
	hash = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)

	hash.hexdigest()
	return base64.b64encode(hash.digest())
    
def get_header(method, uri, api_key, secret_key, customer_id):
	'''
	Default function provided by NAVER, that is required in order to use this API. (I have no idea what it does)
	'''
	timestamp = str(round(time.time() * 1000))
	signature = generate(timestamp, method, uri, secret_key)

	return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': api_key, 'X-Customer': str(customer_id), 'X-Signature': signature}

def GetNumSearch(keywords):
	'''
	Takes in a list object containing five keywords
	Returns a list object with lenght of five, that provides the monthly number of searches for the each keywords given as the argument.
	'''
	global BASE_URL, CUSTOMER_ID, API_KEY, SECRET_KEY

	uri = '/keywordstool'
	method = 'GET'	
	query = {
		'siteId:': '',
		'biztpId':'',
		'hintKeywords':keywords,
		'event':'',
		'mont':'1',
		'showDetail':"1"
	}	
	response = requests.get(BASE_URL + uri, params=query, headers=get_header(method,uri, api_key=API_KEY, secret_key=SECRET_KEY, customer_id=CUSTOMER_ID))
       
	if response.status_code == 200:
		data_response = response.json()
		data_response = data_response['keywordList'][:5]
		return data_response
	else:
		raise custom_exceptions.ResponseError("Response Error: ", response.status_code)

def SortResponse(arr1, arr2):
	'''
	Sorts arr2 so that it is the same as arr1
	Returns sorted arr2
	'''
	arr1 = list(map(str.upper,arr1))
	order_dict = {color: index for index, color in enumerate(arr1)}
	arr2.sort(key=lambda x: order_dict[x["relKeyword"]])

	return arr2

def add_numSearch(table):
	'''
	Takes in the dataframe object 'table' which contains all the keywords
	Returns nothing, instead, modifies the 'table' variable in the main function, since dataframes are mutable when passed as argument.
	'''
	num_search = []
	compIdx = []
	for i in range(5, 121, 5):
		keywords = table["Keywords"][i-5:i]
		data = GetNumSearch(keywords)
		data = SortResponse(keywords, data)
		for k in range(5):
			num_search.append(data[k]["monthlyMobileQcCnt"] + data[k]["monthlyPcQcCnt"])
			compIdx.append(data[k]["compIdx"])
	table["Monthly_num_search"] = num_search
	table["Competitiveness"] = compIdx

def main():       
	time_period = ['d', 'w', 'm']
	for i in range(3):
		table = pd.read_csv(f"./data/{time_period[i]}_top10_keywords.csv", encoding="euc-kr") #Reads the table into a dataframe object
		add_numSearch(table) #Modifies the table so that it contains the monthly number of searches
		table.to_csv(f"./data/{time_period[i]}_top10_keywords.csv", encoding="euc-kr", index=False) #Saves the dataframe as a csv file.

if __name__ == "__main__":
      main()