import custom_exceptions, reusable_funcs
from tabulate import tabulate
import requests, time, json
from datetime import date
from tqdm import tqdm
import pandas as pd

'''
Search criterias
device = pc/mo
gender = f/m
age = 10,20,30...60
Total Combination: 240 for each category
'''

cid_lists = {
    "패션의류":50000000,
    "패션잡화":50000001,
    "화장품/미용":50000002,
    "디지털/가전":50000003,
    "가구/인테리어":50000004,
    "출산/육아":50000005,
    "식품":50000006,
    "스포츠/레저":50000007,
    "생활/건강":50000008,
    "여가/생활편의":50000009,
    "면세점":50000010,
    "도서":50005542
}

header = {
    "Referer":"https://datalab.naver.com/shoppingInsight/sCategory.naver",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8"
}
    
def GetSubCategory(cid):
    '''
    Returns a JSON variable containing the subcategory for the given category.
    '''
    #This header is NOT THE SAME as the global variable header. this just lacks the content type
    header = {
        "Referer":"https://datalab.naver.com/shoppingInsight/sCategory.naver",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    url = f"https://datalab.naver.com/shoppingInsight/getCategory.naver?cid={cid}"
    response = requests.get(url = url, headers = header)
    return response.json()

def GetKeyWordRank(cid, startDate: str, endDate: str) -> list:
    '''
    cid is the category id
    returns: response.json, the response from the server in json format
    '''
    global header
    url = "https://datalab.naver.com/shoppingInsight/getCategoryKeywordRank.naver"

    result = []
    for i in tqdm(range(1, 26)): #tqdm prints out the PROGRESS BAR TO THE TERMINAL
        data = f"cid={cid}&timeUnit=date&startDate={startDate}&endDate={endDate}&age=&gender=&device=&page={i}&count=20"
        response = requests.post(url=url, headers=header, data=data)

        if response.status_code != 200:
            raise custom_exceptions.ResponseError(response.status_code)
        response = response.json() #GETTING THE RESPONSE

        for i in range(20):
            #APPENDIND EACH KEYWORDS TO THE RESULT
            result.append(response['ranks'][i]['keyword'])

        time.sleep(0.5)
    return result

def GetJSON(startDate: str, endDate: str) -> json:
    '''
    Returns a JSON variable that contains the top 10 searcheds keywords for each categories.
    '''
    global cid_lists
    result_keyword = {}

    #adds information about the startDate and the endDate at the top of the result_keyword dictionary
    result_keyword['startDate'] = startDate
    result_keyword['endDate'] = endDate

    for cat_name, cat_id in cid_lists.items():
        print(cat_name)
        try:
            temp = GetKeyWordRank(cat_id, startDate, endDate) #Get the top 500 keywords into temporary list.
        except custom_exceptions.ResponseError as e:
            print(e)
        result_keyword[cat_name] = []
        result_keyword[cat_name] += temp
        reusable_funcs.DisplayTimer(30)


    return json.dumps(result_keyword, indent=4, ensure_ascii=False) #Turns dictionary into json file. 'ensure_ascii=False' is to solve bugs with Korean characters.

def GetCSV(startDate: str, endDate: str) -> pd.DataFrame:
    '''
    Returns a dataframe variable that contains the top 500 searched keywords for each categories.
    '''
    global cid_lists
    result_dataframe = {
        "Category_name":[],
        "Cat_id":[],
        "Keywords":[]
    }
    for i, (cat_name, cat_id) in enumerate(cid_lists.items()):
        print("\nCategory:", cat_name)
        try:
            temp = GetKeyWordRank(cat_id, startDate, endDate) #Get the top 500 keywords into temporary list.
        except custom_exceptions.ResponseError as e:
            print(e)
        
        result_dataframe["Category_name"] += [cat_name] * 500
        result_dataframe["Cat_id"] += [cat_id] * 500
        result_dataframe["Keywords"] += temp
    
        if i < len(cid_lists) - 1:  # Check if it's not the last iteration
            reusable_funcs.DisplayTimer(30)

    
    return pd.DataFrame(result_dataframe)

def main():
    #'d' for day, 'w' for week, 'm' for month.
    time_period = ['d', 'w', 'm']

    #1. Getting the startDate for each time period
    endDate = reusable_funcs.GetEndDate()
    startDate = []
    for i in range(3):
        temp = reusable_funcs.GetStartDate(endDate, time_period[i])
        startDate.append(temp.strftime('%Y-%m-%d')) #Turns the date from, panda's timestamp data structure, to string
    endDate = endDate.strftime('%Y-%m-%d')

    #2. Gets data frame then save as csv file, for each time_period(day, week and month)
    for j in range(3):
        print(f"\nSession{j+1}:")
        print("=" * 100)
        result_dataframe = GetCSV(startDate[j], endDate)
        reusable_funcs.DisplayTimer(30)
        result_dataframe.to_csv(f"./data/{time_period[j]}_top10_keywords.csv", encoding="euc-kr", index=False) #saves the data into the "data" directory
    
if __name__ == "__main__":
    main()
