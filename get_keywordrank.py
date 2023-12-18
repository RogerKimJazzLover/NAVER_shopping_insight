import requests, time, json, pprint, sys
from tabulate import tabulate
from datetime import date
import custom_exceptions
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

def DisplayTimer(t: int):
    '''
    Prints out the timer into the terminal
    '''
    print("\nTimer Starting:")
    for i in range(t,0,-1):
        sys.stdout.write(str(i)+' ')
        sys.stdout.flush()
        time.sleep(1)

def GetEndDate():
    '''
    Returns yesterday in panda's timestamp variable
    '''
    today = date.today()
    today = pd.to_datetime(today)
    today -= pd.to_timedelta(1, 'D')
    return today

def GetStartDate(today, time_period):
    '''
    Returns a day/week/month ago from the given argument: today, in panda's timestamp variable
    '''
    if time_period == "d":
        today -= pd.to_timedelta(1, 'D')
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
        DisplayTimer(30)


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
            DisplayTimer(30)

    
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

    response = requests.get('https://api.ipify.org?format=json')
    data = response.json()
    ip_address = data['ip']

    print("Your IP address is:", ip_address)

    #2. Gets data frame then save as csv file, for each time_period(day, week and month)
    for j in range(3):
        print(f"Session{j+1}:")
        print("=" * 100)
        result_dataframe = GetCSV(startDate[j], endDate)
        DisplayTimer
        result_dataframe.to_csv(f"./data/{time_period[j]}_top10_keywords.csv", encoding="euc-kr", index=False) #saves the data into the "data" directory
    
if __name__ == "__main__":
    main()
