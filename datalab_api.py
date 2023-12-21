#PLEASE READ THIS!!!!!
#THIS 'API_KEYS' IS A PYTHON FILE OF MINE THAT SOTERS MY PRIVATE API KEYS.
from API_KEYS import * #SO DELETE THIS LINE!!!!!

import json, urllib.request

class DatalabShoppingAPI():
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

    def CreateRequest(self, body: json):
        request = urllib.request.Request(self.url)
        request.add_header("X-Naver-Client-Id",self.client_id)
        request.add_header("X-Naver-Client-Secret",self.client_secret)
        request.add_header("Content-Type","application/json")
        response = urllib.request.urlopen(request, data=body.encode("utf-8"))
        
        return response