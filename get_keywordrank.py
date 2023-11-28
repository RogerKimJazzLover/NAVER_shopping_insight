import requests, time, json, pprint
from tabulate import tabulate
from datetime import date
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

def GetEndDate():
    '''
    어제의 날짜를 panda의 timestamp 형식으로 반환 합니다.
    '''
    today = date.today()
    today = pd.to_datetime(today)
    today -= pd.to_timedelta(1, 'D')
    return today

def GetStartDate(today, time_period):
    '''
    주어진 날짜(today)로 부터 일주일/한달 전의 날짜를 panda의 timestamp 형식으로 반환 합니다.
    '''
    if time_period == "d":
        return today
    elif time_period == "w":
        for i in range(7):
            today -= pd.to_timedelta(1, 'D')
        return today
    else:
        return today - pd.DateOffset(months=1)
    
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

def GetKeyWordRank(cid, startDate, endDate):
    '''
    cid is the category id
    returns: response.json, the response from the server in json format
    '''
    global header
    data = f"cid={cid}&timeUnit=date&startDate={startDate}&endDate={endDate}&age=&gender=&device=&page=1&count=10"
    url = "https://datalab.naver.com/shoppingInsight/getCategoryKeywordRank.naver"
    response = requests.post(url=url, headers=header, data=data)
    return response.json()

def GetJSON(startDate, endDate):
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
        temporary_dict = GetKeyWordRank(cat_id, startDate, endDate) #Get the top 10 keywords into temporary_dict dictionary. This dictionary only stores the top 10 keywords of one category.
        result_keyword[cat_name] = [] #creates another item in the dictionary with the category's name as the key, and an empty array as the value.
        for i in range(10):
            #appends each category into the empty array that was just created
            result_keyword[cat_name].append(temporary_dict['ranks'][i]['keyword'])
        time.sleep(0.3) #without this, the server doesn't respond after the 생활/건강

    return json.dumps(result_keyword, indent=4, ensure_ascii=False) #Turns dictionary into json file. 'ensure_ascii=False' is to solve bugs with Korean characters.

def GetCSV(startDate, endDate):
    '''
    Returns a dataframe variable that contains the top 10 searcheds keywords for each categories.
    '''
    global cid_lists
    result_dataframe = {
        "Category_name":[],
        "Cat_id":[],
        "Keywords":[]
    }
    for cat_name, cat_id in cid_lists.items():
        print(cat_name)
        temporary_dict = GetKeyWordRank(cat_id, startDate, endDate) #Get the top 10 keywords into temporary_dict dictionary. This dictionary only stores the top 10 keywords of one category.
        for i in range(10):
            #appends name and id of each category name to the "Category_name" and "Cat_id" column.
            result_dataframe["Category_name"].append(cat_name)
            result_dataframe["Cat_id"].append(cat_id)
            #appends each keywords into the "Keywords" column
            result_dataframe["Keywords"].append(temporary_dict['ranks'][i]['keyword'])
        time.sleep(0.3) #without this, the server doesn't respond after the 생활/건강
    
    return pd.DataFrame(result_dataframe)

def main():
    #'d' for day, 'w' for week, 'm' for month.
    time_period = ['d', 'w', 'm']

    #1. Getting the startDate for each time period
    endDate = GetEndDate()
    startDate = []
    for i in range(3):
        temp = GetStartDate(endDate, time_period[i])
        startDate.append(temp.strftime('%Y-%m-%d')) #Turns the date from, panda's timestamp data structure, to string
    endDate = endDate.strftime('%Y-%m-%d')

    #2. Gets data frame then save as csv file, for each time_period(day, week and month)
    for j in range(3):
        result_dataframe = GetCSV(startDate[j], endDate)
        result_dataframe.to_csv(f"./data/{time_period[j]}_top10_keywords.csv", encoding="euc-kr", index=False) #saves the data into the "data" directory
    
if __name__ == "__main__":
    main()
