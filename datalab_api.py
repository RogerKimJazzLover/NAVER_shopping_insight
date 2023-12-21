#PLEASE READ THIS!!!!!
#THIS 'API_KEYS' IS A PYTHON FILE OF MINE THAT SOTERS MY PRIVATE API KEYS.
from API_KEYS import * #SO DELETE THIS LINE!!!!!

import json, urllib.request

class DatalabShoppingAPI():
    #네이버 데이터 랩 쇼핑인사이트
    def __init__(self) -> None:
        self.client_id = data_lab_client_id #type your own client_id here. like, #client_id = "your_client_id"
        self.client_secret = data_lab_client_secret #type your own client_secret here.
        self.url = "https://openapi.naver.com/v1/datalab/shopping/categories"

    def CreateBody(self, startDate: str, endDate: str, category: list) -> json:
        #category is like: [{"name":"출산/육아", "param":["50000005"]}, {"name":"식품", "param":["50000006"]}],
        body = {
            "startDate":startDate,
            "endDate":endDate,
            "timeUnit":"date",
            "category": category,
            "device":"",
            "ages":[],
            "gender":""
        }
        body = json.dumps(body)
        return body

    def GetResponse(self, body: json):
        request = urllib.request.Request(self.url)
        request.add_header("X-Naver-Client-Id",self.client_id)
        request.add_header("X-Naver-Client-Secret",self.client_secret)
        request.add_header("Content-Type","application/json")
        response = urllib.request.urlopen(request, data=body.encode("utf-8"))
        return response
    
class DatalabSearchAPI():
    #네이버 데이터 랩 통합검색어
    def __init__(self) -> None:
        self.client_id = data_lab_search_client_id #type your own client_id here. like, #client_id = "your_client_id"
        self.client_secret = data_lab_search_client_secret #type your own client_secret here.
        self.url = "https://openapi.naver.com/v1/datalab/search"
    
    def CreateKeywordsGroups(self, group_name: str, keywords: list):
        keyword_groups = []

        keyword_group = {
            'groupName': group_name,
            'keywords': keywords
        }
        
        keyword_groups.append(keyword_group)
        return keyword_groups

    def CreateBody(self, startDate: str, endDate: str, keywords_groups: list):
        body = {
            "startDate": startDate,
            "endDate": endDate,
            "timeUnit": "date",
            "keywordGroups": keywords_groups,
            "device": "",
            "ages": [],
            "gender": ""
        }
        body = json.dumps(body, ensure_ascii=False)
        return body

    def GetResponse(self, body: json):
        request = urllib.request.Request(self.url)
        request.add_header("X-Naver-Client-Id",self.client_id)
        request.add_header("X-Naver-Client-Secret",self.client_secret)
        request.add_header("Content-Type","application/json")
        response = urllib.request.urlopen(request, data=body.encode("utf-8"))
        return response