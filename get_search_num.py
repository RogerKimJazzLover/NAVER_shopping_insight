#PLEASE READ THIS!!!!!
#THIS 'API_KEYS' IS A LOCAL PYTHON FILE OF MINE IN MY LOCAL PC THAT SOTERS MY PRIVATE API KEYS.
from API_KEYS import * #SO DELETE THIS LINE!!!!!

from advertisement_api import AdAPI
from tabulate import tabulate
import custom_exceptions
import pandas as pd
import requests

def GetNumSearch(keywords, ad_api):
	'''
	Takes in a list object containing five keywords
	Returns a list object with lenght of five, that provides the monthly number of searches for the each keywords given as the argument.
	'''
	# global BASE_URL, CUSTOMER_ID, API_KEY, SECRET_KEY

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
	response = requests.get(ad_api.BASE_URL + uri, params=query, headers=ad_api.get_header(method,uri))
       
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

def add_numSearch(table, ad_api):
	'''
	Takes in the dataframe object 'table' which contains all the keywords
	Returns nothing, instead, modifies the 'table' variable in the main function, since dataframes are mutable when passed as argument.
	'''
	num_search = []
	compIdx = []
	for i in range(5, 121, 5):
		keywords = table["Keywords"][i-5:i]
		data = GetNumSearch(keywords, ad_api)
		data = SortResponse(keywords, data)
		for k in range(5):
			num_search.append(data[k]["monthlyMobileQcCnt"] + data[k]["monthlyPcQcCnt"])
			compIdx.append(data[k]["compIdx"])
	table["Monthly_num_search"] = num_search
	table["Competitiveness"] = compIdx

def main():       
	time_period = ['d', 'w', 'm']
	ad_api = AdAPI()
	for i in range(3):
		table = pd.read_csv(f"./data/{time_period[i]}_top10_keywords.csv", encoding="euc-kr") #Reads the table into a dataframe object
		add_numSearch(table, ad_api) #Modifies the table so that it contains the monthly number of searches
		print(f"\r{i+1}/3")
		table.to_csv(f"./data/{time_period[i]}_top10_keywords.csv", encoding="euc-kr", index=False) #Saves the dataframe as a csv file.

if __name__ == "__main__":
      main()