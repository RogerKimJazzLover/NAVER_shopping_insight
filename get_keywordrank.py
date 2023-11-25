import requests, pprint, time
from datetime import date
import pandas as pd

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

def GetDate():
    '''
    어제의 날짜를 panda의 timestamp 형식으로 반환 합니다.
    쇼핑인사이트 데이터는 어제의 것만 제공 되는 것 같습니다.
    '''
    today = date.today()
    today = pd.to_datetime(today)
    today -= pd.to_timedelta(1, 'D')
    return today

def GetDateLastWeek(today):
    '''
    주어진 날짜(today)로 부터 일주일 전의 날짜를 panda의 timestamp 형식으로 반환 합니다.
    '''
    for i in range(7):
        today -= pd.to_timedelta(1, 'D')
    return today
    
def GetSubCategory(cid):
    '''
    하나의 대분류 키워드 (패션의류, 패션잡화) 의 서브 카테고리를 제공합니다.
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
    data = f"cid={cid}&timeUnit=date&startDate={startDate}&endDate={endDate}&page=1&count=10"
    url = "https://datalab.naver.com/shoppingInsight/getCategoryKeywordRank.naver"
    response = requests.post(url=url, headers=header, data=data)
    return response.json()

def main():
    keywords_arr = {}

    yesterday = GetDate()
    startDate = GetDateLastWeek(yesterday)
    
    #Turns each dates from, panda's timestamp data structure, to string
    startDate = startDate.strftime('%Y-%m-%d')
    endDate = yesterday.strftime('%Y-%m-%d')

    #adds information about the startDate and the endDate at the top of the keywords_arr dictionary
    keywords_arr['startDate'] = startDate
    keywords_arr['endDate'] = endDate

    for cat_name, cat_id in cid_lists.items():
        print(cat_name)
        res_dict = GetKeyWordRank(cat_id, startDate, endDate)
        keywords_arr[cat_name] = [] #creates another item in the dictionary with the category's name as the key, and an empty array as the value.
        for i in range(10):
            #appends each category into the empty array that was just created
            keywords_arr[cat_name].append(res_dict['ranks'][i]['keyword'])
        time.sleep(1) #without this, the server doesn't respond after the 생활/건강
        
    #pretty prints the resulting dictionary
    pprint.pprint(keywords_arr)

if __name__ == "__main__":
    main()